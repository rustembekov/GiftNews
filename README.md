# Gift Propaganda News

Современное приложение для агрегации новостей из Telegram каналов.

## 🚀 Быстрый старт

### Frontend
```bash
cd giftpropaganda-frontend
npm install
npm start
```

### Backend
```bash
cd server
pip install -r requirements.txt
python main.py
```

## 🏗️ Архитектура

### Frontend (React + TypeScript)
- **Components**: Переиспользуемые UI компоненты
- **Hooks**: Бизнес-логика и состояние
- **API**: Взаимодействие с сервером
- **Types**: TypeScript типизация

### Backend (FastAPI + SQLAlchemy)
- **API**: REST API роутеры
- **Services**: Бизнес-логика
- **Parsers**: Парсеры новостей
- **Models**: Модели данных

## 📁 Структура проекта

```
├── giftpropaganda-frontend/  # React приложение
├── server/                   # FastAPI сервер
├── scripts/                  # Вспомогательные скрипты
└── migrations/              # Миграции БД
```

## 🔧 Разработка

### Установка зависимостей
```bash
# Frontend
cd giftpropaganda-frontend
npm install

# Backend
cd server
pip install -r requirements.txt
```

### Запуск в режиме разработки
```bash
# Frontend (порт 3000)
cd giftpropaganda-frontend
npm start

# Backend (порт 8000)
cd server
python main.py
```

## 🚀 Деплой

### GitHub Pages (Frontend)
Приложение автоматически деплоится при push в ветку `main`:
- URL: https://rustembekov.github.io/GiftNews/
- GitHub Actions: `.github/workflows/deploy.yml`

### Ручной деплой
```bash
cd giftpropaganda-frontend
npm run deploy
```

## 📱 Telegram Mini App

Приложение интегрировано с Telegram Web App API для использования в качестве мини-приложения.

## 🛠️ Технологии

- **Frontend**: React, TypeScript, Styled Components
- **Backend**: FastAPI, SQLAlchemy, PostgreSQL
- **Парсеры**: RSS, Telegram API
- **Деплой**: GitHub Pages, GitHub Actions 