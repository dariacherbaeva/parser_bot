# Тестовое задание

Бот в данной версии запускается только на локальном компьютере (через файл bot.py). 

Для парсинга страниц используется Selenium (был выбран из-за необходимости разрешить использование JavaScript для запуска страницы и нажатия на кнопку, открывающую полный список майнеров) и BeautifulSoup.

Полный список зависимостей содержится в файле requirements.txt.

Для запуска бота необходимо заменить токен и путь к драйверу Selenium в файле config.py. Для начала работы с ботом введите команду /start. Для повторного выбора команды введите ту же команду (не хватило времени настроить получше). Список майнеров выгружается в Excel-таблицу, которую пользователь может скачать. Настроить возможность подписки, к сожалению, не хватило времени.