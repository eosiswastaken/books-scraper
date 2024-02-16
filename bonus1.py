import csv
import requests
import os
import glob
from bs4 import BeautifulSoup
import uuid
import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd

def create_data_file():
    print("Creating data file...")
    booksPerCategory = {}
    pricesPerCategory = {}
    if not os.path.exists("data.csv"):
        for file in glob.glob("*.csv"): # on recupere toues les fichiers .csv
            with open(file, mode='r', newline='', encoding="utf-8") as f:
                reader = csv.DictReader(f, delimiter=',')
                for row in reader: # on lit ligne par ligne le fichier .csv actuel
                    if row['category'] in booksPerCategory: # et on ajoute +1 au nombre de livres correspondant a la catégorie
                        booksPerCategory[row['category']] += 1
                    else:
                        booksPerCategory[row['category']] = 1

                    if row['category'] in pricesPerCategory: # et on ajoute le prix au calcul de la moyenne des prix pour la catégorie du livre
                        pricesPerCategory[row['category']].append(float(row['price_including_tax'][1:]))
                    else:
                        pricesPerCategory[row['category']] = [float(row['price_including_tax'][1:])]

        for category in pricesPerCategory: # une fois tous les prix dans la liste, on calcule la moyenne de prix par catégorie
            pricesPerCategory[category] = sum(pricesPerCategory[category]) / len(pricesPerCategory[category])

    

        if not os.path.exists("stats"): #si le dossier 'stats' n'exsite pas, on le crée, puis on 'cd' dedans
            os.mkdir("stats")
        os.chdir("stats")
        with open("data.csv", mode="w", newline='') as f: # on crée un fichier data.csv dans le dossier 'stats'
            header = ['category','books_count','average_price']
            data_writer = csv.writer(f)
            data_writer.writerow(header)
            for category in booksPerCategory: # et on y écrit nos datas : category,books_count,average_price
                data_writer.writerow([category,booksPerCategory[category],pricesPerCategory[category]])
    print("Done !")



def pie_chart():
    data = pd.read_csv("data.csv") # pandas is better when you have to read csvs and prepare your data to be displayedd with mpl
    books = data['books_count']
    labels = data['category']

    fig, ax = plt.subplots()
    ax.pie(books, labels=labels, startangle=90, autopct='%1.0f%%') # autopct calculate s the percentage of each part using a formatting string
    ax.axis('equal')
    plt.title("number of books per category")
    plt.show()

def bar_chart():
    data = pd.read_csv("data.csv") # (presque) same a pie chart 
    books = data['average_price']
    labels = data['category']

    fig, ax = plt.subplots()
    ax.bar(labels,books) # giving the labels and data to the bar function and thats it
    plt.title("average book price per category")
    plt.show()

create_data_file()
pie_chart()
bar_chart()