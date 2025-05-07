# Gutenberg Word Analyzer

**Author:** Nicholas Caceres  
**Date:** May 6, 2025

# Description

This Python project is a GUI-based tool for analyzing books from the [Project Gutenberg](https://www.gutenberg.org/) library. It allows users to:

- Search for a book by title in a local database.
- If not found, download and analyze the book via a Project Gutenberg URL.
- Extract and display the top 10 most frequent words.
- Store the title and word frequencies locally for future access.

# Technologies Used

- `Tkinter` – for building the GUI
- `sqlite3` – for storing book data and word frequencies
- `requests` & `BeautifulSoup` – for downloading and parsing book content
- `re` & `collections.Counter` – for word frequency analysis

# Requirements

Install dependencies using:

```bash
pip install requests beautifulsoup4
