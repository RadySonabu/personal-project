from backend.core.config import DB_FILE, DB_BACKEND
from backend.db.json_repo import JSONDatabase as JSONDB
from backend.db import json_repo
from backend.db import sql_repo

json_db = JSONDB(DB_FILE)

def get_ingredient_repo():
    if DB_BACKEND in ("sqlite", "postgres"):
        return sql_repo.IngredientRepository()
    return json_repo.IngredientRepository(json_db)

def get_inventory_repo():
    if DB_BACKEND in ("sqlite", "postgres"):
        return sql_repo.InventoryRepository()
    return json_repo.InventoryRepository(json_db)

def get_recipe_repo():
    if DB_BACKEND in ("sqlite", "postgres"):
        return sql_repo.RecipeRepository()
    return json_repo.RecipeRepository(json_db)
