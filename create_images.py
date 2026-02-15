#!/usr/bin/env python3
"""
Создание placeholder изображений для меню бота
Выполняется один раз при первой инициализации
"""

from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

def create_placeholder_image(filename: str, title: str, color: tuple = (52, 152, 219)):
    """Создаёт простое placeholder изображение"""
    # Размеры: 1080x720 (хороший размер для Telegram)
    width, height = 1080, 720
    
    # Создаём изображение
    img = Image.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(img)
    
    # Заполняем цветной фон
    draw.rectangle([(0, 0), (width, height)], fill=color)
    
    # Добавляем текст (если есть PIL Font support)
    try:
        # Пытаемся использовать системный шрифт
        font = ImageFont.truetype("arial.ttf", 60)
    except:
        # Fallback на встроенный шрифт
        font = ImageFont.load_default()
    
    # Рисуем текст в центре
    text_bbox = draw.textbbox((0, 0), title, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    
    x = (width - text_width) // 2
    y = (height - text_height) // 2
    
    draw.text((x, y), title, fill='white', font=font)
    
    # Сохраняем
    output_path = Path(__file__).parent / "assets" / filename
    output_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(output_path)
    print(f"✅ Создан: {output_path}")

if __name__ == "__main__":
    # Создаём изображения для всех меню
    create_placeholder_image(
        "main_menu.jpg",
        "🏠 ГЛАВНОЕ МЕНЮ",
        color=(52, 152, 219)  # Синий
    )
    
    create_placeholder_image(
        "profile_menu.jpg",
        "👤 МОЙ ПРОФИЛЬ",
        color=(46, 204, 113)  # Зелёный
    )
    
    create_placeholder_image(
        "tech_section.jpg",
        "⚙ ТЕХ.РАЗДЕЛ",
        color=(155, 89, 182)  # Фиолетовый
    )
    
    print("\n✅ Все placeholder изображения созданы!")
    print("📁 Расположение: ./assets/")
