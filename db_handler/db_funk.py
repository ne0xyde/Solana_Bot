from create_bot import async_session, Users
from sqlalchemy import select, update, insert
from sqlalchemy import func

# функция, для получения информации по конкретному пользователю
async def get_user_data(user_id: int, table_name=Users):
    async with async_session() as session:
        print(f'\n\n\n user_id = {user_id}\n\n\n')
        result = await session.execute(select(table_name).where(table_name.user_id == str(user_id)))
        return result.scalars().all()


# функция, для получения всех пользователей (для админки)
async def get_all_users(table_name=Users, count=False):
    async with async_session() as session:
        if count:
            result = await session.execute(func.count(table_name.ID))
        else:
            result = await session.execute(select(table_name))
        all_users = result.scalars().all()
        return all_users


# функция, для добавления пользователя в базу данных
async def insert_user(user_data: dict, table_name=Users):
    async with async_session() as session:
        query = insert(table_name).values(**user_data)
        await session.execute(query)
        await session.commit()


# функция для подсчёта рефералов
async def count_referrals(user_id: int, table_name=Users):
    async with async_session() as session:
        result = await session.execute(
            select(func.count(table_name.ID)).where(table_name.refer_id == str(user_id))
        )
        referrals_count = result.scalar()
        return referrals_count


# функция для получения wallet address
async def get_solana_address(user_id: int, private=False, table_name=Users):
    async with async_session() as session:
        result = await session.execute(
            select(table_name.solana_address).where(table_name.user_id == str(user_id))
        )
        solana_address = result.scalar_one_or_none()

        if private is True:
            result = await session.execute(
                select(table_name.privateKey).where(table_name.user_id == str(user_id))
            )
            priv_key = result.scalar_one_or_none()
            return solana_address, priv_key
        return solana_address


# функция обновления wallet address
async def update_solana_address(user_id: int, new_address: str):
    async with async_session() as session:
        query = update(Users).where(Users.user_id == str(user_id)).values(
            solana_address=new_address
        )
        await session.execute(query)
        await session.commit()
