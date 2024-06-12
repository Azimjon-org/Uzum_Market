from aiogram import Router, F,html
from aiogram.types import Message
from aiogram.utils.i18n import lazy_gettext as __
from aiogram.utils.i18n import gettext as _
from sqlalchemy import select
from sqlalchemy.orm import Session

from bot.buttons.reply import command_start_buttons
from db.models import Network

net_router = Router()


@net_router.message(F.text == __('📲  Our Social Network  🌐'))
async def network_handler(message: Message, session: Session):
    data: list[Network] = list(session.execute(select(Network)).scalars())
    count=0
    name = f""""""
    for i in data:
        if i.images:
            image=i.images
        count+=1
        if i.name.startswith('Uzum'):
          url = "{} : {}".format(html.bold(_('Our website')) ,f"<a href='{i.url}'><b>{i.name}</b></a>\n")
        elif count>=2:
          url = f"|\t<a href='{i.url}'><b>{i.name}</b></a>\t|\t"
        name += url
        if count==len(data):
            func = await command_start_buttons()
            await message.answer_photo(image, caption=f"""{name}""",reply_markup=func)