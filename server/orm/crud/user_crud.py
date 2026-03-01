from . import *
from typing import List
from models import User

class UserCRUD:
    def __init__(self) -> None:
        result = Engine.start()
        self.user_engine = Engine.engine
        print(f"STATUS of engine initialization : {'SUCCESS' if result else 'FAILURE'}")

    async def create(self, user: User) -> bool:
        async with AsyncSession(self.user_engine) as session:
            statement = (
                insert(User)
                .values(
                    userid = user.userid,
                    username = user.username, 
                    password = user.password
                )
            )
            await session.execute(statement)
            await session.commit()
            return True
        
    async def read(self, user_id: int) -> List[Any]:
        async with AsyncSession(self.user_engine) as session:
            statement = (
                select(User)
                .where(User.userid == user_id)
            )
            result = await session.execute(statement)
            res = []
            for i in result:
                r = []
                for j in i:
                    r.append(j.userid)
                    r.append(j.username)
                    r.append(j.password)
                res.append(r)
            return res
                        
    async def update(self,user_id: int, **kwargs) -> bool:
        async with AsyncSession(self.user_engine) as session:
            statement = (
                update(User)
                .where(User.userid == user_id)
                .values(
                    username = kwargs["username"],
                    password = kwargs["password"]
                )
            )
            await session.execute(statement)
            await session.commit()
            return True
        
    async def delete(self, user_id: int) -> bool:
        async with AsyncSession(self.user_engine) as session:
            statement = (
                delete(User)
                .where(User.userid == user_id)
            )
            await session.execute(statement)
            await session.commit()
            return True
        
async def main() -> None:
    usr = UserCRUD()

    op = await usr.create(
        User(
            userid= 1,
            username= "Abhinag",
            password= "adfkadvad"
        )
    )
    print(f"The Row is created. --> {op}")

    result = await usr.read(1)
    print(result)

    op = await usr.update(1,
        username = "saicharan",
        password = "ads924QE#@"
    )
    print(f"The Row is updated. --> {op}")

    result = await usr.read(1)
    print(result)

    op = await usr.delete(1)
    print(f"The Row is deleted. --> {op}")

if __name__ == "__main__":
    asyncio.run(main())