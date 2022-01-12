from tkinter import Scrollbar, Tk, Toplevel
from tkinter import ttk
from tkinter.constants import BOTTOM, CENTER, NO, RIGHT, X, Y
from AddBook import save_book

from Book import Book
from Connection import Connection
from DeleteBook import delete_book
from ReturnBook import get_book_by_id
from ViewBooks import get_all_books, get_books_by_name

#TODO: Improve UI
#TODO: Improve error handle and message
class UI:
    def __init__(self) -> None:
        self.root = None
        self.table_widget = None
        self.id_input = None
        self.name_input = None
        self.books = {}
        self.book_content = None
    
    def destroy_book_content(self):
        if(self.book_content is not None):
            self.book_content.destroy()
        self.book_content = None

    def clean_value(self, value) -> str:
        # Remove all extra spaces
       new_value =  " ".join(value.split())
       new_value = "".join(new_value.rstrip().lstrip())
       return new_value

    def draw_book_content(self,book: Book = None):
        if(self.book_content is not None):
            return
        self.book_content = Toplevel(self.root)
        self.book_content.transient(self.root)
        self.book_content.geometry("300x150")
        self.book_content.resizable(False,False)
        if (id is None):
            self.book_content.title("New Book")
        else:
            self.book_content.title("Edit Book")
        
        # Book name section
        book_name_label = ttk.Label(self.book_content,text="Book name:")
        book_name_label.grid(column=0,row=0,padx=5,pady=5)
        book_name_input = ttk.Entry(self.book_content)
        book_name_input.grid(column=1,row=0,padx=5,pady=5)
        if(book is not None):
            book_name_input.insert(0,book.name)

        # Book publisher section
        book_publisher_label = ttk.Label(self.book_content,text="Book publisher:")
        book_publisher_label.grid(column=0,row=1,padx=5,pady=5)
        book_publisher_input = ttk.Entry(self.book_content)
        book_publisher_input.grid(column=1,row=1,padx=5,pady=5)
        if(book is not None):
            book_publisher_input.insert(0,book.publisher)

        # Book author section
        book_author_label = ttk.Label(self.book_content,text="Book author:")
        book_author_label.grid(column=0,row=2,padx=5,pady=5)
        book_author_input = ttk.Entry(self.book_content)
        book_author_input.grid(column=1,row=2,padx=5,pady=5)
        if(book is not None):
            book_author_input.insert(0,book.author)

        # Confirm button
        if(book is not None):
            confirm_button = ttk.Button(self.book_content, text="Confirm",command=lambda: self.edit_book(
                    (book_name_input.get(),book_publisher_input.get(),book_author_input.get()),book.id))
        else:
            confirm_button = ttk.Button(self.book_content, text="Confirm",command=lambda: self.add_book(
                    (book_name_input.get(),book_publisher_input.get(),book_author_input.get())))
        confirm_button.grid(column=1, row=3,padx=5,pady=5)

        # Cancel button
        cancel_button = ttk.Button(self.book_content, text="Cancel",command=self.destroy_book_content)
        cancel_button.grid(column=0, row=3,padx=5,pady=5)

        self.book_content.protocol("WM_DELETE_WINDOW", self.destroy_book_content)

    def get_all_books(self):
        self.books.clear()
        books = get_all_books()
        for book in books:
            self.books[book.id] = book
        self.update_table()

    def get_book_by_id(self):
        self.books.clear()
        if(self.id_input is None):
            return
        id_clean = self.clean_value(self.id_input.get())
        if(id_clean == ""):
            return

        try:
            id_book = int(id_clean)
        except ValueError as err:
            print(err)

        book = get_book_by_id(id_book)
        if book is not None:
            self.books[book.id] = book

        self.update_table() 

    def get_books_by_name(self):
        self.books.clear()
        if(self.name_input is None):
            return
        name_clean = self.clean_value(self.name_input.get())
        if(name_clean == ""):
            return

        books = get_books_by_name(name_clean)
        for book in books:
            self.books[book.id] = book
        self.update_table()

    def update_table(self):
        if(self.table_widget is not None):
            for i in self.table_widget.get_children():
                self.table_widget.delete(i)
        
        for book_id in self.books:
            book = self.books[book_id]
            self.table_widget.insert(parent='',index='end',iid=book.id,text='',
        values=(book.id,book.name,book.publisher,book.author,"Yes" if book.is_issued else "No"))
    
    def add_book(self,values):
        if(len(values) < 3):
            return
        final_values = []
        for i in range(len(values)):
            new_value = self.clean_value(values[i])
            if new_value == "":
                return
            final_values.append(new_value)

        book = Book(final_values[0],final_values[1],final_values[2],False)
        save_book(book)
        self.destroy_book_content()
        self.get_all_books()
    
    def edit_book(self,values,id:int):
        if(len(values) < 3):
            return
        final_values = []
        for i in range(len(values)):
            new_value = self.clean_value(values[i])
            if new_value == "":
                return
            final_values.append(new_value)

        book = Book(final_values[0],final_values[1],final_values[2],False,id)
        save_book(book)
        self.destroy_book_content()
        self.get_all_books()

    def get_edit_book(self):
        if(self.table_widget is None):
            return
        
        selected = self.table_widget.selection()
        if len(selected) > 0:
            book = self.books[int(selected[0])]
            self.draw_book_content(book)

    def delete_book(self):
        if(self.table_widget is None):
            return
        
        selected = self.table_widget.selection()
        for id in selected:
            book = self.books[int(id)]
            delete_book(book)
        
        self.get_all_books()

    def clear_search(self):
        if(self.id_input is not None):
            self.id_input.delete(0,'end')
        if(self.name_input is not None):
            self.name_input.delete(0,'end')
        self.get_all_books()

    def draw_main_content(self):
        self.root = Tk()
        self.root.resizable(False,False)
        self.root.title("Library")
        content = ttk.Frame(self.root)
        frame_table = ttk.Frame(content, borderwidth=5, relief="ridge")

        #scrollbar
        table_scroll = Scrollbar(frame_table)
        table_scroll.pack(side=RIGHT, fill=Y)
        table_scroll = Scrollbar(frame_table,orient='horizontal')
        table_scroll.pack(side= BOTTOM,fill=X)
        self.table_widget = ttk.Treeview(frame_table,height=20,yscrollcommand=table_scroll.set, xscrollcommand =table_scroll.set)

        table_scroll.config(command=self.table_widget.xview)
        table_scroll.config(command=self.table_widget.yview)

        #define our column
        columns_table = ('book_id', 'book_name', 'book_publisher', 'book_author', 'book_issued')
        
        self.table_widget['columns'] = columns_table

        self.table_widget.column("#0", width=0,  stretch=NO)
        self.table_widget.heading("#0",text="",anchor=CENTER)
        for column in columns_table:
            self.table_widget.column(column,anchor=CENTER, width=150)
            self.table_widget.heading(column,text=column.split("_")[1],anchor=CENTER)

        self.table_widget.pack()

        content.grid(column=0, row=0)
        frame_table.grid(column=0, row=0, columnspan=5, rowspan=20)

        search_row = 2

        # Search header
        search_fields_label= ttk.Label(content, text="Search fields")
        search_fields_label.grid(column=5,row=search_row,columnspan=9)

        # Clear Button
        clear_button = ttk.Button(content, text="Clear Search",command=self.clear_search)
        clear_button.grid(column=8,row=search_row)

        # Search id section
        search_id_label = ttk.Label(content, text="Search id:")
        search_id_label.grid(column=6,row=search_row+1,padx=5)
        self.id_input = ttk.Entry(content)
        self.id_input.grid(column=7, row=search_row+1,padx=5)
        search_button_id = ttk.Button(content, text="Search Book",command=self.get_book_by_id)
        search_button_id.grid(column=8, row=search_row+1,padx=5)

        # Search label section
        search_name_label = ttk.Label(content, text="Search name:")
        search_name_label.grid(column=6,row=search_row+2,padx=5)
        self.name_input = ttk.Entry(content)
        self.name_input.grid(column=7, row=search_row+2,padx=5)
        search_button_name = ttk.Button(content, text="Search Book",command=self.get_books_by_name)
        search_button_name.grid(column=8, row=search_row+2,padx=5)

        # New book button
        new_book_button = ttk.Button(content, text="New Book",command=self.draw_book_content)
        new_book_button.grid(column=5, row=0,padx=5)
        
        # Edit book button
        edit_book_button = ttk.Button(content, text="Edit Book",command=self.get_edit_book)
        edit_book_button.grid(column=7, row=0,padx=5)

        # Delete book button
        delete_book_button = ttk.Button(content, text="Delete Book",command=self.delete_book)
        delete_book_button.grid(column=9, row=0,padx=5)

        self.get_all_books()
        

if __name__ == "__main__":
    Connection.migrate()
    ui = UI()
    ui.draw_main_content()
    ui.root.mainloop()
    Connection.close_connection()