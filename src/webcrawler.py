from operator import index
from bs4 import BeautifulSoup
import requests, re, os

url_regex = ("((http|https)://)(www.)?" +
             "[a-zA-Z0-9@:%._\\+~#?&//=]" +
             "{2,256}\\.[a-z]" +
             "{2,6}\\b([-a-zA-Z0-9@:%" +
             "._\\+~#?&//=]*)")

domain_regex = ('https?://([A-Za-z_0-9.-]+).*')

class WebCrawler:
    URL_PATTERN = re.compile(url_regex)
    DOMAIN_PATTERN = re.compile(domain_regex)

    def __init__(self,limit=300):
        self.LIMIT = limit
        self.CORPUS_PATH = "../Docs"
        self.links = set()


    @staticmethod
    def get_domain(url):
        return WebCrawler.DOMAIN_PATTERN.search(url).group(1)

    def create_document_meetup(self,soup,url,index): 
        # Crea il documento sfruttanzo la soup (bisogna cercare il contenuto)
        # Il nome del file dev'essere collegato al suo url
        d = "{0}/{1}".format(self.CORPUS_PATH,self.INITIAL_DOMAIN)
        file_name = "{0}/{1}.txt".format(d,index)
        if not os.path.exists(d):
            os.mkdir(d)

        with open(file_name, 'w',encoding='utf-8') as f:
            f.write(url + "\n")
            try:
                f.write(soup.title.string +"\n")
            except AttributeError:
                pass
            
            try:
                f.write(soup.select_one('div[data-testid="event-rsvp-time"]').get_text()+"\n\n")
            except AttributeError:
                f.write('--no date--\n\n')
            try:
                f.write(soup.select_one('div[data-event-label="body"]').get_text())
            except AttributeError:
                f.write('--no body--\n\n')

            print("\nfile created: {0} \nfor the url: {1}".format(file_name,url))

    def create_document_eventbrite(self,soup,url,index): 
        # Crea il documento sfruttanzo la soup (bisogna cercare il contenuto)
        # Il nome del file dev'essere collegato al suo url
        d = "{0}/{1}".format(self.CORPUS_PATH,self.INITIAL_DOMAIN)
        file_name = "{0}/{1}.txt".format(d,index)
        if not os.path.exists(d):
            os.mkdir(d)

        with open(file_name, 'w',encoding='utf-8') as f:
            f.write(url + "\n")
            try:
                f.write(soup.title.string +"\n")
            except AttributeError:
                pass
            
            divs_date = soup.find_all('p',{'data-testid':'event-date'})
            divs_time = soup.find_all('p',{'data-testid':'event-time'})

            try:
                data = "{0}, {1}".format(', '.join(divs_date[0].stripped_strings),', '.join(divs_time[0].stripped_strings))
                f.write(data+"\n\n")
            except Exception:
                f.write('--no date--\n\n')


            try:
                # Rimozione dati inutili riguardanti date e luogo
                div = soup.find_all('div',{'class':'has-user-generated-content'})[0]
                f.write('\n'.join([text for text in div.stripped_strings]))
            except Exception:
                f.write('--no body--\n\n')

            print("\nfile created: {0} \nfor the url: {1}".format(file_name,url))

    def run_meetup(self,initial_url="https://www.meetup.com"): 
        """
        La funziona lancia il crawler che scava nel dominio alla ricerca di:
        contenuto e altri link a cui agganciarsi per le prossime richieste
        """
        self.links = []
        self.INITIAL_URL = initial_url
        self.INITIAL_DOMAIN = WebCrawler.get_domain(self.INITIAL_URL)

        html = requests.get(self.INITIAL_URL).text

        self.links.append(self.INITIAL_URL)
        index = 0

        # Esegue il crawling di LIMIT siti link
        while len(self.links) < self.LIMIT and index < len(self.links):
            soup = BeautifulSoup(html, 'html.parser')
            a_list = soup.find_all("a")

            # Carica solo url corretti
            try: 
                support = { link.get('href') for link in a_list if link.get('href') and re.search(self.URL_PATTERN, link.get('href')) and re.search("/events/",link.get('href')) }
            except TypeError:
                continue
            
            new_links = [link for link in support if WebCrawler.get_domain(link) == self.INITIAL_DOMAIN]
            self.links += new_links

            url = self.links[index]

            print("Crawling: {0}".format(url))
            print("  Found: {0}".format(len(new_links)))
            print("  Total: {0}".format(len(self.links)))

            index += 1

        # Elimina il primo link che di solito non ha all'interno informazioni su un evento specifico
        del self.links[0]

        # Crea i documenti dalla source
        index = 0
                
        for url in self.links[1:]:
            try:
                html = requests.get(url).text
            except Exception:
                continue

            soup = BeautifulSoup(html, 'html.parser')
            self.create_document_meetup(soup,url,index)

            index +=1
            if index > self.LIMIT-1:
                break


    def run_eventbrite(self,initial_url="https://www.eventbrite.it/d/italy--carpi-centro/bologna/?page=1"): 
        """
        La funziona lancia il crawler che scava nel dominio alla ricerca di:
        contenuto e altri link a cui agganciarsi per le prossime richieste
        """
        self.links = []
        self.INITIAL_URL = initial_url
        self.INITIAL_DOMAIN = WebCrawler.get_domain(self.INITIAL_URL)

        html = requests.get(self.INITIAL_URL).text

        self.links.append(self.INITIAL_URL)
        index = 0

        # Esegue il crawling di 300 siti link
        while len(self.links) < self.LIMIT and index < len(self.links):
            soup = BeautifulSoup(html, 'html.parser')
            a_list = soup.find_all("a")

            # Carica solo url corretti
            try: 
                support = { link.get('href') for link in a_list if link.get('href') and re.search(self.URL_PATTERN, link.get('href')) and re.search("/e/",link.get('href')) }
            except TypeError:
                continue

            new_links = [link for link in support if WebCrawler.get_domain(link) == self.INITIAL_DOMAIN]
            self.links += new_links

            url = self.links[index]
            

            print("Crawling: {0}".format(url))
            print("  Found: {0}".format(len(new_links)))
            print("  Total: {0}".format(len(self.links)))

            index += 1

        # Crea i documenti dalla source
        index = 0

        for url in self.links[1:]:
            try:
                html = requests.get(url).text
            except Exception:
                continue

            soup = BeautifulSoup(html, 'html.parser')
            self.create_document_eventbrite(soup,url,index)

            index +=1
            
            if index > self.LIMIT-1:
                break