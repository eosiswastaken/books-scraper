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
        data_writer = csv.writer(file)

        file.seek(0) # on positionne le pointeur au tout debut du fichier

        filesize = os.path.getsize(fileName) #verifier si le fichier et vide

        if filesize == 0: # si le fichier est vide, on ajoute la ligne avec le nom des colonnes puis les data du livre
            data_writer.writerow(header)
            data_writer.writerow([URL, upc, title, price_incl, price_excl, quant, descr, cat, rating, img])

        else: # sinon juste les data du livre car les colonnes sont deja présentes
            data_writer.writerow([URL, upc, title, price_incl, price_excl, quant, descr, cat, rating, img])


        

get_book("http://books.toscrape.com/catalogue/its-only-the-himalayas_981/index.html")