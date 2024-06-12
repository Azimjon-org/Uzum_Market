from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.utils.i18n import gettext as _
from aiogram.utils.i18n import lazy_gettext as __


async def language_buttons():
    rkb = ReplyKeyboardBuilder()
    rkb.add(*[
        KeyboardButton(text=_('🇺🇿 Uzbek')),
        KeyboardButton(text=_('🇷🇺 Russian')),
        KeyboardButton(text=_('🇺🇸 English')),
        KeyboardButton(text=_('🔂 Back')),
    ])
    rkb.adjust(2, 1, 1)
    rkb = rkb.as_markup(resize_keyboard=True)
    return rkb


async def command_start_buttons():
    design = [
        [
            KeyboardButton(text=_("🏬 Goods|Products 🏪"))
        ],
        [
            KeyboardButton(text=_("📃 My Orders"))
        ],
        [
            KeyboardButton(text=_("📲  Our Social Network  🌐")),
            KeyboardButton(text=_("📞 ☎️ Contact Us"))
        ],
        [
            KeyboardButton(text=_("🇺🇿/🇷🇺/🇺🇲 Language"))
        ]
    ]
    rkm = ReplyKeyboardMarkup(keyboard=design, resize_keyboard=True, one_time_keyboard=True)
    return rkm
