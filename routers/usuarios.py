from fastapi import APIRouter, HTTPException
from pydantic import BaseModel


# Crea la app
app= APIRouter(prefix="/users",tags=["users"], responses={404: {"description": "Not found"}})


# Entidad user
class User(BaseModel): 
    id: int   
    name: str
    surname: str
    url: str
    age: int


# Lista de usuarios
users_list = [User(id= 1, name = "Brais", surname = "Moure", url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ", age = 35),
        User(id= 2, name = "Diego", surname = "Jara", url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ", age = 21),
        User(id= 3, name = "Martina", surname = "Jara", url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ", age = 16)]


#Llama a todos los users
@app.get("/")
async def users():
    return users_list


#Llama a los users por su id por Path
@app.get("/{id}")
async def usersId(id: int):
    users = filter(lambda user: user.id == id, users_list)
    try:
        return list(users)[0]
    except IndexError: 
        raise HTTPException(status_code=404, detail="User not found")


# Para probar: http://127.0.0.1:8000/users/2


# Llama a los usuarios por su id por Query (No hace falta volverlo funcion, solo fue una prueba para ver si funcionaba)
@app.get("/query/")
async def usersID(id: int):
    return search_user_by_id(id)


# Para probar: http://127.0.0.1:8000/users/query/?id=2


# Funcion para buscar usuarios por id por Query
def search_user_by_id(id: int):
    users = filter(lambda user: user.id == id, users_list)
    try:
        return list(users)[0]
    except IndexError: 
        return 

# Crea un usuario
@app.post("/",response_model= User , status_code=201)
async def users_create(user: User):
    existing_user = search_user_by_id(user.id)
    if existing_user is not None:
        raise HTTPException(status_code=409, detail="User already exists")
    else:
        users_list.append(user)
        return user

# Actualiza un usuario
@app.put("/{id}")
async def user_update(user: User):

    found = False

    for index, saved_user in enumerate(users_list):
        if saved_user.id == user.id:
            users_list[index] = user
            found = True
    if not found:
        raise HTTPException(status_code=404, detail="User not found")
    else:
        return user


# Elimina un usuario
@app.delete("/{id}")
async def user_delete(id: int):
    found = False
    for index, saved_user in enumerate(users_list):
        if saved_user.id == id:
            del users_list[index]
            found = True
            return {"message": "User deleted"}
    if not found:
        raise HTTPException (status_code=404, detail="User not found")
#Para iniciar: uvicorn users:app --reload