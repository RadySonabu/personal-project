from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from datetime import date

class IngredientCreate(BaseModel):
    name: str
    notes: Optional[str] = None

class Ingredient(BaseModel):
    id: int
    name: str
    notes: Optional[str] = None

class InventoryItemCreate(BaseModel):
    is_recipe: bool = False
    name: str
    measurement: float = Field(gt=0)
    unit: Optional[str] = None
    price: Optional[float] = None
    brand: Optional[str] = None
    notes: Optional[str] = None
    expiration: Optional[date] = None

class InventoryItem(BaseModel):
    id: int
    is_recipe: bool
    name: str
    measurement: float
    unit: Optional[str] = None
    price: Optional[float] = None
    brand: Optional[str] = None
    notes: Optional[str] = None
    expiration: Optional[date] = None

class RecipeIngredient(BaseModel):
    name: str
    quantity: float = Field(gt=0)
    unit: Optional[str] = None

class FoodRecipeCreate(BaseModel):
    name: str
    ingredients: List[RecipeIngredient]
    notes: Optional[str] = None

class FoodRecipe(BaseModel):
    id: int
    name: str
    ingredients: List[RecipeIngredient]
    notes: Optional[str] = None

class RecipeValidationRequest(BaseModel):
    batches: int = Field(1, gt=0)

class RecipeValidationResult(BaseModel):
    can_make: bool
    batches_requested: int
    max_batches: int
    shortages: List[Dict[str, object]]
