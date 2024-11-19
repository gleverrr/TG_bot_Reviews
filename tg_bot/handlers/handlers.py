from config import Config
from datetime import datetime, timedelta
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, Message
from tg_bot.keyboards import (
    get_keyboard_photo,
    get_keyboard_photo2,
    get_keyboard_video,
    get_keyboard_confirm,
)
from tg_bot.states import ReviewStates
from aiogram.fsm.context import FSMContext
from tg_bot.misc import filling_bd_handler
from tg_bot.models import get_db_session, get_user_class, get_order_class


async def start_add_review(message: Message, state: FSMContext):
    user_id = str(message.from_user.id)
    User = get_user_class()
    session = get_db_session()
    account = session.query(User).filter(User.tg == user_id).first()
    session.close()
    if account:
        db_user_id = account.id
        await state.update_data(db_user_id=db_user_id)
        session = get_db_session()
        Order = get_order_class()
        articles = (
            session.query(Order)
            .filter(
                (Order.buyer_id == db_user_id)
                & (Order.marketplace == "WB")
                & (Order.status == 5)
            )
            .distinct(Order.article)
            .all()
        )
        session.close()
        accept_articles = []
        buttons = []
        row = []
        for artic in articles:
            accept_articles.append(artic.article)
            row.append(KeyboardButton(text=str(artic.article)))
            if len(row) == 2:
                buttons.append(row)
                row = []

        if row:
            buttons.append(row)
        articles_keyboard = ReplyKeyboardMarkup(
            keyboard=buttons, resize_keyboard=True, one_time_keyboard=True
        )
        await state.update_data(
            articles_keyboard=articles_keyboard, accept_articles=accept_articles
        )
        await message.answer("Выберите артикул:", reply_markup=articles_keyboard)
        await state.set_state(ReviewStates.article)
    else:
        await message.answer(
            "Кажется, у вас нет товаров, на которые можно оставить отзыв"
        )


async def get_article_message(message: Message, state: FSMContext):
    try:
        data = await state.get_data()
        accept_articles = data.get("accept_articles")
        chosen_article = int(message.text)
        if chosen_article in accept_articles:
            db_user_id = data.get("db_user_id")
            session = get_db_session()
            Order = get_order_class()
            change_order = (
                session.query(Order)
                .filter(
                    (Order.article == chosen_article)
                    & (Order.buyer_id == db_user_id)
                    & (Order.marketplace == "WB")
                    & (Order.status == 5)
                )
                .distinct(Order.article)
                .first()
            )
            session.close()
            await message.answer(
                "Загрузите фотографии (до 2 штук)", reply_markup=get_keyboard_photo()
            )
            await state.update_data(order_id=change_order.id)
            await state.set_state(ReviewStates.waiting_for_photos)
        else:
            data = await state.get_data()
            articles_keyboard = data.get("articles_keyboard")
            await message.answer(
                "Выберите корректный артикул", reply_markup=articles_keyboard
            )
    except ValueError:
        data = await state.get_data()
        articles_keyboard = data.get("articles_keyboard")
        await message.answer(
            "Выберите корректный артикул", reply_markup=articles_keyboard
        )


async def photo_handler(message: types.Message, state: FSMContext):
    if message.photo:
        await state.update_data(mess_ph1=message, is_ph1=True)
        await message.answer(
            "Загрузите вторую фотографию", reply_markup=get_keyboard_photo2()
        )
        await state.set_state(ReviewStates.waiting_for_photo2)

    elif message.text == "Не хочу загружать фото":
        await message.answer("Загрузите видео", reply_markup=get_keyboard_video())

        await state.update_data(is_ph1=False)
        await state.set_state(ReviewStates.waiting_for_video)
    else:
        await message.answer(
            "Загрузите фотографию или напишите 'Не хочу загружать фото'",
            reply_markup=get_keyboard_photo(),
        )


async def photo2_handler(message: types.Message, state: FSMContext):
    if message.photo:
        await state.update_data(mess_ph2=message, is_ph2=True)
        await message.answer("Загрузите видео", reply_markup=get_keyboard_video())
        await state.set_state(ReviewStates.waiting_for_video)
    elif message.text == "Не хочу загружать второе фото":
        await message.answer("Загрузите видео", reply_markup=get_keyboard_video())
        await state.update_data(is_ph2=False)
        await state.set_state(ReviewStates.waiting_for_video)
    else:
        await message.answer(
            "Загрузите фотографию или напишите 'Не хочу загружать второе фото'",
            reply_markup=get_keyboard_photo2(),
        )


async def video_handler(message: types.Message, state: FSMContext):
    if message.video:
        await state.update_data(mess_video=message, is_video=True)
        await message.answer(
            "Введите текст вашео отзыва", reply_markup=types.ReplyKeyboardRemove()
        )
        await state.set_state(ReviewStates.waiting_for_text)
    elif message.text == "Не хочу загружать видео":
        await state.update_data(is_video=False)
        await message.answer(
            "Введите текст вашео отзыва", reply_markup=types.ReplyKeyboardRemove()
        )
        await state.set_state(ReviewStates.waiting_for_text)
    else:
        await message.answer(
            "Загрузите видео или напишите 'Не хочу загружать видео'",
            reply_markup=get_keyboard_video(),
        )


async def text_handler(message: types.Message, state: FSMContext):
    if not (message.text):
        await message.answer("Введите текст", reply_markup=types.ReplyKeyboardRemove())
        return
    if len(message.text) > 1023:
        await message.answer(
            "Текст слишком длинный, должен быть до 1023 символов",
            reply_markup=types.ReplyKeyboardRemove(),
        )
        return
    await state.update_data(review_text=message.text)
    await message.answer(
        "Введите время (в минутах), через которое опубликовать отзыв",
        reply_markup=types.ReplyKeyboardRemove(),
    )
    await state.set_state(ReviewStates.waiting_for_time)


async def time_handler(message: types.Message, state: FSMContext):
    text = message.text
    try:
        t_int = int(text)
    except:
        await message.answer(
            "Введите только число!", reply_markup=types.ReplyKeyboardRemove()
        )
        return
    new_t = datetime.now() + timedelta(minutes=t_int)
    await state.update_data(time_public=new_t)
    await message.answer(
        "Вы уверены, что хотите оставить этот отзыв?",
        reply_markup=get_keyboard_confirm(),
    )
    await state.set_state(ReviewStates.confirmation)


async def confirmation_handler(message: types.Message, state: FSMContext, bot: Bot):
    if message.text == "Да":
        await message.answer(
            "Хорошо! Ваш отзыв успешно сохранен",
            reply_markup=types.ReplyKeyboardRemove(),
        )
        BOT_TOKEN = Config.BOT_TOKEN
        await filling_bd_handler(state, bot, BOT_TOKEN)
        await state.clear()
    elif message.text == "Хочу отменить этот отзыв":
        await message.answer(
            "Ваш отзыв не будет отправлен", reply_markup=types.ReplyKeyboardRemove()
        )
        await state.clear()
    else:
        await message.answer(
            "Напшите 'да' или 'Хочу отменить этот отзыв'",
            reply_markup=get_keyboard_confirm(),
        )


async def echo_message(message: types.Message):
    await message.answer("Для начала работы бота используйте команду /start")


def register_handlers(dp: Dispatcher, bot: Bot):
    dp.message.register(start_add_review, Command("start"))
    dp.message.register(get_article_message, ReviewStates.article)
    dp.message.register(photo_handler, ReviewStates.waiting_for_photos)
    dp.message.register(photo2_handler, ReviewStates.waiting_for_photo2)
    dp.message.register(video_handler, ReviewStates.waiting_for_video)
    dp.message.register(text_handler, ReviewStates.waiting_for_text)
    dp.message.register(time_handler, ReviewStates.waiting_for_time)
    dp.message.register(confirmation_handler, ReviewStates.confirmation)
    dp.message.register(echo_message)
