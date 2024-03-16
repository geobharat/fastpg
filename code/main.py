from fastapi import FastAPI, APIRouter, Query,Request
import asyncpg
from typing import Optional
from pydantic import BaseModel
from fastapi import Depends
from utis.table import get_table
from pydantic import BaseModel
from typing import Optional
from utis.makemodel import convert_model,convert_op
from config import user, host,password,database,port, schema
from fastapi.openapi.utils import get_openapi

app = FastAPI(title="FastAPI Implementation of PostgreSQL",
    docs_url="/",
    description="Convert your PostgreSQL Database into executable APIs",
    version="0.0.1",
    swagger_ui_parameters={"defaultModelsExpandDepth": -1},)



def sample(table: str):
    print(table)
    return {"Hello": table}


db_tables = []


# Example route
@app.get("/")
async def read_root():
    return {"message": "Hello World"}



async def gettab():
    con = await asyncpg.connect(
        user=user,
        host=host,
        password=password,
        database=database,
        port=port
    )
    types = await con.fetch(
        f"""SELECT 
    table_name, 
    column_name, 
    data_type 
FROM 
    information_schema.columns 
WHERE 
    table_schema = '{schema}';
                            """
    )
    maintab = {}
    for tp in types:
        if tp[0] not in maintab:
            maintab[tp[0]] = {}
        maintab[tp[0]][tp[1]] = tp[2]

    for key in maintab:
        print(key)
        theMod = convert_model(key, maintab[key])
        router = APIRouter()

        async def read_data(request: Request,m: theMod = Depends()):
            router_name = request.url.path.split('/')[1]
            core_query =  f"""SELECT * from "{schema}"."{router_name}" """  
            all_queries = []
            for field_name, field_value in m.dict().items():
                
                if field_value is not None and field_name != 'limit' and field_name != 'offset' and len(field_value.split('.')) == 2:
                    operation = field_value.split('.')[0]
                    value = field_value.split('.')[1]
                    query_string =  f''+ field_name + ' ' + convert_op(operation) + " '" + value  + "'" #f'"{field_name} {convert_op(operation)}'
                    all_queries.append(query_string)
            if len(all_queries) != 0:
                core_query += " where "
                core_query +=  " and ".join(all_queries)
            q =  await get_table(core_query)
            return q 

        router.add_api_route(f"", read_data, methods=["GET"])
        app.include_router(router, prefix=f"/{key}", tags=[key])


@app.on_event("startup")
async def startup_event():
    await gettab()
