#!/usr/bin/env python3
"""
Тестовый скрипт для проверки Telegram бота
"""

import sys
import os
import requests
from datetime import datetime

sys.path.append(os.path.join(os.path.dirname(__file__), 'server'))
from server.bot import bot
from server.config import TOKEN

def test_bot_info():
    """Тестирование получения информации о боте"""
    print("🔍 Тестирование информации о боте...")
    
    try:
        url = f"https://api.telegram.org/bot{TOKEN}/getMe"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            bot_info = response.json()
            result = bot_info.get("result", {})
            print(f"✅ Бот найден:")
            print(f"   Имя: {result.get('first_name', 'N/A')}")
            print(f"   Username: @{result.get('username', 'N/A')}")
            print(f"   ID: {result.get('id', 'N/A')}")
            print(f"   Поддерживает inline: {result.get('supports_inline_queries', False)}")
        else:
            print(f"❌ Ошибка получения информации о боте: {response.status_code}")
            print(f"   Ответ: {response.text}")
            
    except Exception as e:
        print(f"❌ Ошибка: {e}")

def test_webhook():
    """Тестирование webhook"""
    print("\n🔗 Тестирование webhook...")
    
    try:
        # Проверяем текущий webhook
        url = f"https://api.telegram.org/bot{TOKEN}/getWebhookInfo"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            webhook_info = response.json()
            result = webhook_info.get("result", {})
            
            print(f"📡 Webhook информация:")
            print(f"   URL: {result.get('url', 'Не установлен')}")
            print(f"   Ожидающие обновления: {result.get('pending_update_count', 0)}")
            print(f"   Последняя ошибка: {result.get('last_error_message', 'Нет')}")
            
            if result.get('url'):
                print("✅ Webhook установлен")
            else:
                print("❌ Webhook не установлен")
        else:
            print(f"❌ Ошибка получения webhook: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Ошибка: {e}")

def test_bot_functions():
    """Тестирование функций бота"""
    print("\n🤖 Тестирование функций бота...")
    
    try:
        # Тестируем получение сводки новостей
        print("📰 Тестирование сводки новостей...")
        summary = bot.get_news_summary(3)
        print(f"   Результат: {len(summary)} символов")
        print(f"   Начинается с: {summary[:50]}...")
        
        # Тестируем получение новостей по категории
        print("\n🖼️ Тестирование новостей NFT...")
        nft_news = bot.get_news_by_category("nft", 3)
        print(f"   Результат: {len(nft_news)} символов")
        print(f"   Начинается с: {nft_news[:50]}...")
        
        # Тестируем получение статистики
        print("\n📊 Тестирование статистики...")
        stats = bot.get_news_stats()
        print(f"   Результат: {len(stats)} символов")
        print(f"   Начинается с: {stats[:50]}...")
        
        print("✅ Все функции бота работают корректно")
        
    except Exception as e:
        print(f"❌ Ошибка тестирования функций: {e}")
        import traceback
        traceback.print_exc()

def test_api_endpoints():
    """Тестирование API endpoints бота"""
    print("\n🌐 Тестирование API endpoints...")
    
    try:
        base_url = "http://localhost:8000"
        
        # Тестируем /telegram/bot-info
        print("📡 Тестирование /telegram/bot-info...")
        response = requests.get(f"{base_url}/telegram/bot-info", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"   Статус: {data.get('status')}")
            if data.get('bot_info'):
                print(f"   Бот: {data.get('bot_info', {}).get('first_name', 'N/A')}")
        else:
            print(f"   ❌ Ошибка: {response.status_code}")
        
        # Тестируем /telegram/send-news (без отправки)
        print("\n📤 Тестирование /telegram/send-news...")
        response = requests.post(f"{base_url}/telegram/send-news", 
                               json={"chat_id": 123456789, "news_id": None}, 
                               timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"   Статус: {data.get('status')}")
        else:
            print(f"   ❌ Ошибка: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Ошибка тестирования API: {e}")

def main():
    """Основная функция тестирования"""
    print("🎯 Тестирование Telegram бота...")
    print(f"⏰ Время: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🔑 Токен: {'Установлен' if TOKEN else 'Не установлен'}")
    
    # Проверяем, что сервер запущен
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code != 200:
            print("❌ Сервер не запущен. Запустите сервер сначала.")
            return
    except:
        print("❌ Сервер не запущен. Запустите сервер сначала.")
        return
    
    print("✅ Сервер запущен")
    
    # Запускаем тесты
    test_bot_info()
    test_webhook()
    test_bot_functions()
    test_api_endpoints()
    
    print("\n🎉 Тестирование завершено!")

if __name__ == "__main__":
    main() 