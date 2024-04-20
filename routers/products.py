from fastapi import APIRouter

router = APIRouter(prefix="/products",tags=["products"] , responses={404: {"description": "Not found"}})

@router.get("/")
def products():
    return ["Product 1", "Product 2", "Product 3"]