from aiogram import Router, F
from aiogram.types import Message

order_router=Router()

@order_router.message(F.text=="📃 My Orders")
async def my_orders(message : Message):
    pass
