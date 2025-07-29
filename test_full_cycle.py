#!/usr/bin/env python3
"""
Тестовый скрипт для полного цикла парсинга и сохранения новостей
"""

import asyncio
import sys
import os
from datetime import datetime

# Добавляем путь к серверу
sys.path.append(os.path.join(os.path.dirname(__file__), 'server'))

from server.parsers.telegram_news_service import TelegramNewsService
from server.db import SessionLocal, NewsItem, NewsSource
from server.services.news_service import get_or_create_source

async def test_full_cycle():
    """Тестируем полный цикл: парсинг -> сохранение -> получение"""
    
    print("🔄 Тестирование полного цикла парсинга...")
    
    # Создаем экземпляр сервиса
    service = TelegramNewsService()
    
    try:
        # 1. Парсим канал
        print("\n📡 Шаг 1: Парсинг канала @nextgen_NFT...")
        posts = await service.fetch_telegram_channel('nextgen_NFT')
        
        if not posts:
            print("❌ Не удалось получить посты")
            return
            
        print(f"✅ Получено {len(posts)} постов")
        
        # 2. Сохраняем в базу данных
        print("\n💾 Шаг 2: Сохранение в базу данных...")
        
        db = SessionLocal()
        try:
            saved_count = 0
            
            for post in posts[:5]:  # Сохраняем первые 5 постов
                try:
                    # Получаем или создаём источник
                    source = get_or_create_source(
                        db, 
                        post.get('source', 'NextGen NFT'), 
                        url=f"https://t.me/nextgen_NFT", 
                        source_type='telegram', 
                        category='nft'
                    )
                    
                    # Проверяем, существует ли уже такая новость
                    existing = db.query(NewsItem).filter(
                        NewsItem.title == post['title']
                    ).first()
                    
                    if existing:
                        print(f"   ⏭️  Пост уже существует: {post['title'][:50]}...")
                        continue
                    
                    # Извлекаем медиа данные
                    image_url = None
                    video_url = None
                    
                    if post.get('media'):
                        if post['media']['type'] == 'photo':
                            image_url = post['media']['url']
                        elif post['media']['type'] == 'video':
                            video_url = post['media']['url']
                            if not image_url and post['media'].get('thumbnail'):
                                image_url = post['media']['thumbnail']
                    
                    # Получаем HTML контент
                    content_html = post.get('content_html', '')
                    
                    # Оценка времени чтения
                    reading_time = post.get('reading_time', 1)
                    
                    # Создаем новость
                    news_item = NewsItem(
                        source_id=source.id,
                        title=post['title'],
                        content=post['text'],
                        content_html=content_html,
                        link=post['link'],
                        publish_date=datetime.fromisoformat(post['date'].replace('Z', '+00:00')),
                        category='nft',
                        image_url=image_url,
                        video_url=video_url,
                        reading_time=reading_time,
                        views_count=0,
                        author=post.get('source'),
                        subtitle=None
                    )
                    
                    db.add(news_item)
                    saved_count += 1
                    print(f"   ✅ Сохранен: {post['title'][:50]}...")
                    
                except Exception as e:
                    print(f"   ❌ Ошибка сохранения: {e}")
                    continue
            
            db.commit()
            print(f"\n✅ Успешно сохранено {saved_count} новых постов")
            
        finally:
            db.close()
        
        # 3. Получаем из базы данных
        print("\n📖 Шаг 3: Получение из базы данных...")
        
        db = SessionLocal()
        try:
            # Получаем последние новости
            recent_news = db.query(NewsItem).filter(
                NewsItem.category == 'nft'
            ).order_by(NewsItem.publish_date.desc()).limit(10).all()
            
            print(f"✅ Получено {len(recent_news)} новостей из БД")
            
            for i, news in enumerate(recent_news[:3], 1):
                print(f"\n📰 Новость #{i}:")
                print(f"   Заголовок: {news.title}")
                print(f"   Длина текста: {len(news.content or '')} символов")
                print(f"   HTML контент: {len(news.content_html or '')} символов")
                print(f"   Время чтения: {news.reading_time or 0} мин")
                print(f"   Просмотры: {news.views_count or 0}")
                
                if news.image_url:
                    print(f"   Изображение: {news.image_url}")
                if news.video_url:
                    print(f"   Видео: {news.video_url}")
                
                # Показываем превью контента
                preview = news.content[:100] + "..." if len(news.content) > 100 else news.content
                print(f"   Превью: {preview}")
                
        finally:
            db.close()
        
        print("\n🎉 Полный цикл тестирования завершен успешно!")
        
    except Exception as e:
        print(f"❌ Ошибка в полном цикле: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_full_cycle()) 