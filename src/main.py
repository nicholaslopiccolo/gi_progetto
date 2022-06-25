import shutil
from preprocessor import preprocess_query
from indexing_whoosh import ranking_merged
import os
from webcrawler import WebCrawler
from extractor import extractor
from indexing_whoosh import create_index

FILES_PATH = '../Docs/'

def clean_docs():
    for dir in os.listdir(FILES_PATH):
        shutil.rmtree(os.path.join(FILES_PATH,dir), ignore_errors=True)

def start_crawling(limit=20):
    clean_docs()
    wc = WebCrawler(limit=limit)

    # Si può passare un url iniziale alle funzioni di run
    wc.start_crawling("https://www.meetup.com/find/?source=EVENTS")
    wc.start_crawling("https://www.eventbrite.com/d/ny--new-york/events/")
    #wc.remove_double_files()

    create_index()

def submit_query(query):
    results = ranking_merged(query)
    if results == []:
        print("La query non ha dato risultati utili, provare a riformulare \n")
        return
    count = 0
    for x in results:
        print(f"\n Result {count+1}: \n")
        print(extractor(x['file']))
        print(f" \n score:{x['score']}")
        count += 1
        if count == 10:
            if (input("show more results? (y/n) \n") == "n"):
                return

def menu():
    c = input("""
    1) WebCrawling (Scarica i dati dalle due sorgenti)
    2) Esegui una query
    3) Cronologia delle ultime query
    4) Benchmark
    5) Exit
    """)
    try:

        x = int(c)
        if x==1:
            limit = input("Insert the limit of the search (integer number):")
            start_crawling(limit=int(limit))
        elif x==2:
            submit_query(preprocess_query(input("insert query \n")))
        elif x==3:
            pass
        elif x==4:
            pass
        elif x==5:
            exit()

    except ValueError:
        print("Insert only numbers in the menu please.")
        menu()

while True:
    menu()

#FILES_PATH = '../files/'

# Fase di crwling e ottenimento corpus dei documenti
# potremmo usare i thread per parallelizzare le operazioni







