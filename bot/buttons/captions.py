from aiogram.utils.i18n import gettext as _
from aiogram import html

from db.models import AllProduct


async def caption(caption: AllProduct):
    sub = """
\t {id} :  {ID}
\t{title} : {Title}
\t{type} : {Type}
\t{price} : {Price}
\t{quantity} : {Quantity}
\t{description} : {Description}
    """.format(
        id=html.bold(_(' 🆔 ID')),
        ID=caption.id,
        title=html.bold(_('💠 Title')),
        Title=caption.title,
        price=html.bold(_('💸 Price')),
        Price=caption.price,
        quantity=html.bold(_('〽️ Quantity')),
        Quantity=caption.quantity,
        description=html.bold(_('📕 Description')),
        Description=caption.description,
        type=html.bold(_('📦 Type')),
        Type=caption.category.name,

    )
    return sub
