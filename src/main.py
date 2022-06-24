from concurrent.futures import thread
from indexing_whoosh import ranking_merged
import preprocessor
from webcrawler import WebCrawler
from threading import Thread
from extractor import extractor

FILES_PATH = '../Docs/'

def start_crawling(limit=20):
    wc = WebCrawler(limit=limit)
    # Si può passare un url iniziale alle funzioni di run
    t1 = Thread(target = wc.run_meetup())
    t2 = Thread(target = wc.run_eventbrite())

    t1.start()
    t2.start()
    t2.join()
    t1.join()
    #wc.run_meetup(initial_url="https://www.meetup.com/find/?location=it--bo--Bologna&source=EVENTS")
    #wc.run_eventbrite(initial_url="https://www.eventbrite.it/e/biglietti-i-manoscritti-di-qumran-249260694447?aff=ebdssbdestsearch")

def submit_query(query):
    results = ranking_merged(query)
    if results == []:
        print("La query non ha dato risultati utili, provare a riformulare \n")
        return
    count = 0
    for x in results:
        print(f"\n Result {count+1}: \n")
        print(extractor(x['file']))
        count += 1
        if count == 10:
            if (input("show more results? (y/n) \n") == "n"):
                return

def menu():
    c = input("""
    1) WebCrawling (Scarica i dati dalle due sorgenti)
    2) Esegui una query
    3) Ranking delle ultime query
    4) Benchmark
    5) Exit
    """)
    try:

        x = int(c)
        if x==1:
            limit = input("Insert the limit of the search (integer number):")
            start_crawling(limit=int(limit))
        elif x==2:
            submit_query(input("insert query \n"))
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







