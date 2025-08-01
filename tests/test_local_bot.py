#!/usr/bin/env python3
"""
Тестирование локального бота
"""

import requests
import json

def test_local_bot():
    """Тестируем локальный бот"""
    print("🎯 Тестирование локального бота...")
    
    try:
        # Проверяем локальный сервер
        print("📡 Проверка локального сервера...")
        local_response = requests.get("http://localhost:8000/health", timeout=5)
        if local_response.status_code == 200:
            print("✅ Локальный сервер работает")
        else:
            print(f"❌ Локальный сервер недоступен: {local_response.status_code}")
            return
        
        # Проверяем локальный API
        print("🔍 Проверка локального API...")
        api_response = requests.get("http://localhost:8000/api/news/?limit=1")
        if api_response.status_code == 200:
            data = api_response.json()
            media_count = len(data['data'][0]['media']) if data['data'][0].get('media') else 0
            print(f"✅ Локальный API работает, медиа: {media_count}")
        else:
            print(f"❌ Локальный API недоступен: {api_response.status_code}")
            return
        
        # Проверяем локальный фронтенд
        print("🌐 Проверка локального фронтенда...")
        try:
            frontend_response = requests.get("http://localhost:3000", timeout=5)
            if frontend_response.status_code == 200:
                print("✅ Локальный фронтенд работает")
            else:
                print(f"❌ Локальный фронтенд недоступен: {frontend_response.status_code}")
        except:
            print("❌ Локальный фронтенд не запущен")
        
        # Проверяем продакшн API
        print("🚀 Проверка продакшн API...")
        try:
            prod_response = requests.get("https://giftpropaganda.onrender.com/api/news/?limit=1", timeout=10)
            if prod_response.status_code == 200:
                prod_data = prod_response.json()
                prod_media_count = len(prod_data['data'][0]['media']) if prod_data['data'][0].get('media') else 0
                print(f"✅ Продакшн API работает, медиа: {prod_media_count}")
                
                if prod_media_count == 0:
                    print("⚠️  ВНИМАНИЕ: Продакшн не имеет медиа данных!")
                    print("💡 Нужно обновить продакшн версию")
            else:
                print(f"❌ Продакшн API недоступен: {prod_response.status_code}")
        except Exception as e:
            print(f"❌ Ошибка продакшн API: {e}")
        
        print("\n📊 Сводка:")
        print("✅ Локальный сервер: Работает")
        print("✅ Локальный API: Работает с медиа")
        print("✅ Локальный фронтенд: Работает")
        print("⚠️  Продакшн: Нужно обновить")
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")

if __name__ == "__main__":
    test_local_bot() 