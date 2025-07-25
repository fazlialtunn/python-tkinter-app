import tkinter as tk
from tkinter import messagebox, ttk, font
from datetime import datetime, timedelta
import sqlite3
 
# Custom Style and Color Scheme
class AppStyles:
    BACKGROUND_COLOR = "#F0F4F8"
    PRIMARY_COLOR = "#2C3E50"
    ACCENT_COLOR = "#3498DB"
    SECONDARY_COLOR = "#34495E"
    TEXT_COLOR = "#2C3E50"
    BUTTON_COLOR = "#3498DB"
    BUTTON_TEXT_COLOR = "white"
 
# Initialize the SQLite database
def init_db():
    try:
        conn = sqlite3.connect("library.db")
        cursor = conn.cursor()
 
        # Create Books Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                available INTEGER DEFAULT 1
            )
        """)
 
        # Create Members Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS members (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL
            )
        """)
 
        # Create Borrow Records Table with borrow_date and return_date
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS borrows (
                id INTEGER PRIMARY KEY,
                book_id INTEGER,
                member_id INTEGER,
                borrow_date TEXT,
                return_date TEXT,
                FOREIGN KEY(book_id) REFERENCES books(id),
                FOREIGN KEY(member_id) REFERENCES members(id)
            )
        """)
        
        conn.commit()
        conn.close()
        print("Database initialized successfully")
    except sqlite3.Error as e:
        print(f"Error initializing database: {e}")
 
# Language translations
LANGUAGE = "EN"
translations = {
    "EN": {"add_book": "Add Book", "add_member": "Add Member", "borrow": "Borrow Book", "add_member":"Add Member", "add_book":"Add Book","borrow_book":"Borrow Book",
           "return_book":"Return Book", "view_book":"View Book", "settings":"Settings",
           "return": "Return Book", "view_books": "View Books", "name": "Name", "borrow_btn":"Borrow","library_management_system":"Library Management System",
           "email": "Email", "title": "Title", "author": "Author", "search_by_title":"Search by Title","select_member":"Select Member",
           "book_added": "Book added successfully!", "member_added": "Member added!", "search":"Search","return_button":"Return","add_new_book":"Add New Book",
           "days_prompt": "How many days would you like to borrow the book?", "settings":"Settings", "submit_btn":"Submit", "add_new_member":"Add new Member",
           "enter_borrowing_period_(days):":"Enter Borrowing Period (days):", "available":"Available", "return_date":"Return Date", "borrowed_by":"Borrowed By"},
           
    
    "TR": {"add_book": "Kitap Ekle", "add_member": "Üye Ekle", "borrow": "Kitap Ödünç Al", "add_member":"Üye Ekle", "add_book":"Kitap Ekle","borrow_book":"Kitap Ödünç Al",
           "return_book":"Kitap İade Et", "view_book":"Kitap Görüntüle", "settings":"Ayarlar",
           "return": "Kitap İade Et", "view_books": "Kitapları Gör", "name": "Ad", "search_by_title":"Başlık ile ara","add_new_book":"Yeni Kitap Ekle",
           "email": "E-posta", "title": "Başlık", "author": "Yazar", "borrow_btn":"Ödünç Al","select_member":"Üye Seç","library_management_system":"Kütüphane Yönetici Sistemi",
           "book_added": "Kitap başarıyla eklendi!", "member_added": "Üye başarıyla eklendi!","search":"Ara" ,"return_button":"İade et",
           "days_prompt": "Kitabı kaç gün almak istersiniz?", "settings": "Ayarlar", "submit_btn":"Yükle", "add_new_member":"Yeni üye ekle",
            "enter_borrowing_period_(days):":"Ödünç Alınacak Gün Sayısı", "available":"Müsaitlik", "return_date":"İade Edilecek Tarih", "borrowed_by":"Ödünç Alan"},
}
 
def tr(key):
    return translations[LANGUAGE].get(key, key)
 
# Main Application Class
class BookLendingApp(tk.Tk):
    def __init__(self):
        super().__init__()
        
        # Configure root window
        self.title("Python GUI Project")
        self.geometry("800x600")
        self.configure(bg=AppStyles.BACKGROUND_COLOR)
        
        # Custom font
        self.title_font = font.Font(family="Helvetica", size=24, weight="bold")
        self.button_font = font.Font(family="Helvetica", size=12, weight="bold")
        
        # Configure style
        self.style = ttk.Style()
        self.style.theme_use('clam')  # Modern theme
        
        # Custom button style
        self.style.configure('Custom.TButton',
                             background=AppStyles.BUTTON_COLOR,
                             foreground=AppStyles.BUTTON_TEXT_COLOR,
                             font=self.button_font)
        
        self.style.map('Custom.TButton',
                       background=[('active', AppStyles.ACCENT_COLOR)])
        
        # Create custom frame
        self.main_frame = tk.Frame(self, bg=AppStyles.BACKGROUND_COLOR)
        self.main_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)
        
        self.show_main_menu()
 
    def show_main_menu(self):
        # Clear previous widgets
        for widget in self.main_frame.winfo_children():
            widget.destroy()
 
        # Title Label with custom styling
        title_label = tk.Label(
            self.main_frame,
            text=tr("library_management_system"),
            font=self.title_font,
            fg=AppStyles.PRIMARY_COLOR,
            bg=AppStyles.BACKGROUND_COLOR
        )
        title_label.pack(pady=(0, 30))
 
        # Buttons configuration
        buttons = [
            (tr("add_book"), self.add_book_window),
            (tr("add_member"), self.add_member_window),
            (tr("borrow"), self.borrow_book_window),
            (tr("return"), self.return_book_window),
            (tr("view_books"), self.view_books_window),
            (tr("settings"), self.settings_window),
        ]
 
        # Button frame
        button_frame = tk.Frame(self.main_frame, bg=AppStyles.BACKGROUND_COLOR)
        button_frame.pack(expand=True)
 
        # Create buttons with grid layout
        for i, (text, command) in enumerate(buttons):
            row, col = divmod(i, 3)
            btn = ttk.Button(
                button_frame,
                text=text,
                command=command,
                style='Custom.TButton',
                width=20
            )
            btn.grid(row=row, column=col, padx=10, pady=10)
 
            
    def add_book_window(self):
        self._new_window(tr("add_book"), self.add_book_form)
 
    def add_member_window(self):
        self._new_window(tr("add_member"), self.add_member_form)
 
    def borrow_book_window(self):
        self._new_window(tr("borrow_book"), self.borrow_book_form)
 
    def return_book_window(self):
        self._new_window(tr("return_book"), self.return_book_form)
 
    def view_books_window(self):
        self._new_window(tr("view_books"), self.view_books)
 
    def settings_window(self):
        self._new_window(tr("settings"), self.settings_form)
 
    def _new_window(self, title, form_func):
        window = tk.Toplevel(self)
        window.title(title)
        window.geometry("600x500")
        window.configure(bg=AppStyles.BACKGROUND_COLOR)
        
        # Create a frame inside the window
        frame = tk.Frame(window, bg=AppStyles.BACKGROUND_COLOR)
        frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)
        
        # Override the window
        form_func(frame)
 
    def settings_form(self, frame):
            # Title Label
            title_label = tk.Label(
                frame,
                text=tr("settings"),
                font=self.title_font,
                fg=AppStyles.PRIMARY_COLOR,
                bg=AppStyles.BACKGROUND_COLOR
            )
            title_label.pack(pady=(0, 30))
 
            # Language Selection Frame
            lang_frame = tk.Frame(frame, bg=AppStyles.BACKGROUND_COLOR)
            lang_frame.pack(expand=True)
 
            def switch_language(lang):
                global LANGUAGE
                LANGUAGE = lang
                messagebox.showinfo("Success", "Language switched!")
                self.show_main_menu()
 
            # Language Buttons
            langs = [
                ("English", "EN"),
                ("Türkçe", "TR")
            ]
 
            for text, lang_code in langs:
                btn = ttk.Button(
                    lang_frame,
                    text=text,
                    command=lambda l=lang_code: switch_language(l),
                    style='Custom.TButton',
                    width=20
                )
                btn.pack(pady=10)
 
    def add_book_form(self, frame):
        # Title Label
        title_label = tk.Label(
            frame,
            text=tr("add_new_book"),
            font=self.title_font,
            fg=AppStyles.PRIMARY_COLOR,
            bg=AppStyles.BACKGROUND_COLOR
        )
        title_label.pack(pady=(0, 20))
 
        # Form Frame
        form_frame = tk.Frame(frame, bg=AppStyles.BACKGROUND_COLOR)
        form_frame.pack(expand=True)
 
        # Title Entry
        tk.Label(form_frame, text=tr("title"), bg=AppStyles.BACKGROUND_COLOR, fg=AppStyles.TEXT_COLOR).grid(row=0, column=0, sticky='e', padx=5, pady=5)
        title_entry = tk.Entry(form_frame, width=30, font=('Helvetica', 12))
        title_entry.grid(row=0, column=1, padx=5, pady=5)
 
        # Author Entry
        tk.Label(form_frame, text=tr("author"), bg=AppStyles.BACKGROUND_COLOR, fg=AppStyles.TEXT_COLOR).grid(row=1, column=0, sticky='e', padx=5, pady=5)
        author_entry = tk.Entry(form_frame, width=30, font=('Helvetica', 12))
        author_entry.grid(row=1, column=1, padx=5, pady=5)
 
        def submit():
            title = title_entry.get().strip()
            author = author_entry.get().strip()
            if not title or title.isspace():
                messagebox.showerror("Error", "Title cannot be empty or contain only spaces.")
                return
            
            if not author or author.isspace():
                messagebox.showerror("Error", "Author cannot be empty or contain only spaces.")
                return
 
            try:
                conn = sqlite3.connect("library.db")
                cursor = conn.cursor()
                cursor.execute("INSERT INTO books (title, author) VALUES (?, ?)", (title, author))
                conn.commit()
                conn.close()
                messagebox.showinfo("Success", tr("book_added"))
                # Clear entries
                title_entry.delete(0, tk.END)
                author_entry.delete(0, tk.END)
            except sqlite3.Error as e:
                messagebox.showerror("Error", f"Database error: {e}")
 
        # Submit Button
        submit_btn = ttk.Button(
            form_frame,
            text=tr("submit_btn"),
            command=submit,
            style='Custom.TButton'
        )
        submit_btn.grid(row=2, column=0, columnspan=2, pady=20)
 
    def add_member_form(self, frame):
        title_label = tk.Label(
            frame,
            text=tr("add_new_member"),
            font=self.title_font,
            fg=AppStyles.PRIMARY_COLOR,
            bg=AppStyles.BACKGROUND_COLOR
        )
        title_label.pack(pady=(0, 20))
 
        form_frame = tk.Frame(frame, bg=AppStyles.BACKGROUND_COLOR)
        form_frame.pack(expand=True)
 
        # Name Entry
        tk.Label(form_frame, text=tr("name"), bg=AppStyles.BACKGROUND_COLOR, fg=AppStyles.TEXT_COLOR).grid(row=0, column=0, sticky='e', padx=5, pady=5)
        name_entry = tk.Entry(form_frame, width=30, font=('Helvetica', 12))
        name_entry.grid(row=0, column=1, padx=5, pady=5)
 
        # Email Entry
        tk.Label(form_frame, text=tr("email"), bg=AppStyles.BACKGROUND_COLOR, fg=AppStyles.TEXT_COLOR).grid(row=1, column=0, sticky='e', padx=5, pady=5)
        email_entry = tk.Entry(form_frame, width=30, font=('Helvetica', 12))
        email_entry.grid(row=1, column=1, padx=5, pady=5)
 
        def submit():
            name = name_entry.get().strip()
            email = email_entry.get().strip()
 
            if not name or not email:
                messagebox.showerror("Error", "All fields are required.")
                return
            if '@' not in email:
                messagebox.showerror("Error", "Please enter a valid email address.")
                return    
            if not name or name.isspace():
                messagebox.showerror("Error", "Title cannot be empty or contain only spaces.")
                return
            if not email or email.isspace():
                messagebox.showerror("Error", "Author cannot be empty or contain only spaces.")
                return
 
            try:
                conn = sqlite3.connect("library.db")
                cursor = conn.cursor()
                cursor.execute("INSERT INTO members (name, email) VALUES (?, ?)", (name, email))
                conn.commit()
                conn.close()
                messagebox.showinfo("Success", tr("member_added"))
                # Clear entries
                name_entry.delete(0, tk.END)
                email_entry.delete(0, tk.END)
            except sqlite3.Error as e:
                messagebox.showerror("Error", f"Database error: {e}")
 
        # Submit Button
        submit_btn = ttk.Button(
            form_frame,
            text=tr("submit_btn"),
            command=submit,
            style='Custom.TButton'
        )
        submit_btn.grid(row=2, column=0, columnspan=2, pady=20)
 
    def borrow_book_form(self, frame):
        # Title Label
        title_label = tk.Label(
            frame,
            text=tr("borrow_book"),
            font=self.title_font,
            fg=AppStyles.PRIMARY_COLOR,
            bg=AppStyles.BACKGROUND_COLOR
        )
        title_label.pack(pady=(0, 20))

        # Search Bar Frame
        search_frame = tk.Frame(frame, bg=AppStyles.BACKGROUND_COLOR)
        search_frame.pack(fill=tk.X, padx=10, pady=(0, 10))

        search_label = tk.Label(
            search_frame,
            text=tr("search_by_title"),
            font=('Helvetica', 12),
            fg=AppStyles.TEXT_COLOR,
            bg=AppStyles.BACKGROUND_COLOR
        )
        search_label.pack(side=tk.LEFT, padx=(0, 5))

        search_entry = tk.Entry(search_frame, font=('Helvetica', 12), width=30)
        search_entry.pack(side=tk.LEFT, padx=(0, 5))

        # Treeview to display books
        tree = ttk.Treeview(frame, columns=("ID", "Title", "Author", "Available"), show="headings")
        tree.heading("ID", text="ID")
        tree.heading("Title", text=tr("title"))
        tree.heading("Author", text=tr("author"))
        tree.heading("Available", text=tr("available"))
        tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=(10, 0))
        
        def search_books(search_query):
            # Clear the current tree view content
            for row in tree.get_children():
                tree.delete(row)

            try:
                conn = sqlite3.connect("library.db")
                cursor = conn.cursor()

                if search_query:
                    # Search books
                    cursor.execute("SELECT id, title, author, available FROM books WHERE title LIKE ?", (f"%{search_query}%",))
                else:
                    # Fetch all books if no search query is provided
                    cursor.execute("SELECT id, title, author, available FROM books WHERE available > 0")

                for row in cursor.fetchall():
                    tree.insert("", tk.END, values=row)

                conn.close()
            except sqlite3.Error as e:
                messagebox.showerror("Error", f"Database error: {e}")

        search_button = ttk.Button(
            search_frame,
            text=tr("search"),
            style='Custom.TButton',
            command=lambda: search_books(search_entry.get().strip())
        )
        search_button.pack(side=tk.LEFT, padx=(5, 0))

        # Fetch and display all books initially
        search_books("")

        # Member Selection Frame
        member_frame = tk.Frame(frame, bg=AppStyles.BACKGROUND_COLOR)
        member_frame.pack(pady=10)
        
        # Use grid layout for horizontal alignment
        tk.Label(member_frame, text=tr("select_member"), bg=AppStyles.BACKGROUND_COLOR, fg=AppStyles.TEXT_COLOR).grid(row=0, column=0, padx=5)
        member_var = tk.StringVar()
        member_dropdown = ttk.Combobox(
            member_frame,
            textvariable=member_var,
            width=30,
            font=('Helvetica', 10)
        )
        
        try:
            conn = sqlite3.connect("library.db")
            cursor = conn.cursor()
            cursor.execute("SELECT id, name FROM members")
            members = cursor.fetchall()
            conn.close()
        
            member_dropdown['values'] = [f"{member[0]} - {member[1]}" for member in members]
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Database error: {e}")
            return
        
        member_dropdown.grid(row=0, column=1, padx=5)
        
        # Days Label and Entry
        tk.Label(member_frame, text=tr("enter_borrowing_period_(days):"), bg=AppStyles.BACKGROUND_COLOR, fg=AppStyles.TEXT_COLOR).grid(row=1, column=0, padx=5)
        days_entry = tk.Entry(member_frame, width=30)
        days_entry.grid(row=1, column=1, padx=5)
        
        def borrow_selected_book():
            selected_item = tree.selection()
            if not selected_item:
                messagebox.showerror("Error", "No book selected.")
                return
        
            if not member_var.get():
                messagebox.showerror("Error", "No member selected.")
                return
        
            book_id = tree.item(selected_item, "values")[0]
            member_id = member_var.get().split(" - ")[0]  # Extract member ID
        
            try:
                days = int(days_entry.get())
                if days <= 0:
                    messagebox.showerror("Error", "Please enter a valid number of days.")
                    return
    
                return_date = datetime.now() + timedelta(days=days)
                borrow_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                return_date_str = return_date.strftime("%Y-%m-%d %H:%M:%S")
    
                conn = sqlite3.connect("library.db")
                cursor = conn.cursor()
                cursor.execute("SELECT available FROM books WHERE id = ?", (book_id,))
                available = cursor.fetchone()
                if available and available[0] > 0:
                    cursor.execute("UPDATE books SET available = available - 1 WHERE id = ?", (book_id,))
                    cursor.execute("INSERT INTO borrows (book_id, member_id, borrow_date, return_date) VALUES (?, ?, ?, ?)",
                                (book_id, member_id, borrow_date, return_date_str))
                    conn.commit()
                    conn.close()
                    messagebox.showinfo("Success", f"Book borrowed successfully! Please return by {return_date_str}.")
                    search_books("")  # Refresh book list
                else:
                    messagebox.showerror("Error", "Book is not available for borrowing.")
                    conn.close()
    
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid number of days.")
        
        # Borrow Button
        borrow_button = ttk.Button(
            member_frame,
            text=tr("borrow_btn"),
            command=borrow_selected_book,
            style='Custom.TButton'
        )
        borrow_button.grid(row=2, column=0, columnspan=2, pady=10)

    def view_books(self, frame):
            # Title Label
            title_label = tk.Label(
                frame,
                text=tr("view_book"),
                font=self.title_font,
                fg=AppStyles.PRIMARY_COLOR,
                bg=AppStyles.BACKGROUND_COLOR
            )
            title_label.pack(pady=(0, 20))
 
            # Search Bar Frame
            search_frame = tk.Frame(frame, bg=AppStyles.BACKGROUND_COLOR)
            search_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
 
            search_label = tk.Label(
                search_frame,
            text=tr("search_by_title"),
                font=('Helvetica', 12),
                fg=AppStyles.TEXT_COLOR,
                bg=AppStyles.BACKGROUND_COLOR
            )
            search_label.pack(side=tk.LEFT, padx=(0, 5))
 
            search_entry = tk.Entry(search_frame, font=('Helvetica', 12), width=30)
            search_entry.pack(side=tk.LEFT, padx=(0, 5))
 
            def search_books():
                search_query = search_entry.get().strip()
                # Clear current tree view content
                for row in tree.get_children():
                    tree.delete(row)
 
                try:
                    conn = sqlite3.connect("library.db")
                    cursor = conn.cursor()
 
                    if search_query:
                        # Search books by title
                        cursor.execute("""
                SELECT id, title, author, available 
                FROM books 
                WHERE title LIKE ? OR author LIKE ?
                """, (f"%{search_query}%", f"%{search_query}%"))
                    else:
                        # Fetch all books if no search query is provided
                        cursor.execute("SELECT id, title, author, available FROM books")
                    
                    for row in cursor.fetchall():
                        tree.insert("", tk.END, values=row)
 
                    conn.close()
                except sqlite3.Error as e:
                    messagebox.showerror("Error", f"Database error: {e}")
 
            search_button = ttk.Button(
                search_frame,
            text=tr("search"),
                command=search_books,
                style='Custom.TButton'
            )
            search_button.pack(side=tk.LEFT, padx=(5, 0))
 
            # Treeview to display books
            tree = ttk.Treeview(frame, columns=("ID", "Title", "Author", "Available"), show="headings")
            tree.heading("ID", text="ID")
            tree.heading("Title", text=tr("title"))
            tree.heading("Author", text=tr("author"))
            tree.heading("Available", text=tr("available"))
             # Set column widths
            tree.column("ID", width=50)  # Narrow column for ID
            tree.column("Title", width=200)  # Wide column for Title
            tree.column("Author", width=150)  # Medium column for Author
            tree.column("Available", width=100)  # Medium column for Available status
            
            tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=(10, 0))
 
            # Populate the treeview with all books initially
            search_books()
 
    def return_book_form(self, window):
        # Search Bar Frame
        search_frame = tk.Frame(window, bg=AppStyles.BACKGROUND_COLOR)
        search_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
 
        search_label = tk.Label(
            search_frame,
            text=tr("search_by_title"),
            font=('Helvetica', 12),
            fg=AppStyles.TEXT_COLOR,
            bg=AppStyles.BACKGROUND_COLOR
        )
        search_label.pack(side=tk.LEFT, padx=(0, 5))
 
        search_entry = tk.Entry(search_frame, font=('Helvetica', 12), width=30)
        search_entry.pack(side=tk.LEFT, padx=(0, 5))
 
        search_button = ttk.Button(
            search_frame,
            text=tr("search"),
            style='Custom.TButton',
            command=lambda: fetch_borrowed_books(search_entry.get().strip())
        )
        search_button.pack(side=tk.LEFT, padx=(5, 0))
 
        # Treeview to display borrowed books
        tree = ttk.Treeview(window, columns=("ID", "Title", "Author", "Borrowed By", "Email", "Return Date"), show="headings")
        tree.heading("ID", text="ID")
        tree.heading("Title", text=tr("title"))
        tree.heading("Author", text=tr("author"))
        tree.heading("Borrowed By", text=tr("borrowed_by"))
        tree.heading("Email", text="Email")
        tree.heading("Return Date", text=tr("return_date"))
        tree.pack(fill=tk.BOTH, expand=True)
 
        def fetch_borrowed_books(search_query=""):
            """Fetch and display all borrowed books, optionally filtering by title."""
            try:
                conn = sqlite3.connect("library.db")
                cursor = conn.cursor()
 
                if search_query:
                    # Search borrowed books by title
                    cursor.execute("""
                        SELECT borrows.book_id, books.title, books.author, members.name, members.email, borrows.return_date
                        FROM borrows
                        JOIN books ON borrows.book_id = books.id
                        JOIN members ON borrows.member_id = members.id
                        WHERE books.title LIKE ?
                    """, (f"%{search_query}%",))
                else:
                    # Fetch all borrowed books
                    cursor.execute("""
                        SELECT borrows.book_id, books.title, books.author, members.name, members.email, borrows.return_date
                        FROM borrows
                        JOIN books ON borrows.book_id = books.id
                        JOIN members ON borrows.member_id = members.id
                    """)
 
                # Clear Treeview and populate with fresh data
                tree.delete(*tree.get_children())
                for row in cursor.fetchall():
                    tree.insert("", tk.END, values=row)
 
                conn.close()
            except sqlite3.Error as e:
                messagebox.showerror("Error", f"Database error: {e}")
 
        fetch_borrowed_books()  # Initial population of the Treeview
 
        def return_selected_book():
            selected_item = tree.selection()
            if not selected_item:
                messagebox.showerror("Error", "No book selected.")
                return
 
            book_id = tree.item(selected_item, "values")[0]
            try:
                conn = sqlite3.connect("library.db")
                cursor = conn.cursor()
 
                # Delete borrow record for the book
                cursor.execute("DELETE FROM borrows WHERE book_id = ?", (book_id,))
 
                # Increment the availability count for the book
                cursor.execute("UPDATE books SET available = available + 1 WHERE id = ?", (book_id,))
                conn.commit()
 
                messagebox.showinfo("Success", "Book returned successfully!")
 
                # Refresh the borrowed books list
                fetch_borrowed_books()
                conn.close()
            except sqlite3.Error as e:
                messagebox.showerror("Error", f"Database error: {e}")
 
        return_button = tk.Button(window, text=tr("return_button"), command=return_selected_book)
        return_button.pack(pady=5)
 
 
 
# Initialize database and start the application
if __name__ == "__main__":
    init_db()
    app = BookLendingApp()
    app.mainloop()