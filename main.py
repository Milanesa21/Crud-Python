from fastapi import FastAPI 

app = FastAPI()

@app.get("/")
async def root():
    return {"owo": "uwu"}

@app.get("/sexito")
async def root2():
    return {"NO ME LO CREO": "INCREIBLE CHAVALES"}

#Para iniciar: uvicorn users:app --reload