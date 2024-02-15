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
        print("Enregistrement du livre " + title)
        data_writer = csv.writer(file)

        file.seek(0) # on positionne le pointeur au tout debut du fichier

        filesize = os.path.getsize(fileName) #verifier si le fichier et vide

        if filesize == 0: # si le fichier est vide, on ajoute la ligne avec le nom des colonnes puis les data du livre
            data_writer.writerow(header)
            data_writer.writerow([URL, upc, title, price_incl, price_excl, quant, descr, cat, rating, img])

        else: # sinon juste les data du livre car les colonnes sont deja présentes
            data_writer.writerow([URL, upc, title, price_incl, price_excl, quant, descr, cat, rating, img])


        



def get_books_from_category(URL) -> list[str]:
    urls = []
    pages = [URL]
    rootUrl = URL[:-10] # URL racine sans le index.html
    
    while pages:
        page = requests.get(pages.pop(0)) #on recupere la premiere page
        soup = BeautifulSoup(page.content, "html.parser")
        bc = soup.find_all('div', {"class": "image_container"}) # on recupere toutes les images, elles contiennent un lien vers la page de leur livre
        print("Récupération des livres pour cette page... (" + rootUrl + ")")
        for result in bc: # pour chaque resultat, on recupere le lien 'a' qui est dans chaque image
            link = result.find('a')['href']  # catégorie
            url = "https://books.toscrape.com/catalogue" + link[8:] # et on retire les ../../.. au début pour ne plus avoir d'URL relative
            urls.append(url)

        
        print("Tous les livres de la page ont été récupérés")
        next_button = soup.find('li', {"class": "next"}) # on verifie si il y a un bouton 'next' sur la page
        if next_button: # si oui, cela veut dire qu'il y a une page suivante avec encore plus de livres pour la catégorie
            next_link = next_button.find('a')['href'] # on recupere le lien de la page suivante
            next_page_url = rootUrl + next_link # et on le colle a la fin de l'url racine de la catégorie pour obtenir un lien complet
            pages.append(next_page_url)  
    return urls



def download_all_covers() -> None:
    cwd = os.getcwd() # on stocke le dossier ou on est pour y revenir plus tard
    for file in glob.glob("*.csv"): # un glob est une collection de fichiers, ici on utilise "*.csv" pour recuperer tous les fichiers finissant en .csv
        with open(file, mode='r', newline='', encoding="utf-8") as f:
            print("Enregistrement des images pour la catégorie " + file[:-4] + "...")
            reader = csv.DictReader(f, delimiter=',')

            for row in reader: # pour chaque ligne de notre fichier CSV
                if not os.path.exists("images"): #si le dossier 'images' n'exsite pas, on le crée, puis on 'cd' dedans
                    os.mkdir("images")
                os.chdir("images")
                img_data = requests.get(row["image_url"]).content # on recupere l'URL de l'image pour cette colonne et on effectue une requete a l'URL de l'image
                imageName =  file[:-4] + "_" + str(uuid.uuid4())[:8] + ".jpg" # on nomme l'image avec : sa catégorie, puis 8 caractere aléatoires grace au module uuid, et l'extension de fichier
                with open(imageName, 'wb') as handler: # on ouvre le fichier comportant le nom de l'image 
                    handler.write(img_data) # et on y écrit le contenu de la requete (l'image) : l'image est téléchargée
                    print("Image téléchargée ! (" + imageName + ")")
                os.chdir(cwd) # on retourne dans le dossier ou sont nos fichiers .csv avant de retourner dans la boucle
            

travelBooks = get_books_from_category("http://books.toscrape.com/catalogue/category/books/travel_2/index.html")

fantasyBooks = get_books_from_category("http://books.toscrape.com/catalogue/category/books/fantasy_19/index.html")

allBooks = travelBooks + fantasyBooks
for book in allBooks:
    get_book(book)

download_all_covers()