
from Book import Book
from Connection import Connection


def delete_book(book: Book) -> None:
    stmt_delete = "DELETE FROM books WHERE id = %s"
    Connection.execute_statement(stmt_delete,(book.id,))