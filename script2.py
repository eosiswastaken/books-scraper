import csv
import requests
import os
import glob
from bs4 import BeautifulSoup
import uuid


def get_book(URL) -> None:
    page = requests.get(URL) # obtenir l'URL de la page

    rating_titles = ["One","Two","Three","Four","Five"]

    soup = BeautifulSoup(page.content, "html.parser") # parser la page et la stocker dans la variable soup

    upc = soup.find_all('td')[0].text # code universel : on recupere tous les elements 'td', on regarde le premier et on recupere son texte

    title = soup.find('li', {"class":"active"}).text # titre : on recupere l'element 'li' ayant pour classe 'active' et on recupere son texte


    price_excl = soup.find_all('td')[2].text # prix sans taxe : on recupere tous les elements 'td', on prend le troisieme et on recupere son texte


    price_incl = soup.find_all('td')[3].text # prix avec taxe : se situe juste apres le prix sans taxe

    quant = soup.find_all('td')[5].text # quantité

    li = soup.select('div#product_description')
    descr = li[0].find_all_next('p')[0].text # description



    bc = soup.find_all('ul',{"class":"breadcrumb"})
    cat = bc[0].find_all('a')[2].text # categorie



    rt = soup.find_all('p',{"class":"star-rating"})
    if (rt[0]['class'][1] in rating_titles):
        rating = rt[0]['class'][1] # rating



    url = soup.find('img')['src'] # image URL
    img = "https://books.toscrape.com" + url[5:] # enlever le ../.. de la partie relative de l'URL




    header = ['product_page_url', 'universal_product_code', 'title', 'price_including_tax', 'price_excluding_tax', 'number_available', 'product_description', 'category', 'review_rating', 'image_url']
    fileName = cat + ".csv" # Travel.csv, Horror.csv...
    with open(fileName, mode='a+', newline='', encoding="utf-8") as file:
        print("Saving book : " + title)
        data_writer = csv.writer(file)

        file.seek(0) # on positionne le pointeur au tout debut du fichier

        filesize = os.path.getsize(fileName) #verifier si le fichier et vide

        if filesize == 0: # si le fichier est vide, on ajoute la ligne avec le nom des colonnes puis les data du livre
            data_writer.writerow(header)
            data_writer.writerow([URL, upc, title, price_incl, price_excl, quant, descr, cat, rating, img])

        else: # sinon juste les data du livre car les colonnes sont deja présentes
            data_writer.writerow([URL, upc, title, price_incl, price_excl, quant, descr, cat, rating, img])

        
def get_all_categories() -> dict:
        page = requests.get("http://books.toscrape.com/catalogue/category/books_1/index.html") #on recupere la premiere page
        soup = BeautifulSoup(page.content, "html.parser")
        rootUrl = "http://books.toscrape.com/catalogue/category"
        urls = {}

        bc = soup.find_all('div', {"class": "side_categories"})
        xd = bc[0].find_all('a')
        for result in xd:
            if not result.text.strip() == "Books":
                url = rootUrl + result['href'][2:]
                urls[result.text.strip()] = url

        return urls


def get_books_from_category(category) -> list[str]:
    categories = get_all_categories()

    if category in categories:
        URL = categories[category]
    else:
        return -1
    
    urls = []
    pages = [URL]
    rootUrl = URL[:-10] # URL racine sans le index.html
    
    while pages:
        pageLink = pages.pop(0)
        page = requests.get(pageLink) #on recupere la premiere page
        soup = BeautifulSoup(page.content, "html.parser")
        bc = soup.find_all('div', {"class": "image_container"}) # on recupere toutes les images, elles contiennent un lien vers la page de leur livre
        print("Fetching books for page : " + pageLink)
        for result in bc: # pour chaque resultat, on recupere le lien 'a' qui est dans chaque image
            link = result.find('a')['href']  # catégorie
            url = "https://books.toscrape.com/catalogue" + link[8:] # et on retire les ../../.. au début pour ne plus avoir d'URL relative
            urls.append(url)

        
        print("All books have been fetched\n")
        next_button = soup.find('li', {"class": "next"}) # on verifie si il y a un bouton 'next' sur la page
        if next_button: # si oui, cela veut dire qu'il y a une page suivante avec encore plus de livres pour la catégorie
            next_link = next_button.find('a')['href'] # on recupere le lien de la page suivante
            next_page_url = rootUrl + next_link # et on le colle a la fin de l'url racine de la catégorie pour obtenir un lien complet
            pages.append(next_page_url)  
    return urls

travelBooks = get_books_from_category("Travel")

for book in travelBooks:
    get_book(book)