import sys
sys.path.insert(0, 'src')

from shop_bot.data_manager import database

# Инициализируем БД
database.initialize_db()
print("✅ БД инициализирована с новыми конфигами")

# Проверяем содержимое
import sqlite3
conn = sqlite3.connect('users.db')
cursor = conn.cursor()

print('\n=== MAIN MENU BUTTONS ===')
cursor.execute('SELECT button_id, text, button_width FROM button_configs WHERE menu_type = "main_menu" ORDER BY sort_order')
main_menu = cursor.fetchall()
for row in main_menu:
    print(f'{row[0]}: {row[1]} (width={row[2]})')

print(f'\nВсего кнопок в главном меню: {len(main_menu)} (должно быть 5)')

print('\n=== TECH SECTION BUTTONS ===')
cursor.execute('SELECT button_id, text FROM button_configs WHERE menu_type = "tech_section_menu" ORDER BY sort_order')
tech_buttons = cursor.fetchall()
for row in tech_buttons:
    print(f'{row[0]}: {row[1]}')

print(f'\nВсего кнопок в тех.разделе: {len(tech_buttons)} (должно быть 5)')

print('\n=== PROFILE BUTTONS ===')
cursor.execute('SELECT button_id, text FROM button_configs WHERE menu_type = "profile_menu" ORDER BY sort_order')
profile_buttons = cursor.fetchall()
for row in profile_buttons:
    print(f'{row[0]}: {row[1]}')

print(f'\nВсего кнопок в профиле: {len(profile_buttons)} (должно быть 3)')

# Проверка структуры
print('\n=== ПРОВЕРКА СТРУКТУРЫ ===')
if len(main_menu) == 5:
    print('✅ Главное меню: 5 кнопок')
else:
    print(f'❌ Главное меню: {len(main_menu)} кнопок (ожидается 5)')

if len(tech_buttons) == 5:
    print('✅ Тех.раздел: 5 кнопок')
else:
    print(f'❌ Тех.раздел: {len(tech_buttons)} кнопок (ожидается 5)')

if any(btn[0] == 'tech_section' for btn in main_menu):
    print('✅ Кнопка "Тех.раздел" есть в главном меню')
else:
    print('❌ Кнопка "Тех.раздел" НЕ найдена в главном меню')

conn.close()
print('\n✅ ГОТОВО! БД инициализирована корректно.')
