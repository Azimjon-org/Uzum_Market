from aiogram import Router, F
from aiogram.types import Message
from aiogram.utils.i18n import gettext as _
from aiogram.utils.i18n import lazy_gettext as __
from sqlalchemy import select
from sqlalchemy.orm import Session

from db.models import ContactAddress

ca_router = Router()


@ca_router.message(F.text == __("📞 ☎️ Contact Us"))
async def contact_address_handler(m: Message, session: Session):
    data: list[ContactAddress] = list(session.execute(select(ContactAddress)).scalars())
    for i in data:
        cation=f"""{i.address}\n\n{i.contact}"""
        await m.answer_photo(i.image,caption=cation)
