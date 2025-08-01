#!/usr/bin/env python3
"""
Тестовый скрипт для проверки парсинга Telegram канала @nextgen_NFT
"""

import asyncio
import sys
import os

# Добавляем путь к серверу
sys.path.append(os.path.join(os.path.dirname(__file__), 'server'))

from server.parsers.telegram_news_service import TelegramNewsService

async def test_telegram_parsing():
    """Тестируем парсинг канала @nextgen_NFT"""
    
    print("🔍 Тестирование парсинга канала @nextgen_NFT...")
    
    # Создаем экземпляр сервиса
    service = TelegramNewsService()
    
    try:
        # Парсим канал
        posts = await service.fetch_telegram_channel('nextgen_NFT')
        
        print(f"\n✅ Успешно получено {len(posts)} постов")
        
        # Выводим детали каждого поста
        for i, post in enumerate(posts[:5], 1):  # Показываем первые 5 постов
            print(f"\n📝 Пост #{i}")
            print(f"   Заголовок: {post['title'][:100]}...")
            print(f"   Длина текста: {len(post['text'])} символов")
            print(f"   Время чтения: {post.get('reading_time', 'N/A')} мин")
            print(f"   Категория: {post['category']}")
            print(f"   Дата: {post['date']}")
            
            if post.get('media'):
                print(f"   Медиа: {post['media']['type']}")
                if post['media']['type'] == 'photo':
                    print(f"   Фото URL: {post['media']['url']}")
                elif post['media']['type'] == 'video':
                    print(f"   Видео URL: {post['media']['url']}")
                    print(f"   Превью: {post['media']['thumbnail']}")
            
            # Показываем первые 200 символов текста
            preview = post['text'][:200] + "..." if len(post['text']) > 200 else post['text']
            print(f"   Превью: {preview}")
            
            if post.get('content_html'):
                print(f"   HTML контент: {len(post['content_html'])} символов")
        
        # Статистика
        if posts:
            total_chars = sum(len(post['text']) for post in posts)
            avg_chars = total_chars / len(posts)
            print(f"\n📊 Статистика:")
            print(f"   Средняя длина поста: {avg_chars:.0f} символов")
            print(f"   Общий объем текста: {total_chars} символов")
            
            # Категории медиа
            media_types = {}
            for post in posts:
                if post.get('media'):
                    media_type = post['media']['type']
                    media_types[media_type] = media_types.get(media_type, 0) + 1
            
            if media_types:
                print(f"   Медиа: {media_types}")
        
    except Exception as e:
        print(f"❌ Ошибка при парсинге: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_telegram_parsing()) 