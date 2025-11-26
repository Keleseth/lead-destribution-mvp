from fastapi import APIRouter

from app.api.endpoints import interactions_router


main_router = APIRouter()
main_router.include_router(interactions_router)