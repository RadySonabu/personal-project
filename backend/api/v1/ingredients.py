from fastapi import APIRouter, Depends
from typing import List, Any
from backend.models import IngredientCreate, Ingredient
from backend.dependencies import get_ingredient_repo

router = APIRouter()

@router.post("/ingredients", response_model=Ingredient)
async def create_ingredient(payload: IngredientCreate, repo: Any = Depends(get_ingredient_repo)):
    row = repo.create(name=payload.name, notes=payload.notes)
    return Ingredient(**row)

@router.get("/ingredients", response_model=List[Ingredient])
async def list_ingredients(repo: Any = Depends(get_ingredient_repo)):
    rows = repo.list()
    return [Ingredient(**r) for r in rows]
