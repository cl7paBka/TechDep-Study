# Стоит ли называть разные файлы в разных директориями одинаковыми именами? Например, /db/user.py и
# /schemas/input/user.py, а также /schemas/output/user.py
# Столкнулся с RuntimeError: threads can only be started once возникает из-за того, что поток, который должен
# обрабатывать подключение к базе данных через aiosqlite, был повторно запущен или попытка его запуска происходит
# неправильно.
from FastAPI_Study.db.connection import get_db
from FastAPI_Study.schemas.user import UserInfo, UserInDB


class UserRepository:
    async def create_user(self, user: UserInfo) -> int:
        """Добавить нового пользователя в бд"""
        query = """
        INSERT INTO users
        (first_name, last_name, age, email) VALUES (?, ?, ?, ?)
        """
        async for c in get_db():
            async with c.cursor() as cursor:
                await cursor.execute(query, (user.first_name, user.last_name, user.age, user.email))
                await c.commit()
                return cursor.lastrowid

    async def get_user_by_id(self, user_id: int) -> UserInDB:
        """Вытащить из бд пользователя по id"""
        query = """
        SELECT user_id, first_name, last_name, age, email
        FROM users
        WHERE user_id = ?
        """
        async for c in get_db():
            async with c.cursor() as cursor:
                await cursor.execute(query, (user_id,))
                row = await cursor.fetchone()
                if row:
                    return UserInDB(**dict(row))  # Сделать лучше так или ретёрнить dict(row) и всё?

    async def list_all_users(self) -> list[UserInDB]:
        """Вытащить всех пользователей из бд"""
        query = """
        SELECT user_id, first_name, last_name, age, email
        FROM users
        """
        async for c in get_db():
            async with c.cursor() as cursor:
                cursor = await cursor.execute(query)
                rows = await cursor.fetchall()
                return [UserInDB(**dict(row)) for row in rows]

    async def update_user(self, user_id: int, user: UserInfo) -> None:
        """Функция для обновления информации о пользователе"""
        # базовая часть sql запроса
        query = "UPDATE users SET "
        fields_to_update = []
        values = []

        # далее, проверки на то, какие новые данные вели о пользователе
        if user.first_name is not None:
            fields_to_update.append("first_name = ?")
            values.append(user.first_name)

        if user.last_name is not None:
            fields_to_update.append("last_name = ?")
            values.append(user.last_name)

        if user.age is not None:
            fields_to_update.append("age = ?")
            values.append(user.age)

        if user.email is not None:
            fields_to_update.append("email = ?")
            values.append(user.email)

        # если нечего обновлять, то просто возвращаемся
        if not fields_to_update:
            return

        # объединяем поля в строку и добавляем условие WHERE, для поиска по id
        query += ", ".join(fields_to_update)
        query += " WHERE user_id = ?"

        # user_id добавляется в конец списка значений
        values.append(user_id)

        # выполняем готовый sql запрос, который динамически менялся из-за проверок
        async for c in get_db():
            async with c.cursor() as cursor:
                await cursor.execute(query, tuple(values))
                await c.commit()

    async def delete_user(self, user_id: int) -> None:
        """Функция для удаления пользователя из бд"""
        query = """
        DELETE FROM users
        WHERE user_id = ?
        """
        async for c in get_db():
            async with c.cursor() as cursor:
                await cursor.execute(query, (user_id,))
                await c.commit()
