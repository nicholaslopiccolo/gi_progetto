import preprocessor
from webcrawler import WebCrawler

FILES_PATH = '../Docs/'

def start_crawling(limit=20):
    wc = WebCrawler(limit=limit)
    # Si può passare un url iniziale alle funzioni di run
    wc.run_meetup()
    #wc.run_meetup(initial_url="https://www.meetup.com/find/?location=it--bo--Bologna&source=EVENTS")
    wc.run_eventbrite()
    #wc.run_eventbrite(initial_url="https://www.eventbrite.it/e/biglietti-i-manoscritti-di-qumran-249260694447?aff=ebdssbdestsearch")

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
            pass
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







