<br>

![image](https://raw.githubusercontent.com/eosiswastaken/books-scraper/main/.github/assets/bs4.png)

<br>

<p align="center">
  <img src="https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue" />
  <a href="https://gitmoji.dev">
  <img
    src="https://img.shields.io/badge/gitmoji-%20😜%20😍-FFDD67.svg?style=for-the-badge"
    alt="Gitmoji"
  />
</a>
</p>

Ce projet est un scraper pour [books.toscrape.com](https://books.toscrape.com) réalisé avec python et BeautifulSoup4.

<br>

---

👉 Features
- Récupération d'un livre
- Enregistrement des données pour chaque livre dans un fichier .csv
- Récupération automatique de chaque livre pour une catégorie donnée
- Téléchargement des images de chaque livre automatique


---

👉 Quickstart

cloner le repo

```bash
git clone https://github.com/eosiswastaken/books-scraper.git
```

entrer dans le repo

```bash
cd books-scraper
```

quelques exemples d'utilisation du scraper :

```python

import script3 as scraper

travelBooks = scraper.get_books_from_category("Travel")

  

fantasyBooks = scraper.get_books_from_category("Fantasy")

  

allBooks = travelBooks + fantasyBooks # récupération des livres de deux catégories puis concaténation de tous les livres en une variable

for book in allBooks:

    scraper.get_book(book) # recupere les données puis enregistre les données dans un .csv correspondant a la catégorie du livre

  

scraper.download_all_covers() # télécharge toutes les images des tous les livres scrapés
```




