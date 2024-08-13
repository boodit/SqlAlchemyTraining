from sqlalchemy import text, insert, select, delete, update
from src.database import async_engine, sync_engine
from src.models import metadata, workers_table


class SyncCore:

    @staticmethod
    def create_tables():
        sync_engine.echo = False
        metadata.drop_all(sync_engine)
        metadata.create_all(sync_engine)
        sync_engine.echo = True

    @staticmethod
    def insert_data():
        with sync_engine.connect() as connection:
            stmt = insert(workers_table).values(
                [
                    {'username': "Bob"},
                    {'username': "Alice"},
                ]
            )
            connection.execute(stmt)
            connection.commit()

    @staticmethod
    def select_data():
        with sync_engine.connect() as connection:
            query = select(workers_table)
            result = connection.execute(query)
            print(f"{result.all()=}")

    @staticmethod
    def update_data(worker_id: int = 2, new_username: str = "Sonya"):
        with sync_engine.connect() as connection:
            stmt = update(workers_table).values(username=new_username).filter_by(id=worker_id)
            connection.execute(stmt)
            connection.commit()


class AsyncCore:

    @staticmethod
    async def async_def():
        async with async_engine.connect() as connection:
            res = await connection.execute(text("SELECT VERSION()"))
            print(f"{res.all() =}")
