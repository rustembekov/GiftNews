#!/usr/bin/env python3
"""
Тест для проверки медиа в API
"""

import requests
import json

def test_media_api():
    """Тестируем API на предмет медиа"""
    print("🔍 Тестируем API на предмет медиа...")
    
    try:
        # Тестируем базовый API
        response = requests.get("http://localhost:8000/api/news/?limit=5", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ API работает, получено {len(data.get('data', []))} новостей")
            
            # Проверяем медиа в каждой новости
            for i, news in enumerate(data.get('data', [])[:3]):
                print(f"\n📰 Новость {i+1}: {news.get('title', '')[:50]}...")
                print(f"   ID: {news.get('id')}")
                print(f"   Категория: {news.get('category')}")
                
                media = news.get('media', [])
                if media:
                    print(f"   📷 Медиа найдено: {len(media)} элементов")
                    for j, media_item in enumerate(media):
                        print(f"      {j+1}. Тип: {media_item.get('type')}")
                        print(f"         URL: {media_item.get('url', 'N/A')[:50]}...")
                        if media_item.get('thumbnail'):
                            print(f"         Thumbnail: {media_item.get('thumbnail')[:50]}...")
                else:
                    print("   ❌ Медиа не найдено")
                    
                    # Проверяем image_url и video_url как fallback
                    if news.get('image_url'):
                        print(f"   🖼️ Image URL: {news.get('image_url')[:50]}...")
                    if news.get('video_url'):
                        print(f"   🎬 Video URL: {news.get('video_url')[:50]}...")
        else:
            print(f"❌ API вернул статус {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Не удалось подключиться к API. Проверьте, что сервер запущен.")
    except Exception as e:
        print(f"❌ Ошибка: {e}")

if __name__ == "__main__":
    test_media_api() 