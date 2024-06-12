from aiogram.types import InlineKeyboardButton, switch_inline_query_chosen_chat
from aiogram.utils.i18n import gettext as _
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy import select
from sqlalchemy.orm import Session

from db.config import engine
from db.models import Category, AllProduct


async def   product_detail_buttons(product: AllProduct, step: int = 1, set: int = None):
    product_id = product.id
    quantity = product.quantity
    ikb = InlineKeyboardBuilder()
    category_id = product.category_id

    buttons = [
        InlineKeyboardButton(text='➖', callback_data=f"info_minus_{product_id}_{step - 1}_{set}"),
        InlineKeyboardButton(text=str(step), callback_data=f'info_{product_id}_{step}'),
        InlineKeyboardButton(text='➕', callback_data=f"info_plus_{product_id}_{step + 1}_{set}"),
        InlineKeyboardButton(text=_('↩️ Back'), callback_data=f'info_back_{product_id}_{set}'),
        InlineKeyboardButton(text=_('🛒 Add to Cart'), callback_data='info_addcart_'),
    ]
    if step == 1:
        buttons.pop(0)
        if step == quantity:
            buttons.pop(1)
    elif step == quantity:
        buttons.pop(2)
    ikb.add(*buttons)
    ikb.adjust(3, 2)
    ikb = ikb.as_markup()
    return ikb


async def categories_buttons(categories: list[Category]):
    ikb = InlineKeyboardBuilder()
    buttons = [InlineKeyboardButton(text=i.name, callback_data=f"category_{i.id}") for i in categories]
    buttons.append(InlineKeyboardButton(text=_('🔍 Search'), switch_inline_query_current_chat=''))
    buttons.append(InlineKeyboardButton(text=_('Return ↩️'),callback_data='category_return'))
    ikb.add(*buttons)
    ikb.adjust(2, repeat=True)
    ikb = ikb.as_markup()
    return ikb


async def products_buttons(length: list[AllProduct], set: int = 2):
    ikb = InlineKeyboardBuilder()
    category_id = length[0].category_id
    buttons = [InlineKeyboardButton(text=str(i + 1), callback_data=f'book_{str(val.id)}_{set}') for i,
    val in enumerate(length)]
    with Session(engine) as s:
        data = list(s.execute(select(AllProduct).where(AllProduct.category_id == category_id)).scalars())
    max_len = len(data)
    ex = [
        InlineKeyboardButton(text='⏪', callback_data=f'book_prev_{category_id}_{set}'),
        InlineKeyboardButton(text=_('⏫ Back'), callback_data='book_back_'),
        InlineKeyboardButton(text="⏩", callback_data=f'book_next_{category_id}_{set}'),
    ]
    print(max_len, set)
    if set <= 2:
        ex.pop(0)
    if max_len <= 6 * (set) or max_len + 1 == 6 * (set + 1):
        ex.pop()
    buttons.extend(ex)
    ikb.add(*buttons)
    ikb.adjust(3, repeat=True)
    ikb = ikb.as_markup()
    return ikb
