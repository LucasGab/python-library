from typing import Any, Final, List, Union
import mysql.connector
from mysql.connector import errorcode
from mysql.connector.errors import Error

class Connection:

    DB_USER: Final = "user"
    DB_PASSWORD: Final = "password"
    DB_HOST: Final = "127.0.0.1"
    DB_PORT: Final = 3306
    DB_DATABASE: Final = "database"
    __connection: Any = None

    @staticmethod
    def get_connection() -> Any:
        try:
            if(Connection.__connection == None):
                Connection.__connection = mysql.connector.connect(user=Connection.DB_USER,password=Connection.DB_PASSWORD,
                                            host=Connection.DB_HOST,database=Connection.DB_DATABASE,port=Connection.DB_PORT)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err) 
        return Connection.__connection

    @staticmethod
    def __exist_table(table_name: str) -> bool:
        result = False
        try:
            conn = Connection.get_connection()
            cursor = conn.cursor()
            stmt = "SHOW TABLES LIKE %s"
            cursor.execute(stmt,(table_name,))
            result = cursor.fetchone()
        except Error as err:
            print(err)
        finally:
            if(cursor):
                cursor.close()

        return result

    @staticmethod
    def __create_table_books() -> None:
        stmt = ("CREATE TABLE `books` ("
            "  `id` bigint NOT NULL AUTO_INCREMENT,"
            "  `name` varchar(45) NOT NULL,"
            "  `publisher` varchar(45) NOT NULL,"
            "  `author` varchar(45) NOT NULL,"
            "  `is_issued` boolean NOT NULL,"
            "  PRIMARY KEY (`id`))")
        Connection.execute_statement(stmt)
        

    @staticmethod
    def __create_table_issued() -> None:
        stmt = ("CREATE TABLE `issued_books` ("
            "  `bid` bigint NOT NULL,"
            "  `issuedto` varchar(45) NOT NULL,"
            "  PRIMARY KEY (`bid`))")
        Connection.execute_statement(stmt)
    
    @staticmethod
    def execute_statement(stmt: str,values = None,commit = True) -> None:
        conn = Connection.get_connection()
        try:
            cursor = conn.cursor()
            if(values is not None):
                cursor.execute(stmt,values)
            else:
                cursor.execute(stmt)
            conn.commit()
        except Error as err:
            print(err)
            conn.rollback()
        finally:
            if(cursor):
                cursor.close()
    
    @staticmethod
    def execute_many_statement(stmt: List[str],values = None,commit = True) -> None:
        conn = Connection.get_connection()
        try:
            cursor = conn.cursor()
            for i in range(len(stmt)):
                value = None
                if (len(values) > i):
                    value = values[i]
                if(value is not None):
                    cursor.execute(stmt[i],value)
                else:
                    cursor.execute(stmt[i])
            conn.commit()
        except Error as err:
            print(err)
            conn.rollback()
        finally:
            if(cursor):
                cursor.close()
    
    @staticmethod
    def execute_query(stmt: str,values=None,fetch_one=False) -> Union[List[tuple],tuple]:
        conn = Connection.get_connection()
        result = []
        try:
            cursor = conn.cursor()
            if(values is not None):
                cursor.execute(stmt,values)
            else:
                cursor.execute(stmt)
            if (fetch_one):
                result = cursor.fetchone()
            else:
                result = cursor.fetchall()
            return result
        except Error as err:
            print(err)
        finally:
            if(cursor):
                cursor.close()
        return []

    @staticmethod
    def migrate() -> None:
        if(not Connection.__exist_table("books")):
            Connection.__create_table_books()
        
        if(not Connection.__exist_table("issued_books")):
            Connection.__create_table_issued()
    
    @staticmethod
    def close_connection() -> None:
        if(Connection.__connection != None):
            try:
                Connection.__connection.close()
            except Error as err:
                print(err)
    