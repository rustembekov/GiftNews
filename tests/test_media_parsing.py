#!/usr/bin/env python3
"""
Тестовый скрипт для проверки извлечения медиа из Telegram постов
"""

import asyncio
import sys
import os
import requests
from urllib.parse import urlparse

# Добавляем путь к серверу
sys.path.append(os.path.join(os.path.dirname(__file__), 'server'))

from server.parsers.telegram_news_service import TelegramNewsService

async def test_media_parsing():
    """Тестируем извлечение медиа из Telegram постов"""
    
    print("🔍 Тестирование извлечения медиа из канала @nextgen_NFT...")
    
    # Создаем экземпляр сервиса
    service = TelegramNewsService()
    
    try:
        # Парсим канал
        posts = await service.fetch_telegram_channel('nextgen_NFT')
        
        print(f"\n✅ Получено {len(posts)} постов")
        
        # Анализируем медиа
        media_stats = {}
        media_posts = []
        
        for i, post in enumerate(posts):
            if post.get('media'):
                media_type = post['media']['type']
                media_stats[media_type] = media_stats.get(media_type, 0) + 1
                media_posts.append((i+1, post))
        
        print(f"\n📊 Статистика медиа:")
        for media_type, count in media_stats.items():
            print(f"   {media_type}: {count}")
        
        # Показываем детали постов с медиа
        print(f"\n📸 Посты с медиа:")
        for post_num, post in media_posts[:5]:  # Показываем первые 5
            media = post['media']
            print(f"\n📝 Пост #{post_num}:")
            print(f"   Заголовок: {post['title'][:50]}...")
            print(f"   Тип медиа: {media['type']}")
            print(f"   URL: {media['url']}")
            if media.get('thumbnail'):
                print(f"   Thumbnail: {media['thumbnail']}")
            
            # Проверяем доступность изображения
            if media['type'] == 'photo' and media['url']:
                try:
                    response = requests.head(media['url'], timeout=5)
                    if response.status_code == 200:
                        print(f"   ✅ Изображение доступно")
                    else:
                        print(f"   ❌ Изображение недоступно (статус: {response.status_code})")
                except Exception as e:
                    print(f"   ❌ Ошибка проверки изображения: {e}")
        
        # Тестируем разные URL форматы
        print(f"\n🔗 Тестирование URL форматов:")
        test_urls = [
            "https://t.me/nextgen_NFT/321",
            "https://cdn4.telegram-cdn.org/file/321.jpg",
            "https://cdn4.telegram-cdn.org/file/321.jpg?size=w"
        ]
        
        for url in test_urls:
            try:
                response = requests.head(url, timeout=5)
                print(f"   {url}: {'✅' if response.status_code == 200 else '❌'} (статус: {response.status_code})")
            except Exception as e:
                print(f"   {url}: ❌ Ошибка: {e}")
        
    except Exception as e:
        print(f"❌ Ошибка при тестировании медиа: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_media_parsing()) 