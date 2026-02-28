from fastapi import FastAPI
from backend.api.v1.health import router as health_router
from backend.api.v1.ingredients import router as ingredients_router
from backend.api.v1.inventory import router as inventory_router
from backend.api.v1.recipes import router as recipes_router

def create_app() -> FastAPI:
    app = FastAPI(title="Recipe Backend")
    app.include_router(health_router, prefix="/api")
    app.include_router(ingredients_router, prefix="/api")
    app.include_router(inventory_router, prefix="/api")
    app.include_router(recipes_router, prefix="/api")
    return app

app = create_app()
