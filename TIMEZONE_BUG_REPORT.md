# Timezone Bug Report и Plan Исправлений

## 🔴 КРИТИЧЕСКИЕ НАЙДЕННЫЕ ПРОБЛЕМЫ

### 1. **TIMEZONE BUG В ЛОГИКЕ ПРОДЛЕНИЯ ПОДПИСКИ** (Root Cause: -3 часа)

**Место**: `src/shop_bot/bot/handlers.py` строки 3066-3106
**Проблема**: Смешивание timezone-aware и naive datetime при расчёте новой даты

**Симптом**: 
- Подписка продлевается на -3 часа
- Пример: должна быть 11:25 → становится 8:25

**Root Cause Analysis**:
```python
# Строка 3079 в handlers.py
current_expiry_dt = datetime.fromisoformat(cur_exp)  # NAIVE (no timezone info)
if current_expiry_dt.tzinfo is None:
    current_expiry_dt = current_expiry_dt.replace(tzinfo=timezone.utc)  # Добавляем UTC

# Строка 3101
expiry_ts_param = int(new_dt.timestamp() * 1000)  # new_dt is UTC-aware!
```

**Проблема**: 
1. Дата в БД хранится как NAIVE datetime строка (например: "2025-02-10 11:25:00")
2. Код интерпретирует эту строку как UTC при `replace(tzinfo=timezone.utc)`
3. Но на самом деле в БД может храниться локальное время (Moscow +03:00)
4. Когда конвертируем в timestamp и потом обратно → получаем -3 часа

**Диаграмма ошибки**:
```
BD: "2025-02-10 11:25:00" (actually Moscow time)
    ↓
parse as naive datetime
    ↓
replace(tzinfo=UTC) — НЕПРАВИЛЬНО! Это Moscow, не UTC
    ↓
calculate new_dt + timedelta
    ↓
timestamp() → преобразование "как будто это UTC" → получаем неправильное значение
    ↓
Result: -3 часа потеряны
```

---

### 2. **INCONSISTENT DATETIME STORAGE IN DATABASE**

**Проблемы**:
- `expire_at` хранится как строка "2025-02-10 11:25:00" (NAIVE)
- `expiry_timestamp_ms` хранится как int (UTC миллисекунды)
- `expiry_date` - неясный формат
- При чтении из БД могут использоваться разные поля → путаница

**Files affected**:
- `database.py` - функции `_to_datetime_str()`, `_now_str()`
- `remnawave_repository.py` - функции с работой с expiry
- `handlers.py` - логика продления

---

### 3. **INCOMPLETE TIME_UTILS MODULE USAGE**

**Найдено 50+ мест** где используется прямой `datetime.now()`, `.utcnow()`, `.timestamp()` вместо `time_utils`:

- `app.py` line 655: `datetime.fromisoformat(expiry).timestamp()`
- `app.py` line 729: `expiry_dt.replace(tzinfo=timezone.utc).timestamp()`
- `remnawave_api.py` line 514: `expire_dt.replace(tzinfo=timezone.utc).timestamp()`
- `scheduler.py` line 219-220: `.timestamp()` для сравнения
- И многие другие...

**time_utils.py имеет функции**:
```python
def now() → datetime (локальное время)
def now_utc() → datetime (UTC)
def to_utc_ms(dt) → int (миллисекунды)
def from_utc_ms(ms) → datetime (обратно в UTC datetime)
```

Но они используются не везде.

---

## 📋 НАЙДЕННЫЕ ДОПОЛНИТЕЛЬНЫЕ ПРОБЛЕМЫ

### 4. **ADMIN NOTIFICATION PROBLEM**

**Место**: `handlers.py` line 2785
**Текущее**: Отправляет только `user_id`
**Требуется**: Если есть username → отправлять `@username (user_id)`, иначе `user_id`

```python
# Current (неправильно):
f"👤 Пользователь: {user_id}\n"

# Required:
f"👤 Пользователь: {username_or_user_id}\n"
```

---

### 5. **MISSING FEATURE: TRANSACTIONS IN ADMIN BOT PANEL**

**Требуется**: Кнопка "📊 Последние транзакции" в админ панели бота
**Что нужно**: Вывод 10 последних транзакций в формате компактном

**Data source**: `remnawave_repository.get_recent_transactions(limit=10)`

---

### 6. **SPEEDTEST OUTPUT FORMATTING ISSUE**

**Место**: `admin_handlers.py` line 862 - существует форматирование, но может быть улучшено
**Проблема**: 
- При ошибке сервера выводятся мусорные значения (0, None, пустые строки)
- Нет явного "Offline" статуса
- Временная метка результата не сохраняется

---

### 7. **SCHEDULER/EXPIRATION LOGIC RACE CONDITIONS**

**Место**: `scheduler.py` - функция `check_expiring_subscriptions()` и `sync_keys_with_panels()`
**Проблемы**:
- Сравнение timestamps может быть неточным из-за timezone mix
- Удаление ключей раньше времени возможно при timezone ошибках
- Нет гарантии atomicity при синхронизации с Remnawave

---

## ✅ PLAN ИСПРАВЛЕНИЙ

### Phase 1: Fix Subscription Renewal Logic
1. Убедиться, что ВСЕ datetime в БД хранятся в UTC (строки или int milliseconds)
2. Переписать логику продления в `handlers.py` с правильной обработкой timezone
3. Добавить комментарии о том, когда datetime является timezone-aware vs naive
4. Unit tests для проверки

### Phase 2: Standardize DateTime Storage
1. Проверить все поля в database schema
2. Убедиться, что функции `_to_datetime_str()` работают правильно
3. Все timestamp conversions → через `time_utils`

### Phase 3: Complete time_utils Integration
1. Заменить все прямые `datetime.now()`, `.utcnow()`, `.timestamp()` на `time_utils`
2. Убедиться, что нет "orphan" datetime операций

### Phase 4: Add Missing Features
1. Username в админ уведомлениях
2. Кнопка и логика для последних транзакций в боте
3. Улучшенное форматирование speedtest с Offline status и timestamp

### Phase 5: Audit & Testing
1. Проверить scheduler логику на race conditions
2. Написать unit tests для timezone расчётов
3. Validate database consistency

---

## 🧪 TEST CASES

```python
# Test 1: Subscription renewal when current_expiry > now
# Expected: new_expiry = current_expiry + duration
assert new_expiry == current + 30_days

# Test 2: Subscription renewal when current_expiry < now (overdue)
# Expected: new_expiry = now + duration (not current + duration!)
assert new_expiry == now + 30_days

# Test 3: Timezone conversion consistency
# Input: "2025-02-10 11:25:00" (stored as UTC string)
# Expected: when displayed in Moscow tz → "2025-02-10 14:25:00"
assert moscow_time == utc_time + 3_hours

# Test 4: Admin notification format
# With username:
assert "👤 Пользователь: @username (12345)" in notification
# Without username:
assert "👤 Пользователь: 12345" in notification
```

---

## 📝 FILES TO MODIFY

High Priority:
- ✅ `src/shop_bot/bot/handlers.py` (lines 3066-3106) - renewal logic
- ✅ `src/shop_bot/modules/remnawave_api.py` (lines 480-530) - API call logic
- ✅ `src/shop_bot/data_manager/database.py` - datetime helper functions
- ✅ `src/shop_bot/bot/handlers.py` (line 2785) - admin notification

Medium Priority:
- `src/shop_bot/data_manager/scheduler.py` - sync logic
- `src/shop_bot/webhook_server/app.py` - all datetime operations
- `src/shop_bot/bot/admin_handlers.py` - speedtest formatting, add transactions

Low Priority:
- Documentation updates
- Complete the example in README

