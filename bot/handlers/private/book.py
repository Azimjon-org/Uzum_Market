from aiogram import Router, F, html
from aiogram.types import Message, CallbackQuery, InputMediaPhoto, ReplyKeyboardRemove, InlineQueryResultArticle, \
    InputTextMessageContent, InlineQuery
from aiogram.utils.i18n import lazy_gettext as __
from aiogram.utils.i18n import gettext as _
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.sql.operators import ilike_op

from bot.buttons.captions import caption
from bot.buttons.inline import categories_buttons, products_buttons, product_detail_buttons
from bot.buttons.reply import command_start_buttons
from bot.dispatcher import dp
from db.config import engine
from db.models import Category, AllProduct

book_router = Router()


@book_router.message(F.text == __('🏬 Goods|Products 🏪'))
async def books_handler(message: Message, session: Session):
    query = select(Category)
    res = list(session.execute(query).scalars())
    func = await categories_buttons(res)
    # await message.delete_reply_markup()
    # await message.answer(html.bold(_("🟢\t\t Products Section \t\t🏪\t : ")), reply_markup=ReplyKeyboardRemove())
    await message.answer_photo('https://telegra.ph/file/4d236a6b4ddb3e26a357a.png', html.bold(
        _('🟢\t\t Products Section \t\t🏪\t : \n\n🟢 \t\tChoose one of the Categories : '))
                               , reply_markup=func)


@book_router.callback_query(F.data.startswith('category_'))
async def products_handler(callback: CallbackQuery, session: Session):
    if callback.data.split('_')[1] == 'return':
        func = await command_start_buttons()
        await callback.message.delete()
        await callback.message.answer(html.bold(_("Main Menu")), reply_markup=func)

    else:
        category_id = callback.data.split('_')[1]
        books: list[AllProduct] = list(session.execute(
            select(AllProduct).where(AllProduct.category_id == category_id).offset(6).limit(6)).scalars())
        res = "{}    {}".format(html.bold(_("""Results from 1-6 """)), (html.bold(books[0].category.name + '\n')))
        for i, val in enumerate(books):
            res += '{}.\t🆔 {} ꡶ {} = {}💸  \n'.format(html.bold(str(i + 1)), val.id, val.title, val.price)
        func = await products_buttons(books)
        await callback.message.edit_media(
            media=InputMediaPhoto(media='https://telegra.ph/file/e6389851bd6697cbaccf0.png', caption=res),
            reply_markup=func)


@book_router.inline_query()
async def search_button_handler(query: InlineQuery, session: Session):
    goods: list[AllProduct] = list(session.execute(select(AllProduct).where(ilike_op(AllProduct.title,f'%{query.query.lower()}%'))).scalars())
    res = []
    # filter=[]
    # for i in goods:
    #     if query.query.lower() in i.title.lower():
    #         filter.append(i)
    for i in goods:
        if len(res)==50:
            break
        res.append(InlineQueryResultArticle(
            id=str(i.id),
            title=i.title,
            description=f"""Price : {i.price}
            Quantity : {i.quantity}""",
            thumbnail_url=i.images,
            input_message_content=InputTextMessageContent(message_text=i.title)
        )
        )
    await query.answer(res)


@book_router.callback_query(F.data.startswith('book_'))
async def choose_product_handler(callback: CallbackQuery, session: Session):
    slice = callback.data.split('_')
    if slice[1] == 'back':
        res = list(session.execute(select(Category)).scalars())
        await callback.message.edit_media(
            media=InputMediaPhoto(media="https://telegra.ph/file/4d236a6b4ddb3e26a357a.png",
                                  caption=html.bold(_('🟢 \t\tChoose one of the Categories : ')))
            , reply_markup=await categories_buttons(res))

    elif slice[1] == 'next':
        category_id = int(slice[2])
        step = int(slice[3])
        step += 1
        books: list[AllProduct] = list(session.execute(
            select(AllProduct).where(AllProduct.category_id == category_id).offset((step - 1) * 6).limit(6)).scalars())
        res = "{}    {}".format(html.bold(_("""Results from 1-6 """)), (html.bold(books[0].category.name + '\n')))
        for i, val in enumerate(books):
            res += '{}.\t🆔 {} ꡶ {} = {}💸  \n'.format(html.bold(str(i + 1)), val.id, val.title, val.price)
        print(books)
        func = await products_buttons(books, step)
        await callback.message.edit_media(
            media=InputMediaPhoto(media='https://telegra.ph/file/e6389851bd6697cbaccf0.png', caption=res),
            reply_markup=func)
    elif slice[1] == 'prev':
        category_id = int(slice[2])
        step = int(slice[3])
        step -= 1
        books: list[AllProduct] = list(session.execute(
            select(AllProduct).where(AllProduct.category_id == category_id).offset((step - 1) * 6).limit(6)).scalars())
        res = "{}    {}".format(html.bold(_("""Results from 1-6 """)), (html.bold(books[0].category.name + '\n')))
        for i, val in enumerate(books):
            res += '{}.\t🆔 {} ꡶ {} = {}💸  \n'.format(html.bold(str(i + 1)), val.id, val.title, val.price)
        print(books)
        func = await products_buttons(books, step)
        await callback.message.edit_media(
            media=InputMediaPhoto(media='https://telegra.ph/file/e6389851bd6697cbaccf0.png', caption=res),
            reply_markup=func)
    else:
        set = int(slice[2])
        product_id = int(slice[1])
        product: AllProduct = session.execute(select(AllProduct).where(AllProduct.id == product_id)).scalar()
        # await callback.message.answer_photo(product.images,
        #                                     caption=await caption(product),
        #                                     reply_markup=await product_detail_buttons())
        await callback.message.edit_media(
            media=InputMediaPhoto(media=product.images, caption=await caption(product)),
            reply_markup=await product_detail_buttons(product, set=set))


@book_router.callback_query(F.data.startswith('info'))
async def product_info_counter(callback: CallbackQuery, session: Session):
    slice = callback.data.split('_')
    if slice[1] == 'back':
        product_id = slice[2]
        category_id = session.execute(select(AllProduct.category_id).where(AllProduct.id == product_id)).scalar()
        # print(category_id,type(category_id))
        step = int(slice[3])

        books: list[AllProduct] = list(session.execute(
            select(AllProduct).where(AllProduct.category_id == category_id).offset((step - 1) * 6).limit(6)).scalars())
        res = "{}    {}".format(html.bold(_("""Results from 1-6 """)), (html.bold(books[0].category.name + '\n')))
        for i, val in enumerate(books):
            res += '{}.\t🆔 {} ꡶ {} = {}💸  \n'.format(html.bold(str(i + 1)), val.id, val.title, val.price)
        print(books)
        func = await products_buttons(books, step)
        await callback.message.edit_media(
            media=InputMediaPhoto(media='https://telegra.ph/file/e6389851bd6697cbaccf0.png', caption=res),
            reply_markup=func)

    elif slice[1] == 'minus':
        set = int(slice[4])
        step = int(slice[3])
        product_id = slice[2]
        product: AllProduct = session.execute(select(AllProduct).where(AllProduct.id == product_id)).scalar()
        await callback.message.edit_media(InputMediaPhoto(media=product.images,
                                                          caption=await caption(product)),
                                          reply_markup=await product_detail_buttons(product, step, set))
    elif slice[1] == 'plus':
        set = int(slice[4])
        step = int(slice[3])
        # category_id = slice[2]
        product_id = slice[2]
        product: AllProduct = session.execute(select(AllProduct).where(AllProduct.id == product_id)).scalar()
        await callback.message.edit_media(
            media=InputMediaPhoto(media=product.images, caption=await caption(product)),
            reply_markup=await product_detail_buttons(product, step, set))
