import mysql.connector
from mysql.connector import Error

class MySQLClient:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None

    # 데이터베이스 연결
    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            if self.connection.is_connected():
                print("[MySQLClient] MySQL 서버에 연결되었습니다.")
        except Error as e:
            print(f"[MySQLClient] MySQL 연결 실패: {e}")
            self.connection = None

    # 데이터 삽입
    def insert(self, table, data):
        if not self.connection:
            print("[MySQLClient] MySQL 연결이 되어 있지 않습니다.")
            return

        try:
            cursor = self.connection.cursor()
            columns = ", ".join(data.keys())
            values = ", ".join(["%s"] * len(data))
            query = f"INSERT INTO {table} ({columns}) VALUES ({values})"
            cursor.execute(query, tuple(data.values()))
            self.connection.commit()
            print(f"[MySQLClient] {cursor.rowcount} 개의 레코드가 삽입되었습니다.")
        except Error as e:
            print(f"[MySQLClient] 삽입 실패: {e}")

    # 데이터 조회
    def select(self, table, columns="*", where=None):
        if not self.connection:
            print("[MySQLClient] MySQL 연결이 되어 있지 않습니다.")
            return None

        try:
            cursor = self.connection.cursor(dictionary=True)
            query = f"SELECT {columns} FROM {table}"
            if where:
                query += f" WHERE {where}"
            cursor.execute(query)
            result = cursor.fetchall()
            return result
        except Error as e:
            print(f"[MySQLClient] 조회 실패: {e}")
            return None

    # 연결 종료
    def close(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("[MySQLClient] MySQL 연결이 종료되었습니다.")