import sqlite3
import sys

sys.path.insert(0, 'src')

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

print(f'\nВсего кнопок в профиле: {len(profile_buttons)} (должно быть 4)')

# Проверка что старые кнопки удалены из главного меню
print('\n=== ПРОВЕРКА УДАЛЕНИЯ СТАРЫХ КНОПОК ===')
cursor.execute('SELECT COUNT(*) FROM button_configs WHERE menu_type = "main_menu" AND button_id IN ("my_keys", "buy_key", "topup", "support", "about", "speed", "howto")')
old_count = cursor.fetchone()[0]
print(f'Старых кнопок в главном меню: {old_count} (должно быть 0)')

if old_count == 0:
    print('\n✅ МИГРАЦИЯ УСПЕШНА! Все старые кнопки удалены.')
else:
    print(f'\n❌ ОШИБКА! В главном меню остались {old_count} старых кнопок.')

conn.close()
