from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy import update as sqlalchemy_update
from sqlalchemy.future import select
from sqlalchemy.orm import relationship

from database import Base, async_db_session


class ModelAdmin:
    @classmethod
    async def create(cls, **kwargs):
        async_db_session.add(cls(**kwargs))
        await async_db_session.commit()

    @classmethod
    async def update(cls, id, **kwargs):
        query = (
            sqlalchemy_update(User)
            .where(User.id == id)
            .values(**kwargs)
            .execution_options(synchronize_session="fetch")
        )

        await async_db_session.execute(query)
        await async_db_session.commit()

    @classmethod
    async def get(cls, id):
        query = select(cls).where(cls.id == id)
        results = await async_db_session.execute(query)
        (result,) = results.one()
        return result


class User(Base, ModelAdmin):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    full_name = Column(String)
    posts = relationship("Post")

    # required in order to acess columns with server defaults
    # or SQL expression defaults, subsequent to a flush, without
    # triggering an expired load
    __mapper_args__ = {"eager_defaults": True}

    def __repr__(self):
        return (
            f"<{self.__class__.__name__}("
            f"id={self.id}, "
            f"full_name={self.full_name}, "
            f"posts={self.posts}, "
            f")>"
        )


class Post(Base, ModelAdmin):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(ForeignKey("users.id"))
    data = Column(String)

    def __repr__(self):
        return (
            f"<{self.__class__.__name__}(" f"id={self.id}, " f"data={self.data}" f")>"
        )

    @classmethod
    async def filter_by_user_id(cls, user_id):
        query = select(cls).where(cls.user_id == user_id)
        posts = await async_db_session.execute(query)
        return posts.scalars().all()
