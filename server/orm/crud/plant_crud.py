from crud import *
from typing import List, Any
from models import Plant
import asyncio

# Plant model has fields: plantid, name, scientific_name

class PlantCRUD:
    def __init__(self) -> None:
        result = Engine.start()
        self.user_engine = Engine.engine
        print(f"STATUS of engine initialization : {'SUCCESS' if result else 'FAILURE'}")

    async def create(self, plant: Plant) -> bool:
        """Insert a new Plant row. ``plantid`` may be omitted if autoincrementing."""
        async with AsyncSession(self.user_engine) as session:    
            statement = (
                insert(Plant)
                .values(
                    plantid=plant.plantid,
                    name=plant.name,
                    scientific_name=plant.scientific_name,
                )
            )
            await session.execute(statement)
            await session.commit()
            return True

    async def read(self, pid: int) -> List[Any]:
        """Return matching plant(s) by id as list of attribute lists."""
        async with AsyncSession(self.user_engine) as session:    
            statement = select(Plant).where(Plant.plantid == pid)
            result = await session.execute(statement)
            res: List[Any] = []
            for row in result:
                r = []
                for obj in row:
                    r.append(obj.plantid)
                    r.append(obj.name)
                    r.append(obj.scientific_name)
                res.append(r)
            return res

    async def update(self, plantid: int, **kwargs) -> bool:
        """Update name and/or scientific_name for a plant."""
        async with AsyncSession(self.user_engine) as session:    
            stmt = update(Plant).where(Plant.plantid == plantid)
            values: dict = {}
            if "name" in kwargs:
                values["name"] = kwargs["name"]
            if "scientific_name" in kwargs:
                values["scientific_name"] = kwargs["scientific_name"]
            if values:
                stmt = stmt.values(**values)
            await session.execute(stmt)
            await session.commit()
            return True

    async def delete(self, plantid: int) -> bool:
        async with AsyncSession(self.user_engine) as session:    
            statement = (
                delete(Plant)
                .where(Plant.plantid == plantid)
            )
            await session.execute(statement)
            await session.commit()
            return True

async def main() -> None:
    pt = PlantCRUD()

    # op = await pt.create(
    #     Plant(
    #         plantid = 1,
    #         name = "hibiscus",
    #         scientific_name = "afadlfknvjdk"
    #     )
    # )
    # print(f"Is Row Inserted --> {op}")

    op = await pt.read(1)
    print(op)

    # op = await pt.update(1,
    #     name = "Tulasi",
    #     scientific_name = "rqiopuewjf"
    # )
    # print(f"Is Row Updated --> {op}")

    # op = await pt.read(1)
    # print(op)

    # op = await pt.delete(1)
    # print(f"IS Row Deleted? --> {op}")


if __name__ == "__main__":
    asyncio.run(main())