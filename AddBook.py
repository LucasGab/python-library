
from Book import Book
from Connection import Connection

def save_book(book: Book) -> None:
    stmt_add = ("INSERT INTO books "
               "(name, publisher, author, is_issued) "
               "VALUES (%s, %s, %s, %s)")
    stmt_update = ("UPDATE books SET "
               "name = %s, publisher = %s, author = %s, is_issued = %s "
               "WHERE id = %s")
    if(book.id == -1):
        Connection.execute_statement(stmt_add,(book.name,book.publisher,book.author,book.is_issued))
    else:
        Connection.execute_statement(stmt_update,(book.name,book.publisher,book.author,book.is_issued,book.id))
