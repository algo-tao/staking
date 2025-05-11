from psycopg2 import pool
from psycopg2.extras import DictCursor
from contextlib import contextmanager
import traceback

class PgsqlStorage():
    def __init__(self):
        self.tabledata = []
        try:
            self.connection_pool = pool.ThreadedConnectionPool(
                minconn=1,
                maxconn=10,
                user='tao',
                password='taoWish2$',
                host='162.244.82.31',
                port='5432',
                database='subnet88'
            )
            
            with self.get_connection_from_pool() as connection:
                with connection.cursor() as cursor:
                    # Set the session to use UTC timezone
                    cursor.execute("SET TIME ZONE 'UTC';")
                    connection.commit()

        except Exception:
            errors = f"write row failed: {traceback.print_exc()}"
            print(errors)
    
    def __exit__(self):
        self.close_connection_pool()

    def close_connection_pool(self):
        self.connection_pool.closeall()

    @contextmanager
    def get_connection_from_pool(self):
        connection = self.connection_pool.getconn()
        try:
            yield connection
        finally:
            self.connection_pool.putconn(connection)

    def query_update(self, hotkey) -> int:
        query_sql = f"select update from miner_strategy where hotkey= '{hotkey}' limit 1"
        try:
            with self.get_connection_from_pool() as connection:
                with connection.cursor(cursor_factory=DictCursor) as cursor:
                    cursor.execute(query_sql)
                    cnt = cursor.fetchone()
            return cnt[0]
        except Exception as e:
            errors = f"query_context failed: {e}\n {traceback.print_exc()}"
            print(errors)
            return None

    def update_update(self, hotkey) -> bool:
        query_sql = f"update miner_strategy set update=0 where hotkey= '{hotkey}'"
        try:
            with self.get_connection_from_pool() as connection:
                with connection.cursor(cursor_factory=DictCursor) as cursor:
                    cursor.execute(query_sql)
                    connection.commit()
            return True
        except Exception as e:
            errors = f"query_context failed: {e}\n {traceback.print_exc()}"
            print(errors)
            return False

    def query_context(self, hotkey) -> str:
        query_sql = f"select content from miner_strategy where hotkey= '{hotkey}' limit 1"
        try:
            with self.get_connection_from_pool() as connection:
                with connection.cursor(cursor_factory=DictCursor) as cursor:
                    cursor.execute(query_sql)
                    cnt = cursor.fetchone()
            return cnt[0]
        except Exception as e:
            errors = f"query_context failed: {e}\n {traceback.print_exc()}"
            print(errors)
            return None
        