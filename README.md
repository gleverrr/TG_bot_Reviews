# Telegram Бот для оставления отзывов

Этот Telegram бот написан на Python 3.11.2 с использованием библиотеки aiogram 3. Бот позволяет пользователям оставлять отзывы, которые сохраняются в базе данных PostgreSQL. В отзыве может быть текст, видео, фотографии, а также время, через которое отзыв будет опубликован.

Фото и видео удобно хранятся в отдельной папке `uploads`, расположенной внутри основной папки проекта. Бот предоставляет возможность оставить отзыв на товары, привязанные к пользователю и его `telegram_id`, если для этих товаров еще нет отзывов.

**Примечание**: Все хендлеры прописаны прямо в файле `bot.py` по странным предпочтениям заказчика, а не в отдельной папке `handlers`. 😳

## Инструкции по запуску:

1. Создайте файл `.env` на основе примера из `.env.example.txt`.
2. Установите зависимости:
    ```bash
    pip install -r requirements.txt
    ```
3. Запустите бота:
    ```bash
    python bot.py
    ```

## Требования:
- Python 3.11.2
- PostgreSQL
--------------
# Telegram Bot for Reviews

This Telegram bot is written in Python 3.11.2 using the aiogram 3 library. The bot allows users to leave reviews, which are stored in a PostgreSQL database. The review can include text, video, photos, and the time at which the review should be posted.

Photos and videos are conveniently stored in a separate `uploads` folder inside the main project directory. The bot allows users to leave reviews for products associated with their `telegram_id`, provided that no review has been left for those products yet.

**Note**: All handlers are written directly in the `bot.py` file due to the customer's strange preferences, instead of in a separate `handlers` folder. 😳

## Instructions for Running:

1. Create a `.env` file based on the example in `.env.example.txt`.
2. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3. Run the bot:
    ```bash
    python bot.py
    ```

## Requirements:
- Python 3.11.2
- PostgreSQL
