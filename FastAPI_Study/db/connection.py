import aiosqlite


async def get_db():
    conn = await aiosqlite.connect("users.db")
    conn.row_factory = aiosqlite.Row
    try:
        yield conn
    finally:
        await conn.close()
