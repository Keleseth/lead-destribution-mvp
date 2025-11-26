from fastapi import FastAPI

from app.api.router import main_router
from app.db.db_dependencies import engine
from app.models import Base



app = FastAPI()
app.include_router(main_router)

@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
