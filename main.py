import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

DATA_FILE = 'books.json'

class BookTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Book Tracker")
        self.books = []
        self.load_books()

        # --- Поля ввода ---
        tk.Label(root, text="Название книги:").grid(row=0, column=0, padx=5, pady=5, sticky='e')
        self.title_entry = tk.Entry(root, width=30)
        self.title_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(root, text="Автор:").grid(row=1, column=0, padx=5, pady=5, sticky='e')
        self.author_entry = tk.Entry(root, width=30)
        self.author_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(root, text="Жанр:").grid(row=2, column=0, padx=5, pady=5, sticky='e')
        self.genre_entry = tk.Entry(root, width=30)
        self.genre_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(root, text="Страниц:").grid(row=3, column=0, padx=5, pady=5, sticky='e')
        self.pages_entry = tk.Entry(root, width=10)
        self.pages_entry.grid(row=3, column=1, padx=5, pady=5, sticky='w')

        # --- Кнопка добавления ---
        self.add_btn = tk.Button(root, text="Добавить книгу", command=self.add_book)
        self.add_btn.grid(row=4, column=0, columnspan=2, pady=10)

        # --- Таблица книг ---
        self.tree = ttk.Treeview(root, columns=("Автор", "Жанр", "Страниц"), show='headings')
        self.tree.heading("Автор", text="Автор")
        self.tree.heading("Жанр", text="Жанр")
        self.tree.heading("Страниц", text="Страниц")
        self.tree.grid(row=5, column=0, columnspan=2, padx=5, pady=5, sticky='nsew')

        # --- Фильтрация ---
        tk.Label(root, text="Фильтр по жанру:").grid(row=6, column=0, padx=5, pady=5, sticky='e')
        self.filter_genre = tk.Entry(root, width=30)
        self.filter_genre.grid(row=6, column=1, padx=5, pady=5)

        tk.Label(root, text="Страниц больше:").grid(row=7, column=0, padx=5, pady=5, sticky='e')
        self.filter_pages = tk.Entry(root, width=10)
        self.filter_pages.grid(row=7, column=1, padx=5, pady=5, sticky='w')

        self.filter_btn = tk.Button(root, text="Применить фильтр", command=self.apply_filter)
        self.filter_btn.grid(row=8, column=0, columnspan=2, pady=10)

        # Заполнение таблицы при старте
        self.update_tree()

    def load_books(self):
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                self.books = json.load(f)
        else:
            self.books = []
            self.save_books()

    def save_books(self):
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.books, f, ensure_ascii=False, indent=4)

    def update_tree(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for book in self.books:
            self.tree.insert('', 'end', values=(book['author'], book['genre'], book['pages']))

    def add_book(self):
        title = self.title_entry.get().strip()
        author = self.author_entry.get().strip()
        genre = self.genre_entry.get().strip()
        pages_str = self.pages_entry.get().strip()

        if not title or not author or not genre or not pages_str:
            messagebox.showerror("Ошибка", "Все поля должны быть заполнены!")
            return

        if not pages_str.isdigit() or int(pages_str) <= 0:
            messagebox.showerror("Ошибка", "Количество страниц должно быть положительным числом!")
            return

        book = {
            "title": title,
            "author": author,
            "genre": genre,
            "pages": int(pages_str)
        }

        self.books.append(book)
        self.save_books()
        self.update_tree()

    def apply_filter(self):
        filter_genre = self.filter_genre.get().strip().lower()
        try:
            filter_pages = int(self.filter_pages.get().strip())
            if filter_pages < 0:
                filter_pages = None
                messagebox.showwarning("Внимание", "Число страниц должно быть неотрицательным. Фильтр по страницам отключен.")
                self.filter_pages.delete(0, tk.END)
                self.filter_pages.insert(0, "")
                return False
        except ValueError:
            filter_pages = None

        filtered_books = []
        for book in self.books:
            match_genre = filter_genre == "" or filter_genre in book['genre'].lower()
            match_pages = filter_pages is None or book['pages'] > filter_pages

            if match_genre and match_pages:
                filtered_books.append(book)

        # Очистка и заполнение таблицы отфильтрованными данными
        for i in self.tree.get_children():
            self.tree.delete(i)
        
        for book in filtered_books:
            self.tree.insert('', 'end', values=(book['author'], book['genre'], book['pages']))


if __name__ == "__main__":
    root = tk.Tk()
    app = BookTrackerApp(root)
    root.mainloop()
