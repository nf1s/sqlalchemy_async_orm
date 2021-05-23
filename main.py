import asyncio

from database import async_db_session
from models import Post, User


async def init_app():
    await async_db_session.init()
    await async_db_session.create_all()


async def create_user():
    await User.create(full_name="John Doe")
    user = await User.get(1)
    return user.id


async def create_post(user_id, data):
    await Post.create(user_id=user_id, data=data)
    posts = await Post.filter_by_user_id(user_id)
    return posts


async def update_user(id, full_name):
    await User.update(id, full_name="John Not Doe")
    user = await User.get(id)
    return user.full_name


async def async_main():
    await init_app()
    user_id = await create_user()
    await update_user(user_id, "John Not Doe")
    await create_post(user_id, "hello world")


asyncio.run(async_main())
