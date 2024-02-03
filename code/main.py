from fastapi import FastAPI, APIRouter,Query
from utis.table import get_table
import asyncpg
from typing import Optional
from pydantic import BaseModel



app = FastAPI()


def sample(table: str):
    print(table)
    return {"Hello": table}


db_tables = []

# Example route
@app.get("/")
async def read_root(ass):
    return {"message": "Hello World"}


async def gettab():
    con = await asyncpg.connect(
        user="myuser",
        host="localhost",
        password="mypassword",
        database="mydb",
        port=5437,
    )
    types = await con.fetch(
        """SELECT 
    table_name, 
    column_name, 
    data_type 
FROM 
    information_schema.columns 
WHERE 
    table_schema = 'api';
                            """
    )
    maintab = {}
    for tp in types:
        if tp[0] not in maintab:
            maintab[tp[0]] = {}
        maintab[tp[0]][tp[1]] = tp[2]

    for key in maintab:
        router = APIRouter()
        for k in maintab[key]:
           print(k)
           if maintab[key][k] == 'bigint' or maintab[key][k] == 'int':
               print('type int')
        def get_sample(table):
            return get_table(table)
        router.add_api_route(f"", get_sample, methods=["GET"])
        app.include_router(router, prefix=f"/{key}", tags=[key])
    print(maintab)


@app.on_event("startup")
async def startup_event():
    await gettab()
