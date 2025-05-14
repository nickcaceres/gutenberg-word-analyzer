 # -*- coding: utf-8 -*-
"""Python_Programming_Final_V2.ipynb

Project Gutenberg Word Analyzer
Author: Nicholas Caceres
Date: 2025-05-06
Description: GUI-based tool to search for ebooks, extract and display the 10 most frequent words,
and store results in a local SQLite database.
"""

import tkinter as tk
from tkinter import messagebox, scrolledtext
import requests
from bs4 import BeautifulSoup
import sqlite3
import re
from collections import Counter

# Database Functions

def init_db():
    conn = sqlite3.connect('books.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS books (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT UNIQUE)''')
    c.execute('''CREATE TABLE IF NOT EXISTS word_frequencies (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    book_id INTEGER,
                    word TEXT,
                    frequency INTEGER,
                    FOREIGN KEY(book_id) REFERENCES books(id))''')
    conn.commit()
    conn.close()

def search_title(title):
    conn = sqlite3.connect('books.db')
    c = conn.cursor()
    c.execute("SELECT id FROM books WHERE title=?", (title,))
    result = c.fetchone()
    if result:
        book_id = result[0]
        c.execute("SELECT word, frequency FROM word_frequencies WHERE book_id=? ORDER BY frequency DESC LIMIT 10", (book_id,))
        words = c.fetchall()
    else:
        words = None
    conn.close()
    return words

def save_book(title, word_freq):
    conn = sqlite3.connect('books.db')
    c = conn.cursor()
    try:
        c.execute("INSERT INTO books (title) VALUES (?)", (title,))
        book_id = c.lastrowid
    except sqlite3.IntegrityError:
        conn.close()
        return  # Avoid duplicates
    for word, freq in word_freq:
        c.execute("INSERT INTO word_frequencies (book_id, word, frequency) VALUES (?, ?, ?)", (book_id, word, freq))
    conn.commit()
    conn.close()

# Web Functions 

def fetch_book_text(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        text = soup.get_text()
        return text
    except Exception as e:
        messagebox.showerror("Fetch Error", f"Could not fetch data: {e}")
        return None

def get_most_frequent_words(text, top_n=10):
    words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())  
    freq = Counter(words).most_common(top_n)
    return freq

# GUI 

def search_local():
    title = title_entry.get().strip()
    if not title:
        messagebox.showwarning("Input Error", "Please enter a book title.")
        return
    results = search_title(title)
    if results:
        output.delete('1.0', tk.END)
        output.insert(tk.END, f"Top 10 Words for '{title}':\n")
        for word, freq in results:
            output.insert(tk.END, f"{word}: {freq}\n")
    else:
        output.delete('1.0', tk.END)
        output.insert(tk.END, "Book was not found.")

def search_gutenberg():
    url = url_entry.get().strip()
    if not url:
        messagebox.showwarning("Input Error", "Please enter a URL.")
        return
    text = fetch_book_text(url)
    if text:
        title = title_entry.get().strip() or "Untitled"
        word_freq = get_most_frequent_words(text)
        save_book(title, word_freq)
        output.delete('1.0', tk.END)
        output.insert(tk.END, f"Top 10 Words for '{title}' (fetched):\n")
        for word, freq in word_freq:
            output.insert(tk.END, f"{word}: {freq}\n")

# Main 
init_db()

root = tk.Tk()
root.title("Gutenberg Word Analyzer")

# Book title search
tk.Label(root, text="Book Title:").pack()
title_entry = tk.Entry(root, width=50)
title_entry.pack()
tk.Button(root, text="Search Local DB", command=search_local).pack(pady=5)

# Gutenberg URL fetch
tk.Label(root, text="Project Gutenberg URL:").pack()
url_entry = tk.Entry(root, width=50)
url_entry.pack()
tk.Button(root, text="Fetch from Gutenberg", command=search_gutenberg).pack(pady=5)

# Output
output = scrolledtext.ScrolledText(root, height=15, width=60)
output.pack(pady=10)

root.mainloop()
