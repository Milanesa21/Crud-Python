from fastapi import FastAPI 
from routers import products, usuarios
from fastapi.staticfiles import StaticFiles


app = FastAPI()

# rutas
app.include_router(usuarios.app)
app.include_router(products.router)
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def root():
    return {"owo": "uwu"}

@app.get("/sexito")
async def root2():
    return {"NO ME LO CREO": "INCREIBLE CHAVALES"}

#Para iniciar: uvicorn users:app --reload