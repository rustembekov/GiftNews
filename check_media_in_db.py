#!/usr/bin/env python3
"""
Скрипт для проверки медиа в базе данных
"""

import sys
import os
import json

sys.path.append(os.path.join(os.path.dirname(__file__), 'server'))
from server.db import get_db_session, NewsItem

def check_media_in_db():
    """Проверяем медиа в базе данных"""
    print("🔍 Проверка медиа в базе данных...")
    
    try:
        with get_db_session() as session:
            # Получаем все новости с медиа
            news_items = session.query(NewsItem).all()
            
            print(f"📊 Всего новостей в базе: {len(news_items)}")
            
            media_count = 0
            media_items = []
            
            for item in news_items:
                if item.media:
                    media_count += 1
                    media_items.append({
                        'id': item.id,
                        'title': item.title[:50] + "..." if len(item.title) > 50 else item.title,
                        'media': item.media,
                        'source': item.source.name if item.source else "Unknown"
                    })
            
            print(f"📸 Новостей с медиа: {media_count}")
            
            if media_items:
                print("\n📋 Детали медиа:")
                for item in media_items[:5]:  # Показываем первые 5
                    print(f"\n   ID: {item['id']}")
                    print(f"   Заголовок: {item['title']}")
                    print(f"   Источник: {item['source']}")
                    print(f"   Медиа: {json.dumps(item['media'], indent=2, ensure_ascii=False)}")
            else:
                print("❌ Медиа не найдено в базе данных")
            
            # Проверяем новости от @nextgen_NFT
            print(f"\n🎯 Проверка новостей от @nextgen_NFT:")
            nextgen_news = session.query(NewsItem).join(NewsItem.source).filter(
                NewsItem.source.has(name="NextGen NFT")
            ).all()
            
            print(f"   Всего новостей от NextGen NFT: {len(nextgen_news)}")
            
            nextgen_media = 0
            for item in nextgen_news:
                if item.media:
                    nextgen_media += 1
                    print(f"   ✅ ID {item.id}: {len(item.media)} медиа элементов")
                    print(f"      Медиа: {item.media}")
            
            print(f"   Новостей с медиа от NextGen NFT: {nextgen_media}")
            
    except Exception as e:
        print(f"❌ Ошибка при проверке базы данных: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check_media_in_db() 