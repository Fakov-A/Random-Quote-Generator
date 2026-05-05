import tkinter as tk
from tkinter import messagebox, ttk
import random
import json
import os

# --- Данные ---
DEFAULT_QUOTES = [
    {"text": "Верь в себя и все получится!", "author": "Неизвестный", "topic": "Мотивация"},
    {"text": "Жизнь — это то, что происходит, пока ты строишь планы.", "author": "Джон Леннон", "topic": "Жизнь"},
    {"text": "Лучший способ начать — перестать говорить и начать делать.", "author": "Уолт Дисней", "topic": "Работа"},
]

HIST_FILE = 'quotes.json'

# --- Функции ---
def load_history():
    if os.path.exists(HIST_FILE):
        with open(HIST_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_history(history):
    with open(HIST_FILE, 'w', encoding='utf-8') as f:
        json.dump(history, f, ensure_ascii=False, indent=4)

def generate_quote():
    quote = random.choice(DEFAULT_QUOTES)
    quote_text.set(quote['text'])
    quote_author.set(quote['author'])
    quote_topic.set(quote['topic'])
    history.append(quote)
    save_history(history)
    update_history_list()

def filter_history():
    author = filter_author.get().lower()
    topic = filter_topic.get().lower()
    filtered = [
        q for q in history
        if (not author or author in q['author'].lower())
        and (not topic or topic in q['topic'].lower())
    ]
    history_list.delete(0, tk.END)
    for q in filtered:
        history_list.insert(tk.END, f"{q['text']} — {q['author']} ({q['topic']})")

def add_quote():
    text = new_quote_text.get().strip()
    author = new_quote_author.get().strip()
    topic = new_quote_topic.get().strip()
    if not text or not author or not topic:
        messagebox.showerror("Ошибка", "Все поля должны быть заполнены!")
        return
    quote = {"text": text, "author": author, "topic": topic}
    history.append(quote)
    save_history(history)
    update_history_list()
    new_quote_text.set('')
    new_quote_author.set('')
    new_quote_topic.set('')

def update_history_list():
    history_list.delete(0, tk.END)
    for q in history:
        history_list.insert(tk.END, f"{q['text']} — {q['author']} ({q['topic']})")

# --- Инициализация ---
root = tk.Tk()
root.title("Random Quote Generator")
root.geometry("600x500")

history = load_history()

# --- Переменные ---
quote_text = tk.StringVar()
quote_author = tk.StringVar()
quote_topic = tk.StringVar()
filter_author = tk.StringVar()
filter_topic = tk.StringVar()
new_quote_text = tk.StringVar()
new_quote_author = tk.StringVar()
new_quote_topic = tk.StringVar()

# --- Виджеты ---
tk.Label(root, text="Случайная цитата:", font=('Arial', 12, 'bold')).pack(pady=5)
tk.Label(root, textvariable=quote_text, wraplength=500, justify='center').pack(pady=5)
tk.Label(root, textvariable=quote_author, font=('Arial', 10, 'italic')).pack()
tk.Label(root, textvariable=quote_topic).pack(pady=10)

tk.Button(root, text="Сгенерировать цитату", command=generate_quote).pack(pady=5)

# Фильтр
filter_frame = tk.Frame(root)
filter_frame.pack(pady=10)
tk.Label(filter_frame, text="Фильтр по автору:").grid(row=0, column=0, padx=5)
tk.Entry(filter_frame, textvariable=filter_author).grid(row=0, column=1, padx=5)
tk.Label(filter_frame, text="Фильтр по теме:").grid(row=0, column=2, padx=5)
tk.Entry(filter_frame, textvariable=filter_topic).grid(row=0, column=3, padx=5)
tk.Button(filter_frame, text="Применить фильтр", command=filter_history).grid(row=0, column=4, padx=5)

# История
tk.Label(root, text="История цитат:", font=('Arial', 10, 'bold')).pack(pady=5)
history_list = tk.Listbox(root, width=70, height=10)
history_list.pack(pady=5)
update_history_list()

# Добавление новой цитаты
add_frame = tk.LabelFrame(root, text="Добавить новую цитату")
add_frame.pack(pady=10, fill='x')
tk.Label(add_frame, text="Текст:").grid(row=0, column=0, padx=5, pady=2)
tk.Entry(add_frame, textvariable=new_quote_text, width=40).grid(row=0, column=1, padx=5)
tk.Label(add_frame, text="Автор:").grid(row=1, column=0, padx=5, pady=2)
tk.Entry(add_frame, textvariable=new_quote_author).grid(row=1, column=1, padx=5)
tk.Label(add_frame, text="Тема:").grid(row=2, column=0, padx=5, pady=2)
tk.Entry(add_frame, textvariable=new_quote_topic).grid(row=2, column=1, padx=5)
tk.Button(add_frame, text="Добавить", command=add_quote).grid(row=3, columnspan=2, pady=10)

root.mainloop()