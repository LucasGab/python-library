
from typing import Union
from Book import Book
from Connection import Connection

def get_book_by_id(id: int) -> Union[Book,None]:
    stmt_book = "SELECT name, publisher, author, is_issued, id FROM books WHERE id = %s"
    book_raw = Connection.execute_query(stmt_book,(id,),True)
    if book_raw is None:
        return None
    return Book(book_raw[0],book_raw[1],book_raw[2],book_raw[3],book_raw[4])
