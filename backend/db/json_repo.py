from pathlib import Path
import json
import threading
from typing import Dict, List, Optional, Any

class JSONDatabase:
    def __init__(self, path: Path):
        self.path = Path(path)
        self.lock = threading.Lock()
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            self._write({"ingredients": [], "inventory": [], "recipes": [], "_seq": {"ingredients": 1, "inventory": 1, "recipes": 1}})

    def _read(self) -> Dict[str, Any]:
        with self.path.open("r", encoding="utf-8") as f:
            return json.load(f)

    def _write(self, data: Dict[str, Any]) -> None:
        tmp = self.path.with_suffix(".tmp")
        with tmp.open("w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False)
        tmp.replace(self.path)

    def next_id(self, collection: str) -> int:
        with self.lock:
            data = self._read()
            nid = int(data["_seq"].get(collection, 1))
            data["_seq"][collection] = nid + 1
            self._write(data)
            return nid

    def insert(self, collection: str, item: Dict[str, Any]) -> Dict[str, Any]:
        with self.lock:
            data = self._read()
            rows = data.get(collection, [])
            rows.append(item)
            data[collection] = rows
            self._write(data)
            return item

    def list(self, collection: str) -> List[Dict[str, Any]]:
        data = self._read()
        return list(data.get(collection, []))

    def get(self, collection: str, item_id: int) -> Optional[Dict[str, Any]]:
        data = self._read()
        for row in data.get(collection, []):
            if int(row.get("id")) == int(item_id):
                return row
        return None

class IngredientRepository:
    def __init__(self, db: JSONDatabase):
        self.db = db

    def create(self, name: str, notes: Optional[str]) -> Dict[str, Any]:
        nid = self.db.next_id("ingredients")
        item = {"id": nid, "name": name, "notes": notes}
        return self.db.insert("ingredients", item)

    def list(self) -> List[Dict[str, Any]]:
        return self.db.list("ingredients")

class InventoryRepository:
    def __init__(self, db: JSONDatabase):
        self.db = db

    def create(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        nid = self.db.next_id("inventory")
        item = {"id": nid, **payload}
        return self.db.insert("inventory", item)

    def list(self) -> List[Dict[str, Any]]:
        return self.db.list("inventory")

class RecipeRepository:
    def __init__(self, db: JSONDatabase):
        self.db = db

    def create(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        nid = self.db.next_id("recipes")
        item = {"id": nid, **payload}
        return self.db.insert("recipes", item)

    def list(self) -> List[Dict[str, Any]]:
        return self.db.list("recipes")

    def get(self, recipe_id: int) -> Optional[Dict[str, Any]]:
        return self.db.get("recipes", recipe_id)
