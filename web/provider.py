from os import getenv

from dotenv import load_dotenv
from starlette.requests import Request
from starlette.responses import Response
from starlette_admin.auth import AdminConfig, AdminUser, AuthProvider
from starlette_admin.exceptions import FormValidationError, LoginFailed

from web.hasher import Secure

load_dotenv()


class UsernameAndPasswordProvider(AuthProvider):
    async def login(
            self,
            username: str,
            password: str,
            remember_me: bool,
            request: Request,
            response: Response,
    ) -> Response:
        if len(username) < 3:
            raise FormValidationError({"username": "Ensure username has at least 03 characters"})

        if username == getenv('WEB_USERNAME') and Secure().decoder(password):
            request.session.update({"username": username})
            return response

        raise LoginFailed("Invalid username or password")

    async def is_authenticated(self, request) -> bool:
        if request.session.get('username', None) == getenv('WEB_USERNAME'):
            request.state.user = getenv('WEB_USERNAME')
            return True
        return False

    def get_admin_config(self, request: Request) -> AdminConfig:
        return AdminConfig(
            app_title='Admin page'
        )

    def get_admin_user(self, request: Request) -> AdminUser:
        user = request.state.user
        return AdminUser(username=user)

    async def logout(self, request: Request, response: Response) -> Response:
        request.session.clear()
        return response
