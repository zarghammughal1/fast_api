"""
    Test FastAPI
"""

from typing import Union
from fastapi import FastAPI, status, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import psycopg2


app = FastAPI()

conn = psycopg2.connect(
   database="MyFirstDB", user='postgres', password='8025', host='127.0.0.1', port= '5432'
)


cursor = conn.cursor()

class UserInSchema(BaseModel):
    """
    Define a class of user scahema
    """
    first_name: str
    last_name: str
    email: str
    password: str
    contact_number: Union[int, None] = None
    is_active: Union[bool, None] = None

@app.post("/user/", status_code=status.HTTP_201_CREATED)
async def post_user(record: UserInSchema):
    """
    Post User API
    """
    try:
        query = f"""insert into users
                    (first_name, last_name, email, password, contact_number, is_active)
                    values ('{record.first_name}', '{record.last_name}', '{record.email}', 
                            '{record.password}', '{record.contact_number}', '{record.is_active}')
        """
        cursor.execute(query)
        conn.commit()
        return record.dict()
    except Exception as err:
        print(err)
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
        detail= "Email already exists") from err

@app.get("/user/{user_id}/")
async def read_user(user_id: int):
    """
    Get User API
    """
    try:
        query = f"""select * from users where id = {user_id};
        """
        cursor.execute(query)
        result = cursor.fetchone()
    except Exception as err:
        print("Error -------->", err)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail= "Something went wrong") from err

    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail= "User not found!")

    return result


@app.put("/user/{user_id}/", status_code=status.HTTP_202_ACCEPTED)
async def update_user(user_id: int, record: UserInSchema):
    """
    Update User API
    """
    try:
        query = f"select * from users where id = {user_id};"
        cursor.execute(query)
        result = cursor.fetchone()
        if not result:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
            content={"detail": "User not found"})

        query = f"""Update users set
                    first_name = '{record.first_name}', 
                    last_name = '{record.last_name}',
                    email = '{record.email}', 
                    password = '{record.password}', 
                    contact_number = {record.contact_number},
                    is_active = '{record.is_active}' 
                    where id = {user_id};
        """
        cursor.execute(query)
        conn.commit()
    except Exception as err:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail= "Something went wrong") from err

    return record.dict()


@app.delete("/user/{user_id}/", status_code=status.HTTP_202_ACCEPTED)
async def delete_user(user_id: int):
    """
    Delete User API
    """
    try:
        query = f"select * from users where id = {user_id};"
        cursor.execute(query)
        result = cursor.fetchone()
        if not result:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
            content={"detail": "User not found"})

        query = f"delete from users where id = {user_id}"
        cursor.execute(query)
        conn.commit()

    except Exception as err:
        print("Error -------->", err)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail= "Something went wrong") from err

    return "User deleted successfully!"
