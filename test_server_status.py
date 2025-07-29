#!/usr/bin/env python3
"""
Скрипт для тестирования статуса сервера и проверки обновлений
"""

import requests
import json
import time
from datetime import datetime

def test_server():
    """Тестируем сервер"""
    
    print("🔍 Тестирование сервера...")
    
    try:
        # Проверяем здоровье сервера
        response = requests.get("http://localhost:8000/health", timeout=10)
        if response.status_code == 200:
            print("✅ Сервер работает")
            health_data = response.json()
            print(f"   Статус: {health_data.get('status')}")
            print(f"   База данных: {health_data.get('database')}")
        else:
            print(f"❌ Ошибка сервера: {response.status_code}")
            return
        
        # Получаем статистику
        response = requests.get("http://localhost:8000/api/stats/", timeout=10)
        if response.status_code == 200:
            stats = response.json()
            print(f"\n📊 Статистика:")
            print(f"   Всего новостей: {stats.get('total_news')}")
            print(f"   Категории: {stats.get('categories')}")
            print(f"   Последнее обновление: {stats.get('last_updated')}")
        
        # Получаем новости
        response = requests.get("http://localhost:8000/api/news/?limit=5", timeout=10)
        if response.status_code == 200:
            news_data = response.json()
            print(f"\n📰 Последние новости ({len(news_data.get('data', []))}):")
            
            for i, news in enumerate(news_data.get('data', [])[:3], 1):
                print(f"   {i}. {news.get('title', '')[:50]}...")
                print(f"      Источник: {news.get('source_name', 'N/A')}")
                print(f"      Категория: {news.get('category', 'N/A')}")
                print(f"      Дата: {news.get('publish_date', 'N/A')}")
                if news.get('media'):
                    print(f"      Медиа: {len(news.get('media', []))} элементов")
                print()
        
        print("🎉 Все тесты прошли успешно!")
        
    except requests.exceptions.ConnectionError:
        print("❌ Не удалось подключиться к серверу")
    except requests.exceptions.Timeout:
        print("❌ Таймаут запроса")
    except Exception as e:
        print(f"❌ Ошибка: {e}")

def monitor_updates():
    """Мониторим обновления каждые 5 минут"""
    
    print("\n🔄 Мониторинг обновлений (каждые 5 минут)...")
    print("Нажмите Ctrl+C для остановки")
    
    last_count = None
    
    try:
        while True:
            try:
                response = requests.get("http://localhost:8000/api/stats/", timeout=10)
                if response.status_code == 200:
                    stats = response.json()
                    current_count = stats.get('total_news', 0)
                    last_updated = stats.get('last_updated', 'N/A')
                    
                    if last_count is None:
                        print(f"📊 Начальное количество новостей: {current_count}")
                        last_count = current_count
                    elif current_count > last_count:
                        print(f"🎉 Новые новости! {last_count} → {current_count} (+{current_count - last_count})")
                        print(f"   Время обновления: {last_updated}")
                        last_count = current_count
                    else:
                        print(f"⏰ Проверка: {current_count} новостей (без изменений)")
                    
                time.sleep(300)  # 5 минут
                
            except KeyboardInterrupt:
                print("\n🛑 Мониторинг остановлен")
                break
            except Exception as e:
                print(f"❌ Ошибка мониторинга: {e}")
                time.sleep(60)  # Ждем минуту при ошибке
                
    except KeyboardInterrupt:
        print("\n🛑 Мониторинг остановлен")

if __name__ == "__main__":
    test_server()
    
    # Спрашиваем пользователя о мониторинге
    response = input("\nХотите запустить мониторинг обновлений? (y/n): ")
    if response.lower() == 'y':
        monitor_updates()
    else:
        print("✅ Тестирование завершено") 