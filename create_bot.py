import logging
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from decouple import config

# получаем список администраторов из .env
admins = [int(admin_id) for admin_id in config('ADMINS').split(',')]

# настраиваем логирование и выводим в переменную для отдельного использования в нужных местах
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


# инициируем объект, который будет отвечать за взаимодействие с базой данных
engine = create_async_engine(config('MYSQL_ASYNCMY_LINK'), echo=False)
Base = declarative_base()


class Users(Base):
    __tablename__ = 'users'
    ID = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(15), nullable=False)
    full_name = Column(String(40))
    user_login = Column(String(40))
    solana_address = Column(String(50))
    privateKey = Column(String(255))
    mnemonic = Column(String(255))
    refer_id = Column(String(15))

    def __repr__(self):
        return self.__tablename__


async_session = async_sessionmaker(engine, expire_on_commit=False)


# инициируем объект бота, передавая ему parse_mode=ParseMode.HTML по умолчанию
bot = Bot(token=config('TOKEN'), default=DefaultBotProperties(parse_mode=ParseMode.HTML))
storage = MemoryStorage()

# инициируем объект бота
dp = Dispatcher(storage=storage)
