from aiogram import Router, F,html
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils.i18n import gettext as _, lazy_gettext as __
from sqlalchemy import update, select
from sqlalchemy.orm import Session

from bot.buttons.reply import language_buttons, command_start_buttons
from bot.dispatcher import i18n
from bot.states.states import Next
from db.models import User

lang_router = Router()


@lang_router.message(F.text == __('🇺🇿/🇷🇺/🇺🇲 Language'))
async def language_handler(message: Message, state: FSMContext):
    await message.answer(_('Language ♻️ Switch')
                         , reply_markup=await language_buttons())
    await state.set_state(Next.choose_lang)


@lang_router.message(Next.choose_lang)
async def choose_lang_handler(message: Message, state: FSMContext, session: Session):
    await state.clear()
    user_id = message.from_user.id
    if message.text == __('🇺🇿 Uzbek'):
        query = update(User).where(User.user_id == user_id).values(lang='uz')
        session.execute(query)
        session.commit()
        await state.update_data({'locale': 'uz'})
        i18n.current_locale = 'uz'
        await message.answer(html.bold(_("Selected: 🇺🇿 Uzbek")))

    elif message.text == __('🇷🇺 Russian'):
        await state.update_data({'locale': 'ru'})
        i18n.current_locale = 'ru'
        query = update(User).where(User.user_id == user_id).values(lang='ru')
        session.execute(query)
        session.commit()
        await message.answer(html.bold(_("Selected: 🇷🇺 Russian")))
    elif message.text == __('🇺🇸 English'):
        query = update(User).where(User.user_id == user_id).values(lang='en')
        session.execute(query)
        session.commit()
        await state.update_data({'locale': 'en'})
        i18n.current_locale = 'en'
        await message.answer(html.bold(_("Selected: 🇺🇸 English")))
    func = await command_start_buttons()
    await message.answer(html.bold(_("Main Menu")), reply_markup=func)
    query = select(User.lang).where(User.user_id == user_id)
    lang=session.execute(query).scalar().value
    await state.update_data({'locale':lang})
    i18n.current_locale=lang
