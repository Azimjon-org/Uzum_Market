from aiogram import Router, html
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, BotCommand
from aiogram.utils.i18n import gettext as _
from sqlalchemy import select, insert
from sqlalchemy.orm import Session

from bot.buttons.reply import command_start_buttons, command_start_buttons
from bot.dispatcher import dp, i18n
from db.models import User

main_router = Router()


@main_router.message(CommandStart())
async def command_start_handler(message: Message, session: Session, state: FSMContext) -> None:
    user = {
        'user_id': message.from_user.id,
        'first_name': message.from_user.first_name,
        'last_name': message.from_user.last_name,
        'username': message.from_user.username,
    }
    query = select(User).where(User.user_id == message.from_user.id)
    res: User = session.execute(query).scalar()
    if not res:
        session.execute(insert(User).values(**user))
        session.commit()
    if res:
        lang = res.lang.value
        await state.update_data({'locale': lang})
        i18n.current_locale = lang
    func = await command_start_buttons()
    await message.answer("{} , {}".format(_("Hello"), html.bold(message.from_user.full_name)), reply_markup=func)
    await message.bot.set_my_commands([
        BotCommand(command='start', description='start the bot')
    ])
