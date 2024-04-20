from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

app = FastAPI()

oauth2 = OAuth2PasswordBearer(tokenUrl="login")

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
        "password": "1234"
    },
    "Toto": {
        "username": "Toto",
        "full_name": "Juan Perez",
        "email": "fake@email.com",
        "disables": True,
        "password": "4321"
    },
    "Hide on bush": {
        "username": "Hide on bush",
        "full_name": "Lee Sang-Hyeok",
        "email": "fake@email.com",
        "disables": False,
        "password": "3214"
    }
}

def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username])

def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])

async def current_user(token: str = Depends(oauth2)):
    user = search_user(token)
    if not user: 
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Not Authorized",
        headers={"WWW-Authenticate": "Bearer"})
    
    if user.disables:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
        detail="User disabled",)
    return user

@app.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User not correct")


    user = search_user_db(form.username)
    if not form.password == user.password:
        raise HTTPException(status_code= status.HTTP_400_BAD_REQUEST, detail="Password not correct")

    return {"acces_token": user.username, "token_type": "bearer"}

@app.get("/users/me")
async def read_users_me(user: User= Depends(current_user)):
    return user

# uvicorn basic_auth_users:app --reload