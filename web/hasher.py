from os import getenv

import bcrypt
from dotenv import load_dotenv

load_dotenv()


class Secure:
    def encoder(self, password: str = None):
        cd = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        return cd

    def decoder(self, password: str)-> bool:
        res = bcrypt.checkpw(password.encode(), getenv('WEB_PASSWORD').encode())
        return res

