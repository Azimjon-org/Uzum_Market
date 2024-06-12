from typing import Dict, Any

import uvicorn
from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.requests import Request
from starlette_admin.contrib.sqla import Admin, ModelView

from db.config import engine
from db.models import User, AllProduct, Network, Category, ContactAddress
from web.provider import UsernameAndPasswordProvider
from starlette.middleware.sessions import SessionMiddleware

middleware = [
    Middleware(SessionMiddleware, secret_key=None)
]

app = Starlette(middleware=middleware)

logo_url = 'https://fiverr-res.cloudinary.com/images/q_auto,f_auto/gigs/346993714/original/d524eed3a6df4f37fe7e5f81d4c717b601117736/do-telegram-bot-with-python-aiogram.png'
admin = Admin(
    engine=engine,
    title="Aiogram Web Admin",
    logo_url=logo_url,
    auth_provider=UsernameAndPasswordProvider(),
    middlewares=middleware
)


class CategoryCustomView(ModelView):
    exclude_fields_from_create = ('created_at', 'updated_at' , 'books')


class BookCustomView(ModelView):
    exclude_fields_from_create = ('created_at', 'updated_at' , 'order_items')

    async def create(self, request: Request, data: Dict[str, Any]) -> Any:
        print(data)
        return await super().create(request, data)



admin.add_view(ModelView(User))
admin.add_view(ModelView(AllProduct))
admin.add_view(ModelView(Category))
admin.add_view(ModelView(Network))
admin.add_view(ModelView(ContactAddress))


# Mount admin to your app
admin.mount_to(app)

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8080)
