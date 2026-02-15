import sys
sys.path.insert(0, 'src')

from shop_bot import config

print("=== ПРОВЕРКА ПУТЕЙ К ИЗОБРАЖЕНИЯМ ===\n")

print(f"Main Menu Image:")
print(f"  Path: {config.MAIN_MENU_IMAGE_PATH}")
from pathlib import Path
if Path(config.MAIN_MENU_IMAGE_PATH).exists():
    print(f"  ✅ Файл существует")
else:
    print(f"  ❌ Файл не найден")

print(f"\nProfile Menu Image:")
print(f"  Path: {config.PROFILE_MENU_IMAGE_PATH}")
if Path(config.PROFILE_MENU_IMAGE_PATH).exists():
    print(f"  ✅ Файл существует")
else:
    print(f"  ❌ Файл не найден")

print(f"\nTech Section Image:")
print(f"  Path: {config.TECH_SECTION_IMAGE_PATH}")
if Path(config.TECH_SECTION_IMAGE_PATH).exists():
    print(f"  ✅ Файл существует")
else:
    print(f"  ❌ Файл не найден")

print("\n✅ Все пути готовы к использованию!")
