import asyncio
import uvicorn
from fastapi import FastAPI
from api.routes import api_router
from db.repository import UserRepository
from db.initialize import init_db

app = FastAPI()

app.include_router(api_router)


async def main():
    await init_db()

    repo = UserRepository()

    uvicorn.run('main:app', host='127.0.0.1', port=8000, reload=True)


if __name__ == "__main__":
    asyncio.run(main())
