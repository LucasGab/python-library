
from Book import Book
from Connection import Connection


def issue_book(book: Book,issued_to: str) -> None:
    if(book.id == -1):
        return
    stmt_add = ("INSERT INTO issued_books "
               "(bid, issuedto) "
               "VALUES (%s, %s)")
    stmt_update = ("UPDATE books SET "
               "is_issued = %s "
               "WHERE id = %s")
    Connection.execute_many_statement([stmt_add,stmt_update],[(book.id,issued_to),(True,book.id)])