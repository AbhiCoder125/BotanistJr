from sqlmodel import select, update, delete, insert 
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from typing import List, Any
import asyncio

class Engine:
    DATABADATABASE_URL: str = "postgresql+asyncpg://postgres:{password}@{host}/{database}".format(
        password = "@Raghav2012".strip().replace("@", "%40"),
        host = "localhost".strip(),
        database = "botanistjr".strip()
    )
    __started: bool
    __stopped: bool
    engine: AsyncEngine

    @classmethod
    def start(cls) -> bool:
        try:
            cls.engine = create_async_engine(cls.DATABADATABASE_URL, echo=True)
            cls.__started = True
        except Exception as e:
            cls.__started = False
            print(f"The engine could not start because {e}")
        finally:
            return cls.__started
    
    @classmethod
    async def stop(cls) -> bool:
        try:
            await cls.engine.dispose()
            cls.__stopped = True
        except Exception as e:
            cls.__stopped = False
            print(f"The engine could not be stopped because {e}")
        finally:
            return cls.__stopped
                    

        
