from bs4 import BeautifulSoup
import requests, re

regex = ("((http|https)://)(www.)?" +
             "[a-zA-Z0-9@:%._\\+~#?&//=]" +
             "{2,256}\\.[a-z]" +
             "{2,6}\\b([-a-zA-Z0-9@:%" +
             "._\\+~#?&//=]*)")

class WebCrawler:
    def __init__(self,initial_url:str,corpus_path:str,limit:int = None) -> None:
        self.INITIAL_URL = initial_url
        self.URL_REGEX = re.compile(regex)
        self.LIMIT = limit | 300
        self.CORPUS_PATH = corpus_path

        self.counter = 0
        self.links = []
    
    # TO DO
    def create_document(self,soup,url) -> None: 
        # Crea il documento sfruttanzo la soup (bisogna cercare il contenuto)
        # Il nome del file dev'essere collegato al suo url
        pass

    def run(self) -> None: 
        """
        La funziona lancia il crawler che scava nel dominio alla ricerca di:
        contenuto e altri link a cui agganciarsi per le prossime richieste
        """
        html = requests.get(self.INITIAL_URL).text
        self.links.append(self.INITIAL_URL)
        self.counter += 1

        # Esegue il crawling di 300 siti link
        while self.counter < self.LIMIT-1:
            soup = BeautifulSoup(html, 'html.parser')
            a_list = soup.find_all("a")

            # Carica solo url corretti
            new_links = [link.get('href') for link in a_list if(re.search(self.URL_REGEX, link.get('href')))]
            self.links += new_links

            url = self.links[self.counter]
            # Create file
            self.create_document(soup,url)

            print("Crawling: {0}".format(url))
            print("  Found: {0}".format(len(new_links)))
            print("  Total: {0}".format(len(self.links)))

            self.counter += 1

            # Un generico errore durante richiesta
            try:
                html = requests.get(url).text
            except Exception as e:
                print(e)

def test():
    INITIAL_URL = "https://www.google.it"

    wc = WebCrawler(initial_url=INITIAL_URL, corpus_path="../files/", limit=10)
    wc.run()

#test()
