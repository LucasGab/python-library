from Book import Book
from Connection import Connection

def return_book(book: Book) -> None:
    if(book.id == -1):
        return
    stmt_delete = "DELETE FROM issued_books WHERE bid = %s"
    stmt_update = ("UPDATE books SET "
               "is_issued = %s "
               "WHERE id = %s")
    Connection.execute_many_statement([stmt_delete,stmt_update],[(book.id,),(False,book.id)])
