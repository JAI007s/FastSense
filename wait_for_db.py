import time
import os
import pymysql

DB_HOST = os.getenv("DB_HOST", "db")
DB_PORT = int(os.getenv("DB_PORT", 3306))
DB_USER = os.getenv("DB_USER", "user")
DB_PASSWORD = os.getenv("DB_PASSWORD", "password")
DB_NAME = os.getenv("DB_NAME", "db")

def wait(max_retries=30):
    attempts = 0
    while attempts < max_retries:
        try:
            conn = pymysql.connect(host=DB_HOST, port=DB_PORT, user=DB_USER, password=DB_PASSWORD, database=DB_NAME)
            conn.close()
            print("[wait_for_db] Database is ready")
            return True
        except Exception as e:
            attempts += 1
            print(f"[wait_for_db] DB not ready ({e}), retry {attempts}/{max_retries} in 2s")
            time.sleep(2)
    raise Exception("Database not ready after retries")

if __name__ == "__main__":
    wait()