
import asyncpg
from config import user, host, password, database, port,schema


async def get_table(query):
    con = await asyncpg.connect(
        user=user,
        host=host,
        password=password,
        database=database,
        port=port
    )
  
    types = await con.fetch(query)
    for tp in types:
        print(tp)
    return types