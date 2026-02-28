from fastapi import APIRouter, Depends, HTTPException
from typing import List, Dict, Any
from backend.models import FoodRecipeCreate, FoodRecipe, RecipeValidationRequest, RecipeValidationResult
from backend.dependencies import get_recipe_repo, get_inventory_repo
from backend.services.recipes import compute_max_batches, build_available_map

router = APIRouter()

@router.post("/recipes", response_model=FoodRecipe)
async def create_recipe(payload: FoodRecipeCreate, repo: Any = Depends(get_recipe_repo)):
    row = repo.create({"name": payload.name, "notes": payload.notes, "ingredients": [i.dict() for i in payload.ingredients]})
    return FoodRecipe(**row)

@router.get("/recipes", response_model=List[FoodRecipe])
async def list_recipes(repo: Any = Depends(get_recipe_repo)):
    rows = repo.list()
    return [FoodRecipe(**r) for r in rows]

@router.get("/recipes/{recipe_id}/max-batches", response_model=Dict[str, int])
async def get_max_batches(recipe_id: int, recipes: Any = Depends(get_recipe_repo), inventory: Any = Depends(get_inventory_repo)):
    row = recipes.get(recipe_id)
    if not row:
        raise HTTPException(status_code=404, detail="Recipe not found")
    recipe = FoodRecipe(**row)
    value = compute_max_batches(recipe, inventory.list())
    return {"max_batches": value}

@router.post("/recipes/{recipe_id}/validate", response_model=RecipeValidationResult)
async def validate_recipe(recipe_id: int, payload: RecipeValidationRequest, recipes: Any = Depends(get_recipe_repo), inventory: Any = Depends(get_inventory_repo)):
    row = recipes.get(recipe_id)
    if not row:
        raise HTTPException(status_code=404, detail="Recipe not found")
    recipe = FoodRecipe(**row)
    available = build_available_map(inventory.list())
    shortages: List[Dict[str, object]] = []
    for req in recipe.ingredients:
        key = req.name.lower()
        unit = req.unit or ""
        needed = req.quantity * payload.batches
        have = available.get(key, {}).get(unit, 0.0)
        if have < needed:
            shortages.append({"name": req.name, "unit": unit or None, "required": needed, "available": have, "missing": max(0.0, needed - have)})
    max_possible = compute_max_batches(recipe, inventory.list())
    can_make = len(shortages) == 0
    return RecipeValidationResult(can_make=can_make, batches_requested=payload.batches, max_batches=max_possible, shortages=shortages)
