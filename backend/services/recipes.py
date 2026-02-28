from typing import Dict, List
from backend.models import FoodRecipe

def build_available_map(inventory_rows: List[Dict[str, object]]) -> Dict[str, Dict[str, float]]:
    available: Dict[str, Dict[str, float]] = {}
    for item in inventory_rows:
        if item.get("is_recipe"):
            continue
        key = str(item.get("name", "")).lower()
        unit = str(item.get("unit") or "")
        measurement = float(item.get("measurement", 0))
        if key not in available:
            available[key] = {}
        available[key][unit] = available[key].get(unit, 0.0) + measurement
    return available

def compute_max_batches(recipe: FoodRecipe, inventory_rows: List[Dict[str, object]]) -> int:
    available = build_available_map(inventory_rows)
    max_batches = float("inf")
    for req in recipe.ingredients:
        key = req.name.lower()
        unit = req.unit or ""
        if key not in available:
            return 0
        available_amount = available[key].get(unit, 0.0)
        if available_amount <= 0:
            return 0
        max_batches = min(max_batches, int(available_amount // req.quantity))
    if max_batches == float("inf"):
        return 0
    return max_batches
