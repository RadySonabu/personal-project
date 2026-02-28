from fastapi import APIRouter, Depends
from typing import List, Any
from backend.models import InventoryItemCreate, InventoryItem
from backend.dependencies import get_inventory_repo

router = APIRouter()

@router.post("/inventory", response_model=InventoryItem)
async def add_inventory(payload: InventoryItemCreate, repo: Any = Depends(get_inventory_repo)):
    row = repo.create(payload.dict())
    return InventoryItem(**row)

@router.get("/inventory", response_model=List[InventoryItem])
async def list_inventory(repo: Any = Depends(get_inventory_repo)):
    rows = repo.list()
    return [InventoryItem(**r) for r in rows]
