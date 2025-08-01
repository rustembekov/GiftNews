# Gift Propaganda Mini App

Telegram Mini App для новостей о подарках, криптовалютах и NFT.

## 🚀 Деплой на GitHub Pages

### 1. Подготовка репозитория

1. Создайте новый репозиторий на GitHub:
   ```
   https://github.com/your-username/giftpropaganda-mini-app
   ```

2. Обновите `homepage` в `package.json`:
   ```json
   "homepage": "https://your-username.github.io/giftpropaganda-mini-app"
   ```

### 2. Установка зависимостей

```bash
npm install
npm install --save-dev gh-pages
```

### 3. Деплой

```bash
# Сборка и деплой
npm run deploy
```

### 4. Настройка GitHub Pages

1. Перейдите в Settings репозитория
2. В разделе "Pages" выберите:
   - Source: "Deploy from a branch"
   - Branch: "gh-pages"
   - Folder: "/ (root)"

### 5. Получение ссылки

После деплоя ваше приложение будет доступно по адресу:
```
https://your-username.github.io/giftpropaganda-mini-app
```

## 🔧 Альтернативные варианты деплоя

### Vercel (Рекомендуется)

1. Установите Vercel CLI:
   ```bash
   npm install -g vercel
   ```

2. Деплой:
   ```bash
   vercel
   ```

### Netlify

1. Создайте аккаунт на Netlify
2. Подключите GitHub репозиторий
3. Настройте:
   - Build command: `npm run build`
   - Publish directory: `build`

## 📱 Настройка Telegram Bot

### 1. Создание бота

1. Напишите @BotFather в Telegram
2. Создайте нового бота: `/newbot`
3. Получите токен бота

### 2. Настройка Mini App

1. Отправьте @BotFather команду `/newapp`
2. Выберите вашего бота
3. Укажите название Mini App
4. Добавьте ссылку на деплой:
   ```
   https://your-username.github.io/giftpropaganda-mini-app
   ```

### 3. Получение ссылки Mini App

После настройки вы получите ссылку вида:
```
https://t.me/your_bot_name/giftpropaganda
```

## 🔗 Полезные ссылки

- [Telegram Mini Apps Documentation](https://core.telegram.org/bots/webapps)
- [GitHub Pages](https://pages.github.com/)
- [Vercel](https://vercel.com/)
- [Netlify](https://netlify.com/)

## 📝 Структура проекта

```
src/
├── components/          # React компоненты
├── hooks/              # Custom hooks
├── api/                # API интеграция
├── types/              # TypeScript типы
├── utils/              # Утилиты
├── constants/          # Константы
└── telegram/           # Telegram Web App интеграция
```

## 🛠 Разработка

```bash
# Установка зависимостей
npm install

# Запуск в режиме разработки
npm start

# Сборка для продакшена
npm run build

# Деплой
npm run deploy
```

## 📄 Лицензия

MIT License
