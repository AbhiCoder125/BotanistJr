from crud import *
from typing import List
from models import Session
import asyncio

class SessionCRUD:
    def __init__(self) -> None:
        result = Engine.start()
        self.user_engine = Engine.engine
        print(f"STATUS of engine initialization : {'SUCCESS' if result else 'FAILURE'}")

    async def create(self, session_obj: Session) -> bool:
        """Insert a new Session row. ``sessionid`` is optional."""
        async with AsyncSession(self.user_engine) as session:
            statement = (
                insert(Session)
                .values(
                    sessionid=session_obj.sessionid,
                    pid=session_obj.pid,
                    usr_id=session_obj.usr_id,
                )
            )
            await session.execute(statement)
            await session.commit()
            return True

    async def read(self, sid: int) -> List[Any]:
        """Return sessions matching the given id as attribute lists."""
        async with AsyncSession(self.user_engine) as session:
            statement = select(Session).where(Session.sessionid == sid)
            result = await session.execute(statement)
            res: List[Any] = []
            for row in result:
                r = []
                for obj in row:
                    r.append(obj.sessionid)
                    r.append(obj.pid)
                    r.append(obj.usr_id)
                res.append(r)
            return res

    async def update(self, sessionid: int, **kwargs) -> bool:
        """Update ``pid`` and/or ``usr_id`` for given sessionid."""
        async with AsyncSession(self.user_engine) as session:
            stmt = update(Session).where(Session.sessionid == sessionid)
            values: dict = {}
            if "pid" in kwargs:
                values["pid"] = kwargs["pid"]
            if "usr_id" in kwargs:
                values["usr_id"] = kwargs["usr_id"]
            if values:
                stmt = stmt.values(**values)
            await session.execute(stmt)
            await session.commit()
            return True

    async def delete(self, sessionid: int) -> bool:
        async with AsyncSession(self.user_engine) as session:
            statement = (
                delete(Session)
                .where(Session.sessionid == sessionid)
            )
            await session.execute(statement)
            await session.commit()
            return True


async def main() -> None:
    s_crud = SessionCRUD()

    # create example session
    op = await s_crud.create(
        Session(sessionid=1, pid=1, usr_id=1)
    )
    print(f"Created? {op}")

    print("read ->", await s_crud.read(1))

    await s_crud.update(1, pid=2)
    print("after update ->", await s_crud.read(1))

    await s_crud.delete(1)
    print("after delete ->", await s_crud.read(1))


if __name__ == "__main__":
    asyncio.run(main())