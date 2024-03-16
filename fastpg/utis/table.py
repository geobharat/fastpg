import asyncpg
from config import settings

async def get_table(query):
    con = await asyncpg.connect(
        user=settings.username, host=settings.host, password=settings.password, database=settings.dbname, port=settings.port
    )

    types = await con.fetch(query)
    return types
