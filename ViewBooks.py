

from typing import List, Union
from Book import Book
from Connection import Connection


def get_all_books() -> List[Book]:
    stmt_all = "SELECT name, publisher, author, is_issued, id FROM books"
    results = []
    results_raw = Connection.execute_query(stmt_all)
    for book_raw in results_raw:
        results.append(Book(book_raw[0],book_raw[1],book_raw[2],book_raw[3],book_raw[4]))
    return results

def get_books_by_name(search: str) -> List[Book]:
    print(search)
    stmt_all = "SELECT name, publisher, author, is_issued, id FROM books WHERE name LIKE %s"
    results = []
    results_raw = Connection.execute_query(stmt_all,("%" + search + "%",))
    for book_raw in results_raw:
        results.append(Book(book_raw[0],book_raw[1],book_raw[2],book_raw[3],book_raw[4]))
    return results

def get_book_by_id(id: int) -> Union[Book,None]:
    stmt_book = "SELECT name, publisher, author, is_issued, id FROM books WHERE id = %s"
    book_raw = Connection.execute_query(stmt_book,(id,),True)
    if book_raw is None:
        return None
    return Book(book_raw[0],book_raw[1],book_raw[2],book_raw[3],book_raw[4])