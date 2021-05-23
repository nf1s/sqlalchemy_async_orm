import asyncio

from database import async_db_session
from models import Post, User


async def init_app():

    await async_db_session.init()
    await async_db_session.create_all()


async def async_main():
    await init_app()
    await User.create(full_name="John Doe")
    user = await User.get(1)
    print(user.id)
    print(user.full_name)
    posts = await Post.filter_by_user_id(user.id)
    print(posts)
    await user.update(full_name="John Not Doe")
    user = await User.get(1)
    print(user.full_name)


asyncio.run(async_main())
