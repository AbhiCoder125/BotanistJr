from crud import *
from typing import List, Any
from models import UserLogin

# UserLogin model has fields: loginid (PK), sid (session FK), uid (user FK)
# no timestamp columns defined in the current models.py

class UserLoginCRUD:
    def __init__(self) -> None:
        result = Engine.start()
        self.user_engine = Engine.engine
        print(f"STATUS of engine initialization : {'SUCCESS' if result else 'FAILURE'}")

    async def create(self,user_login: UserLogin) -> bool:
        """Insert a new UserLogin row.  Pass a UserLogin instance with
        ``loginid`` (optional if autoincrementing), ``sid`` and ``uid`` set.
        """
        async with AsyncSession(self.user_engine) as session:
            statement = (
                insert(UserLogin)
                .values(
                    loginid=user_login.loginid,
                    sid=user_login.sid,
                    uid=user_login.uid,
                )
            )
            await session.execute(statement)
            await session.commit()
            return True

    async def read(self) -> List[Any]:
        """Return all rows as a list of simple attribute lists, similar to ``UserCRUD.read``.
        """
        async with AsyncSession(self.user_engine) as session:
            statement = select(UserLogin)
            result = await session.execute(statement)
            res: List[Any] = []
            for row in result:
                r = []
                for obj in row:
                    # each row contains a UserLogin instance
                    r.append(obj.loginid)
                    r.append(obj.sid)
                    r.append(obj.uid)
                res.append(r)
            return res

    async def update(self, loginid: int, **kwargs) -> bool:
        """Update the ``sid`` and/or ``uid`` for the given loginid.
        Additional fields may be passed in ``kwargs`` but only these two are
        currently handled.
        """
        async with AsyncSession(self.user_engine) as session:
            stmt = update(UserLogin).where(UserLogin.loginid == loginid)
            values: dict = {}
            if "sid" in kwargs:
                values["sid"] = kwargs["sid"]
            if "uid" in kwargs:
                values["uid"] = kwargs["uid"]
            if values:
                stmt = stmt.values(**values)
            await session.execute(stmt)
            await session.commit()
            return True

    async def delete(self, loginid: int) -> bool:
        async with AsyncSession(self.user_engine) as session:
            statement = (
                delete(UserLogin)
                .where(UserLogin.loginid == loginid)
            )
            await session.execute(statement)
            await session.commit()
            return True

async def main() -> None:
    usr_log = UserLoginCRUD()

    # create a new login record (loginid can be omitted if it is autoincremented)
    op = await usr_log.create(
        UserLogin(
            loginid=1,
            sid=1,    # assume there is a session with id 1
            uid=1     # assume there is a user with id 1
        )
    )
    print(f"The Row is created. --> {op}")

    result = await usr_log.read()
    print("all logins ->", result)

    op = await usr_log.update(1, sid=2, uid=1)
    print(f"Updated? {op}")

    result = await usr_log.read()
    print("after update ->", result)

    op = await usr_log.delete(1)
    print(f"Deleted? {op}")


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())

