from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta

#algoritmo dd encriptacion
algorithm_encryption = "HS256"

# tiempo de duracion del token de 10 minutos
access_token_expires = 10

#Clave secreta
SECRET = "Aña"

app = FastAPI()

oauth2 = OAuth2PasswordBearer(tokenUrl="login")

# contexto de encriptacion
crypt_context = CryptContext(schemes=["bcrypt"])


class User(BaseModel): 
    username: str   
    full_name: str
    email: str
    disables: bool

class UserDB(User): 
    password: str

users_db = {
    "Milanesa": {
        "username": "Milanesa",
        "full_name": "Digo Jara",
        "email": "fake@email.com",
        "disables": False,
        "password": "$2a$12$2Y1uHE6JeFKIxagfCYKfX.zTWm8knGz5mjdIoTbtfLqMaRBCE0vQW"
    },
    "Toto": {
        "username": "Toto",
        "full_name": "Juan Perez",
        "email": "fake@email.com",
        "disables": True,
        "password": "$2a$12$cLqhM9aEAQLcIrBv0Cd1CuZTLQRw1WZ0eczF5TKQH.kibrs3G6KOC"
    },
    "Hide on bush": {
        "username": "Hide on bush",
        "full_name": "Lee Sang-Hyeok",
        "email": "fake@email.com",
        "disables": False,
        "password": "$2a$12$6aBLnzKGXhaxiLtez804s.J2D.3tvHGhnHOyu7EIiE9AZVXOhpxF."
    }
}

def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])

def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username])
    

async def auht_user(token: str = Depends(oauth2)):

    EXCEPTION = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Not Authorized",
        headers={"WWW-Authenticate": "Bearer"})
    

    try:
        username = jwt.decode(token, SECRET, algorithms=[algorithm_encryption]).get("sub")
        if username is None:
            raise EXCEPTION
        
            

    except  JWTError: 
        raise EXCEPTION
    
    return search_user(username)

async def current_user(user: User = Depends(auht_user)):

    if user.disables:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
        detail="User disabled",)
    return user


@app.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user = search_user_db(form.username)

    if not crypt_context.verify(form.password, user.password):
        raise HTTPException(
            status_code= status.HTTP_400_BAD_REQUEST, detail="Password not correct")


    expire = datetime.utcnow() + timedelta(minutes=access_token_expires)

    access_token = ({ "sub": user.username, "exp": expire})

    return {"acces_token": jwt.encode(access_token, SECRET, algorithm=algorithm_encryption), "token_type": "bearer"}

@app.get("/users/me")
async def read_users_me(user: User= Depends(current_user)):
    return user