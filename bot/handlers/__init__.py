from bot.dispatcher import dp
from bot.handlers.main import main_router
from bot.handlers.private.book import book_router
from bot.handlers.private.contact_addresses import ca_router
from bot.handlers.private.language import lang_router
from bot.handlers.private.networks import net_router
from bot.handlers.private.payment import order_router

dp.include_routers(*[
    main_router,
    book_router,
    lang_router,
    net_router,
    ca_router,
    order_router
])
