// Тест для проверки данных фронтенда
async function testFrontendData() {
    try {
        console.log('🔍 Тестирование данных фронтенда...');
        
        // Получаем данные из API
        const response = await fetch('http://localhost:8000/api/news/?limit=5');
        const data = await response.json();
        
        console.log('✅ Получено новостей:', data.data.length);
        
        // Проверяем медиа в каждой новости
        data.data.forEach((item, index) => {
            const media = item.media || [];
            console.log(`📰 Новость #${index + 1} (ID: ${item.id}):`);
            console.log(`   Заголовок: ${item.title.substring(0, 50)}...`);
            console.log(`   Источник: ${item.source_name}`);
            console.log(`   Медиа: ${media.length} элементов`);
            
            if (media.length > 0) {
                media.forEach((mediaItem, mediaIndex) => {
                    console.log(`     ${mediaIndex + 1}. Тип: ${mediaItem.type}`);
                    console.log(`        URL: ${mediaItem.url}`);
                    if (mediaItem.thumbnail) {
                        console.log(`        Thumbnail: ${mediaItem.thumbnail}`);
                    }
                });
            } else {
                console.log('     ❌ Нет медиа');
            }
            console.log('');
        });
        
        // Проверяем фронтенд
        console.log('🌐 Проверка фронтенда...');
        try {
            const frontendResponse = await fetch('http://localhost:3000');
            if (frontendResponse.ok) {
                console.log('✅ Фронтенд доступен');
            } else {
                console.log('❌ Фронтенд недоступен');
            }
        } catch (error) {
            console.log('❌ Фронтенд не запущен');
        }
        
    } catch (error) {
        console.error('❌ Ошибка:', error);
    }
}

// Запускаем тест
testFrontendData(); 