
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

import handlers.keyboard as kb
from create_bot import dp, lilabred_bot
from handlers.text_contacts import contacts
from handlers.text_courses import courses
from handlers.to_fsm import HaircutState


# Приветствие
@dp.message_handler(commands="start")
async def send_welcome(message: types.Message):
    await lilabred_bot.send_message(
        message.from_user.id,
        "Привет! Выбери нужную опцию:",
        reply_markup=kb.first_choice_button,
    )
    await HaircutState.initialize.set()

# Кнопка назад
@dp.message_handler(Text(equals='назад', ignore_case=True), state='*')
async def back(message: types.Message, state: FSMContext):
    current_state = await state.get_state()

    if (current_state in (None, HaircutState.initialize.state)):
        return

    # Возвращаемся к выбору между курсы/контакты/прайс
    if (current_state == HaircutState.haircut.state):
        await lilabred_bot.send_message(
            message.from_user.id,
            "Выбери нужную опцию:",
            reply_markup=kb.first_choice_button,
        )
        await HaircutState.initialize.set()
        return
    
    # Возвращаемся в Прайс
    if (current_state in (HaircutState.afro.state, HaircutState.bred.state, HaircutState.tail.state)):
        await lilabred_bot.send_message(
            message.from_user.id,
            "Какая прическа тебя интересует?",
            reply_markup=kb.price_choice_button,
        )
        await HaircutState.haircut.set()
        return
    
    # Возвращаемся к выбору зоны для афрокосичек
    if (current_state in (HaircutState.afro_full_head.state, HaircutState.afro_undercut.state)):
        await lilabred_bot.send_message(
            message.from_user.id,
            "Выбери зону прически:",
            reply_markup=kb.afro_zone_choice_button,
        )
        await HaircutState.afro.set()
    
    # Возвращаемся к выбору зоны для брейдов
    if (current_state in (HaircutState.bred_full_head.state, HaircutState.bred_undercut.state)):
        await lilabred_bot.send_message(
            message.from_user.id,
            "Выбери зону прически:",
            reply_markup=kb.breds_zone_choice_button,
        )
        await HaircutState.bred.set()
    
    # Возвращаемся к выбору наличия материалов для брейдов на всю голову
    if (current_state in (HaircutState.bred_full_head_with_material.state, HaircutState.bred_full_head_without_material.state)):
        await lilabred_bot.send_message(
            message.from_user.id,
            "Брейды с материалом или без?",
            reply_markup=kb.breds_head_material_button,
        )
        await HaircutState.bred_full_head.set()
    
    # Возвращаемся к выбору наличия материалов для брейдов на макушку
    if (current_state in (HaircutState.bred_undercut_with_material.state, HaircutState.bred_undercut_without_material.state)):
        await lilabred_bot.send_message(
            message.from_user.id,
            "Брейды с материалом или без?",
            reply_markup=kb.breds_undercut_material_button,
        )
        await HaircutState.bred_undercut.set()

# ____________________________________________Выбор опции___________________________________________________________

# Выбираем курсы
@dp.message_handler(Text(equals="курсы", ignore_case=True), state=HaircutState.initialize)
async def course_choice(message: types.Message):
    await lilabred_bot.send_message(
        message.from_user.id,
        f"{courses}",
        reply_markup=kb.first_choice_button,
    )


# Выбираем контакты
@dp.message_handler(Text(equals="контакты", ignore_case=True), state=HaircutState.initialize)
async def contacts_choice(message: types.Message):
    await lilabred_bot.send_message(
        message.from_user.id,
        f"{contacts}",
        reply_markup=kb.first_choice_button,
    )


# Выбираем прайс
@dp.message_handler(Text(equals="прайс", ignore_case=True), state=HaircutState.initialize)
async def price_choice(message: types.Message):
    await lilabred_bot.send_message(
        message.from_user.id,
        "Какая прическа тебя интересует?",
        reply_markup=kb.price_choice_button,
    )
    await HaircutState.haircut.set()

# ____________________________________________Выбран прайс___________________________________________________________

# Опции > Прайс > Выбираем афрокосички - предоставлен выбор зоны
@dp.message_handler(Text(equals="афрокосички точечно", ignore_case=True), state=HaircutState.haircut)
async def afro_zone_choice(message: types.Message):
    await lilabred_bot.send_message(
        message.from_user.id,
        "Выбери зону прически:",
        reply_markup=kb.afro_zone_choice_button,
    )
    await HaircutState.afro.set()


# Опции > Прайс > Выбираем брейды - предоставлен выбор зоны
@dp.message_handler(Text(equals="брейды", ignore_case=True), state=HaircutState.haircut)
async def breds_zone_choice(message: types.Message):
    await lilabred_bot.send_message(
        message.from_user.id,
        "Выбери зону прически:",
        reply_markup=kb.breds_zone_choice_button,
    )
    await HaircutState.bred.set()


# Опции > Прайс > Выбираем афрохвост
@dp.message_handler(Text(equals="афрохвост", ignore_case=True), state=HaircutState.haircut)
async def tail_length_choice(message: types.Message):
    await lilabred_bot.send_message(
        message.from_user.id,
        "Выбери длину афрохвоста:",
        reply_markup=kb.tail_length_button,
    )
    await HaircutState.tail.set()

# ___________________________________________Выбраны афрокосички > выбор зоны______________________________________________________

# Опции > Прайс > Афрокосички точечно > Выбор зоны - Выбираем афрокосички на всю голову - предоставлен выбор толщины
@dp.message_handler(Text(equals="на всю голову", ignore_case=True), state=HaircutState.afro)
async def afro_head_value_choice(message: types.Message):
    await lilabred_bot.send_message(
        message.from_user.id,
        "Выбери толщину/количество косичек:",
        reply_markup=kb.afro_head_thickness_button,
    )
    await HaircutState.afro_full_head.set()


# Опции > Прайс > Афрокосички точечно > Выбор зоны - Выбираем афрокосички на макушку - предоставлен выбор толщины
@dp.message_handler(Text(equals="на андеркат(макушка)", ignore_case=True), state=HaircutState.afro)
async def afro_undercut_value_choice(message: types.Message):
    await lilabred_bot.send_message(
        message.from_user.id,
        "Выбери толщину/количество косичек:",
        reply_markup=kb.afro_undercut_thickness_button,
    )
    await HaircutState.afro_undercut.set()

# ___________________________________________Выбраны афрокосички > зона: на всю голову______________________________________________________


@dp.message_handler(Text(equals="крупные(20-40 шт.)", ignore_case=True), state=HaircutState.afro_full_head)
async def afro_head_big(message: types.Message):
    await lilabred_bot.send_photo(
        chat_id=message.from_user.id,
        photo=open("photos/Afro_head_big.JPG", "rb"),
        caption="Крупные(20-40 шт.) – 16 500 руб.",
    )


@dp.message_handler(Text(equals="толстые(40-60 шт.)", ignore_case=True), state=HaircutState.afro_full_head)
async def afro_head_thick(message: types.Message):
    await lilabred_bot.send_photo(
        chat_id=message.from_user.id,
        photo=open("photos/Afro_head_thick.jpg", "rb"),
        caption="Толстые(40-60 шт.) – 18 500 руб.",
    )


@dp.message_handler(Text(equals="средние(60-80 шт.)", ignore_case=True), state=HaircutState.afro_full_head)
async def afro_head_middle(message: types.Message):
    await lilabred_bot.send_photo(
        chat_id=message.from_user.id,
        photo=open("photos/Afro_head_middle.jpg", "rb"),
        caption="Средние(60-80 шт.) – 20 000 руб.",
    )


@dp.message_handler(Text(equals="мелкие(80-100 шт.)", ignore_case=True), state=HaircutState.afro_full_head)
async def afro_head_small(message: types.Message):
    await lilabred_bot.send_photo(
        chat_id=message.from_user.id,
        photo=open("photos/Afro_head_small.jpg", "rb"),
        caption="Мелкие(80-100 шт.) – 23 500 руб.",
    )


# ___________________________________________Выбраны афрокосички > зона: на макушку______________________________________________________


@dp.message_handler(Text(equals="крупные(10-20 шт.)", ignore_case=True), state=HaircutState.afro_undercut)
async def afro_undercut_big(message: types.Message):
    await lilabred_bot.send_photo(
        chat_id=message.from_user.id,
        photo=open("photos/Afro_undercut_big.jpg", "rb"),
        caption="Крупные(10-20 шт.) – 6 500 руб.",
    )


@dp.message_handler(Text(equals="толстые(30-40 шт.)", ignore_case=True), state=HaircutState.afro_undercut)
async def afro_undercut_thick(message: types.Message):
    await lilabred_bot.send_photo(
        chat_id=message.from_user.id,
        photo=open("photos/Afro_undercut_thick.jpg", "rb"),
        caption="Толстые(30-40 шт.) – 8 500 руб.",
    )


@dp.message_handler(Text(equals="средние(40-60 шт.)", ignore_case=True), state=HaircutState.afro_undercut)
async def afro_undercut_small(message: types.Message):
    await lilabred_bot.send_photo(
        chat_id=message.from_user.id,
        photo=open("photos/Afro_undercut_middle.jpg", "rb"),
        caption="Средние(40-60 шт.) – 10 000 руб.",
    )


# ___________________________________________Выбраны брейды > выбор зоны______________________________________________________

# Опции > Прайс > Брейды > Выбор зоны - предоставлен выбор зоны
@dp.message_handler(Text(equals="вся голова", ignore_case=True), state=HaircutState.bred)
async def breds_head_choice_material(message: types.Message):
    await lilabred_bot.send_message(
        message.from_user.id,
        "Брейды с материалом или без?",
        reply_markup=kb.breds_head_material_button,
    )
    await HaircutState.bred_full_head.set()


# Опции > Прайс > Брейды > Выбор зоны - предоставлен выбор зоны
@dp.message_handler(Text(equals="андеркат(макушка)", ignore_case=True), state=HaircutState.bred)
async def breds_undercut_choice_material(message: types.Message):
    await lilabred_bot.send_message(
        message.from_user.id,
        "Брейды с материалом или без?",
        reply_markup=kb.breds_undercut_material_button,
    )
    await HaircutState.bred_undercut.set()


# ___________________________________________Выбрана зона брейдов: вся голова > материал______________________________________________________


@dp.message_handler(Text(equals="с материалом", ignore_case=True), state=HaircutState.bred_full_head)
async def breds_head_withmat_choice_value(message: types.Message):
    await lilabred_bot.send_message(
        message.from_user.id,
        "Выбери количество брейдов:",
        reply_markup=kb.breds_head_material_thickness_button,
    )
    await HaircutState.bred_full_head_with_material.set()


@dp.message_handler(Text(equals="без материала", ignore_case=True), state=HaircutState.bred_full_head)
async def breds_head_withoutmat_choice_value(message: types.Message):
    await lilabred_bot.send_message(
        message.from_user.id,
        "Выбери количество брейдов:",
        reply_markup=kb.breds_head_thickness_button,
    )
    await HaircutState.bred_full_head_without_material.set()


# ___________________________________________Выбрана зона брейдов: андеркат > материал______________________________________________________


@dp.message_handler(Text(equals="с материалом", ignore_case=True), state=HaircutState.bred_undercut)
async def breds_zone_choice(message: types.Message):
    await lilabred_bot.send_message(
        message.from_user.id,
        "Выбери количество брейдов:",
        reply_markup=kb.breds_undercut_material_thickness_button,
    )
    await HaircutState.bred_undercut_with_material.set()


@dp.message_handler(Text(equals="без материала", ignore_case=True), state=HaircutState.bred_undercut)
async def breds_zone_choice(message: types.Message):
    await lilabred_bot.send_message(
        message.from_user.id,
        "Выбери количество брейдов:",
        reply_markup=kb.breds_undercut_thickness_button,
    )
    await HaircutState.bred_undercut_without_material.set()

# ___________________________________________Выбрана зона брейдов: вся голова > с материалом > выбор кол-ва брейдов______________________________________________________


@dp.message_handler(
    Text(equals="2-4 шт.", ignore_case=True),
    state=[HaircutState.bred_full_head, HaircutState.bred_full_head_with_material],
)
async def breds_head_material_middle(message: types.Message):
    await lilabred_bot.send_photo(
        chat_id=message.from_user.id,
        photo=open("photos/Breds_head_materials_middle.jpg", "rb"),
        caption="Брейды: 2-4 шт. – 4 500 руб.",
    )


@dp.message_handler(
    Text(equals="5-7 шт.", ignore_case=True),
    state=[HaircutState.bred_full_head, HaircutState.bred_full_head_with_material],
)
async def breds_head_material_thick(message: types.Message):
    await lilabred_bot.send_photo(
        chat_id=message.from_user.id,
        photo=open("photos/Breds_head_materials_thick.jpg", "rb"),
        caption="Брейды: 5-7 шт. – 6 500 руб.",
    )


@dp.message_handler(
    Text(equals="8-10 шт.", ignore_case=True),
    state=[HaircutState.bred_full_head, HaircutState.bred_full_head_with_material],
)
async def breds_head_material_big(message: types.Message):
    await lilabred_bot.send_photo(
        chat_id=message.from_user.id,
        photo=open("photos/Breds_head_materials_big.jpg", "rb"),
        caption="Брейды: 8-10 шт. – 7 500 руб.",
    )


# ___________________________________________Выбрана зона брейдов: вся голова > без материалов > выбор кол-ва брейдов______________________________________________________


@dp.message_handler(
    Text(equals="2-4 шт.", ignore_case=True),
    state=[HaircutState.bred_full_head, HaircutState.bred_full_head_without_material],
)
async def breds_head_1(message: types.Message):
    await lilabred_bot.send_message(message.from_user.id, "2 000 руб.")  # НУЖНО ФОТО


@dp.message_handler(
    Text(equals="5-7 шт.", ignore_case=True),
    state=[HaircutState.bred_full_head, HaircutState.bred_full_head_without_material],
)
async def breds_head_2(message: types.Message):
    await lilabred_bot.send_photo(
        chat_id=message.from_user.id,
        photo=open("photos/Breds_head_thick.jpg", "rb"),
        caption="Брейды: 5-7 шт. – 4 500 руб.",
    )


@dp.message_handler(
    Text(equals="8-10 шт.", ignore_case=True),
    state=[HaircutState.bred_full_head, HaircutState.bred_full_head_without_material],
)
async def breds_head_3(message: types.Message):
    await lilabred_bot.send_message(message.from_user.id, "6 000 руб.")  # НУЖНО ФОТО


# ___________________________________________Выбраны зоны брейдов: андеркат > с материалом > выбор кол-ва брейдов______________________________________________________


@dp.message_handler(
    Text(equals="2-4 шт.", ignore_case=True),
    state=[HaircutState.bred_undercut, HaircutState.bred_undercut_with_material],
)
async def breds_undercut_material_1(message: types.Message):
    await lilabred_bot.send_message(message.from_user.id, "3 500 руб.")  # НУЖНО ФОТО


@dp.message_handler(
    Text(equals="5-7 шт.", ignore_case=True),
    state=[HaircutState.bred_undercut, HaircutState.bred_undercut_with_material],
)
async def breds_undercut_material_2(message: types.Message):
    await lilabred_bot.send_message(message.from_user.id, "4 500 руб.")  # НУЖНО ФОТО


@dp.message_handler(
    Text(equals="8-10 шт.", ignore_case=True),
    state=[HaircutState.bred_undercut, HaircutState.bred_undercut_with_material],
)
async def breds_undercut_material_3(message: types.Message):
    await lilabred_bot.send_message(message.from_user.id, "5 500 руб.")  # НУЖНО ФОТО


# ___________________________________________Выбраны зоны брейдов: андеркат > без материалов > выбор кол-ва брейдов______________________________________________________


@dp.message_handler(
    Text(equals="2-4 шт.", ignore_case=True),
    state=[HaircutState.bred_undercut, HaircutState.bred_undercut_without_material],
)
async def breds_undercut_1(message: types.Message):
    await lilabred_bot.send_message(message.from_user.id, "2 500 руб.")  # НУЖНО ФОТО


@dp.message_handler(
    Text(equals="5-7 шт.", ignore_case=True),
    state=[HaircutState.bred_undercut, HaircutState.bred_undercut_without_material],
)
async def breds_undercut_2(message: types.Message):
    await lilabred_bot.send_message(message.from_user.id, "3 500 руб.")  # НУЖНО ФОТО


@dp.message_handler(
    Text(equals="8-10 шт.", ignore_case=True),
    state=[HaircutState.bred_undercut, HaircutState.bred_undercut_without_material],
)
async def breds_undercut_3(message: types.Message):
    await lilabred_bot.send_message(message.from_user.id, "4 500 руб.")  # НУЖНО ФОТО


# ___________________________________________Выбран афрохвост > выбор длины______________________________________________________


# Опции > Прайс > Афрохвост > Выбор длины - длинный хвост
@dp.message_handler(Text(equals="длинный хвост(75-80 см.)", ignore_case=True), state=HaircutState.tail)
async def tail_lenght_long(message: types.Message):
    await lilabred_bot.send_message(message.from_user.id, "5 000 руб.")  # НУЖНО ФОТО


# Опции > Прайс > Афрохвост > Выбор длины - средний хвост
@dp.message_handler(Text(equals="средний хвост(55-60 см.)", ignore_case=True), state=HaircutState.tail)
async def tail_lenght_middle(message: types.Message):
    await lilabred_bot.send_message(message.from_user.id, "4 000 руб.")  # НУЖНО ФОТО


# Опции > Прайс > Афрохвост > Выбор длины - короткий хвост
@dp.message_handler(Text(equals="короткий хвост(40-45 см.)", ignore_case=True), state=HaircutState.tail)
async def tail_lenght_short(message: types.Message):
    await lilabred_bot.send_message(message.from_user.id, "3 000 руб.")  # НУЖНО ФОТО


# ___________________________________________UNKNOWN_MESSAGE______________________________________________________


@dp.message_handler(content_types=types.ContentType.ANY)
async def unknown_message(message: types.Message):
    await lilabred_bot.send_message(
        message.from_user.id,
        "Я не понимаю это сообщение. Введи:\nПрайс - если хочешь узнать прайс по прическам,\nКурсы - если хочешь узнать информацию о курсах,\nКонтакты - и я покажу тебе как связаться с LilaBred.\n/start - и мы начнем общение заново.",
    )


# ___________________________________________CANCEL______________________________________________________


@dp.message_handler(state="*", commands="cancel")
@dp.message_handler(Text(equals="cancel", ignore_case=True), state="*")
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply("Отмена.", reply_markup=types.ReplyKeyboardRemove())