from typing import Dict, List, Any, Optional
from sqlalchemy import (
    create_engine,
    MetaData,
    Table,
    Column,
    Integer,
    String,
    Float,
    Boolean,
    Date,
    ForeignKey,
    Text,
    select,
    insert,
)
from sqlalchemy.engine import Engine
from backend.core.config import DB_URL

metadata = MetaData()

ingredients = Table(
    "ingredients",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String(255), nullable=False, unique=False),
    Column("notes", Text, nullable=True),
)

inventory = Table(
    "inventory",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("is_recipe", Boolean, nullable=False, default=False),
    Column("name", String(255), nullable=False),
    Column("measurement", Float, nullable=False),
    Column("unit", String(50), nullable=True),
    Column("price", Float, nullable=True),
    Column("brand", String(255), nullable=True),
    Column("notes", Text, nullable=True),
    Column("expiration", Date, nullable=True),
)

recipes = Table(
    "recipes",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String(255), nullable=False),
    Column("notes", Text, nullable=True),
)

recipe_ingredients = Table(
    "recipe_ingredients",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("recipe_id", Integer, ForeignKey("recipes.id", ondelete="CASCADE"), nullable=False),
    Column("name", String(255), nullable=False),
    Column("quantity", Float, nullable=False),
    Column("unit", String(50), nullable=True),
)

def _create_engine() -> Engine:
    engine = create_engine(DB_URL, future=True)
    metadata.create_all(engine)
    return engine

engine: Engine = _create_engine()

class IngredientRepository:
    def create(self, name: str, notes: Optional[str]) -> Dict[str, Any]:
        with engine.begin() as conn:
            result = conn.execute(insert(ingredients).values(name=name, notes=notes))
            nid = int(result.inserted_primary_key[0])
            row = conn.execute(select(ingredients).where(ingredients.c.id == nid)).mappings().one()
            return dict(row)

    def list(self) -> List[Dict[str, Any]]:
        with engine.connect() as conn:
            rows = conn.execute(select(ingredients)).mappings().all()
            return [dict(r) for r in rows]

class InventoryRepository:
    def create(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        with engine.begin() as conn:
            result = conn.execute(insert(inventory).values(**payload))
            nid = int(result.inserted_primary_key[0])
            row = conn.execute(select(inventory).where(inventory.c.id == nid)).mappings().one()
            return dict(row)

    def list(self) -> List[Dict[str, Any]]:
        with engine.connect() as conn:
            rows = conn.execute(select(inventory)).mappings().all()
            return [dict(r) for r in rows]

class RecipeRepository:
    def create(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        with engine.begin() as conn:
            result = conn.execute(insert(recipes).values(name=payload.get("name"), notes=payload.get("notes")))
            rid = int(result.inserted_primary_key[0])
            for ing in payload.get("ingredients", []):
                conn.execute(insert(recipe_ingredients).values(recipe_id=rid, name=ing.get("name"), quantity=ing.get("quantity"), unit=ing.get("unit")))
            row = conn.execute(select(recipes).where(recipes.c.id == rid)).mappings().one()
            ings = conn.execute(select(recipe_ingredients).where(recipe_ingredients.c.recipe_id == rid)).mappings().all()
            return {"id": row["id"], "name": row["name"], "notes": row["notes"], "ingredients": [dict(i) | {"id": None} for i in ings]}

    def list(self) -> List[Dict[str, Any]]:
        with engine.connect() as conn:
            rows = conn.execute(select(recipes)).mappings().all()
            result: List[Dict[str, Any]] = []
            for row in rows:
                rid = row["id"]
                ings = conn.execute(select(recipe_ingredients).where(recipe_ingredients.c.recipe_id == rid)).mappings().all()
                result.append({"id": row["id"], "name": row["name"], "notes": row["notes"], "ingredients": [dict(i) | {"id": None} for i in ings]})
            return result

    def get(self, recipe_id: int) -> Optional[Dict[str, Any]]:
        with engine.connect() as conn:
            row = conn.execute(select(recipes).where(recipes.c.id == recipe_id)).mappings().first()
            if not row:
                return None
            ings = conn.execute(select(recipe_ingredients).where(recipe_ingredients.c.recipe_id == recipe_id)).mappings().all()
            return {"id": row["id"], "name": row["name"], "notes": row["notes"], "ingredients": [dict(i) | {"id": None} for i in ings]}
