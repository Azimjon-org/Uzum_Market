import datetime
import enum

from sqlalchemy import INT, BigInteger, VARCHAR, Boolean, TIMESTAMP, func, Integer, Enum, TEXT, DECIMAL, SMALLINT, \
    ForeignKey, Column
from sqlalchemy.orm import DeclarativeBase, declared_attr, relationship
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


# engine.connect()


class Base(DeclarativeBase):
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower() + 's'


class CustomAbstarct(Base):
    __abstract__ = True
    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=func.current_timestamp())
    updated_at: Mapped[datetime] = Column(TIMESTAMP, default=func.current_timestamp(),
                                          onupdate=func.current_timestamp())


class User(CustomAbstarct):
    class LangEnum(enum.Enum):
        UZ = 'uz'
        RU = 'ru'
        EN = 'en'

    user_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    first_name: Mapped[str] = mapped_column(VARCHAR(255))
    last_name: Mapped[str] = mapped_column(VARCHAR(255), nullable=True)
    username: Mapped[str] = mapped_column(VARCHAR(255), nullable=True)
    phone_number: Mapped[str] = mapped_column(VARCHAR(255), nullable=True)
    lang: Mapped[str] = mapped_column(Enum(LangEnum, values_callable=lambda i: [field.value for field in i])
                                      , default=LangEnum.EN)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)

    def __repr__(self):
        return self.first_name


class Category(CustomAbstarct):
    __tablename__ = 'categories'
    name: Mapped[str] = mapped_column(VARCHAR(255), unique=True)
    allproducts: Mapped[list['AllProduct']] = relationship("AllProduct", back_populates='category')

    def __repr__(self):
        return self.name


class AllProduct(CustomAbstarct):
    title: Mapped[str] = mapped_column(VARCHAR(255))
    description: Mapped[str] = mapped_column(TEXT, nullable=True)
    price: Mapped[float] = mapped_column(DECIMAL(precision=8, scale=2))
    images: Mapped[str] = mapped_column(VARCHAR)
    quantity: Mapped[int] = mapped_column(SMALLINT, nullable=True)
    category_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('categories.id', ondelete="CASCADE"))
    category: Mapped[list[Category]] = relationship('Category', back_populates='allproducts')

    rating: Mapped[float] = mapped_column(DECIMAL(precision=8, scale=2), nullable=True)
    total: Mapped[float] = mapped_column(DECIMAL(precision=8, scale=2), nullable=True)
    discountPercentage: Mapped[float] = mapped_column(DECIMAL(precision=8, scale=2), nullable=True)
    p_category: Mapped[str] = mapped_column(VARCHAR(255), nullable=True)
    ingredients: Mapped[str] = mapped_column(TEXT, nullable=True)
    instructions: Mapped[str] = mapped_column(TEXT, nullable=True)
    prepTimeMinutes: Mapped[int] = mapped_column(INT, nullable=True)
    cookTimeMinutes: Mapped[int] = mapped_column(INT, nullable=True)
    difficulty: Mapped[str] = mapped_column(VARCHAR(255), nullable=True)
    cuisine: Mapped[str] = mapped_column(VARCHAR(255), nullable=True)

    def __repr__(self):
        return self.title


class Network(CustomAbstarct):
    name: Mapped[str] = mapped_column(VARCHAR(255))
    url: Mapped[str] = mapped_column(TEXT)
    images: Mapped[str] = mapped_column(TEXT,nullable=True)

    def __repr__(self):
        return self.name


class ContactAddress(CustomAbstarct):
    __tablename__="contact_addresses"
    address :Mapped[str] =mapped_column(TEXT)
    contact: Mapped[str] =mapped_column(VARCHAR(255))
    image:Mapped[str]=mapped_column(TEXT,nullable=True)



# with open('/home/asus/PycharmProjects/pythonProject/FactorBooks/db/data/recipes.json', 'r') as f:
#     data = json.load(f)

# for i in data:
#     with Session(engine) as s:
#         product = {
#             'title': i['name'],
#             'description': i['instructions'],
#             'price': i['caloriesPerServing'],
#             'images': i['image'],
#             'quantity': i['reviewCount'],
#             'discountPercentage': i['prepTimeMinutes'],
#             'category_id': 3,
#             'rating': i['rating'],
#             'ingredients': i['ingredients'],
#             'instructions': i['instructions'],
#             'cookTimeMinutes': i['cookTimeMinutes'],
#             'prepTimeMinutes': i['prepTimeMinutes'],
#         }
#         query = insert(AllProduct).values(**product)
#         s.execute(query)
#         s.commit()
