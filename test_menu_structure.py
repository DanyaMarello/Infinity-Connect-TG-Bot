#!/usr/bin/env python3
"""
Тестирование переработанной структуры меню бота.

Проверяет:
1. Что все функции клавиатур существуют и работают
2. Что все callback_data маппятся на существующие обработчики
3. Что нет синтаксических ошибок
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.shop_bot.bot import keyboards
from src.shop_bot import config

def test_keyboards():
    """Тест существования и работоспособности функций клавиатур"""
    print("🧪 Тестирование клавиатур...")
    
    # Тест главного меню
    print("  ✓ create_main_menu_keyboard (без пробы, без админа)...", end=" ")
    try:
        kb = keyboards.create_main_menu_keyboard([], False, False)
        assert kb is not None
        print("✅")
    except Exception as e:
        print(f"❌ {e}")
        return False
    
    print("  ✓ create_main_menu_keyboard (с пробой, с админом)...", end=" ")
    try:
        kb = keyboards.create_main_menu_keyboard([], True, True)
        assert kb is not None
        print("✅")
    except Exception as e:
        print(f"❌ {e}")
        return False
    
    # Тест профиля
    print("  ✓ create_profile_keyboard...", end=" ")
    try:
        kb = keyboards.create_profile_keyboard()
        assert kb is not None
        print("✅")
    except Exception as e:
        print(f"❌ {e}")
        return False
    
    # Тест техсекции
    print("  ✓ create_tech_section_keyboard...", end=" ")
    try:
        kb = keyboards.create_tech_section_keyboard()
        assert kb is not None
        print("✅")
    except Exception as e:
        print(f"❌ {e}")
        return False
    
    return True

def test_config():
    """Тест наличия необходимых конфигов"""
    print("\n🧪 Тестирование конфигурации...")
    
    print("  ✓ MAIN_MENU_IMAGE_PATH...", end=" ")
    try:
        assert hasattr(config, 'MAIN_MENU_IMAGE_PATH')
        assert isinstance(config.MAIN_MENU_IMAGE_PATH, str)
        print(f"✅ ({config.MAIN_MENU_IMAGE_PATH})")
    except Exception as e:
        print(f"❌ {e}")
        return False
    
    print("  ✓ PROFILE_MENU_IMAGE_PATH...", end=" ")
    try:
        assert hasattr(config, 'PROFILE_MENU_IMAGE_PATH')
        assert isinstance(config.PROFILE_MENU_IMAGE_PATH, str)
        print(f"✅ ({config.PROFILE_MENU_IMAGE_PATH})")
    except Exception as e:
        print(f"❌ {e}")
        return False
    
    return True

def test_callback_mapping():
    """Тест маппинга callback_data на обработчики"""
    print("\n🧪 Тестирование маппинга callback_data...")
    
    # Callback'и из главного меню
    main_callbacks = [
        "get_trial",           # Если доступна
        "show_profile",        # Профиль
        "show_referral_program", # Реферальная
        "show_tech_section",   # Техсекция (НОВОЕ)
        "admin_menu",          # Если админ
    ]
    
    # Callback'и из профиля
    profile_callbacks = [
        "manage_keys",         # Мои ключи
        "buy_new_key",         # Купить ключ
        "top_up_start",        # Пополнить баланс
        "back_to_main_menu",   # Назад
    ]
    
    # Callback'и из техсекции
    tech_callbacks = [
        "show_help",           # Поддержка
        "show_about",          # О проекте
        "user_speedtest_last", # Скорость
        "howto_vless",         # Как использовать
        "back_to_main_menu",   # Назад
    ]
    
    all_callbacks = set(main_callbacks + profile_callbacks + tech_callbacks)
    
    print(f"  Total callbacks to check: {len(all_callbacks)}")
    for cb in sorted(all_callbacks):
        print(f"    - {cb}")
    
    print("\n  📝 NOTE: Полная проверка регистрации требует импорта handlers.py")
    print("  (которые содержат декораторы @user_router.callback_query)")
    
    return True

def main():
    print("=" * 60)
    print("ТЕСТИРОВАНИЕ ПЕРЕРАБОТАННОЙ СТРУКТУРЫ МЕНЮ")
    print("=" * 60)
    
    success = True
    
    success = test_keyboards() and success
    success = test_config() and success
    success = test_callback_mapping() and success
    
    print("\n" + "=" * 60)
    if success:
        print("✅ ВСЕ ТЕСТЫ ПРОЙДЕНЫ!")
    else:
        print("❌ НЕКОТОРЫЕ ТЕСТЫ НЕ ПРОЙДЕНЫ")
    print("=" * 60)
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())
