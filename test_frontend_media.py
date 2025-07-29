#!/usr/bin/env python3
"""
Тестирование фронтенда с медиа
"""

import requests
import json

def test_frontend_media():
    """Тестирование фронтенда с медиа"""
    print("🎯 Тестирование фронтенда с медиа...")
    
    try:
        # Проверяем API
        print("📡 Проверка API...")
        response = requests.get("http://localhost:8000/api/news/?limit=5")
        
        if response.status_code == 200:
            data = response.json()
            news_items = data.get('data', [])
            
            print(f"✅ Получено {len(news_items)} новостей")
            
            # Проверяем медиа
            media_count = 0
            for i, item in enumerate(news_items):
                media = item.get('media', [])
                if media:
                    media_count += 1
                    print(f"📸 Новость #{i+1} (ID: {item['id']}):")
                    print(f"   Заголовок: {item['title'][:50]}...")
                    print(f"   Источник: {item['source_name']}")
                    print(f"   Медиа: {len(media)} элементов")
                    for j, media_item in enumerate(media):
                        print(f"     {j+1}. Тип: {media_item['type']}")
                        print(f"        URL: {media_item['url']}")
                        if media_item.get('thumbnail'):
                            print(f"        Thumbnail: {media_item['thumbnail']}")
            
            print(f"📊 Всего новостей с медиа: {media_count}")
            
            # Проверяем фронтенд
            print("\n🌐 Проверка фронтенда...")
            try:
                frontend_response = requests.get("http://localhost:3000", timeout=5)
                if frontend_response.status_code == 200:
                    print("✅ Фронтенд доступен")
                else:
                    print(f"❌ Фронтенд недоступен: {frontend_response.status_code}")
            except:
                print("❌ Фронтенд не запущен")
            
        else:
            print(f"❌ Ошибка API: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Ошибка: {e}")

if __name__ == "__main__":
    test_frontend_media() 