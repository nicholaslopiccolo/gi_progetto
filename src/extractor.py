import re
import os
from pprint import pprint
from preprocessor import preprocess

enc = 'utf-8'
class extractor:
    def __init__(self,path):
        self.path = path
    
        self.extract()

    def extract(self):
        with open(self.path,encoding=enc) as f:
            raw_lines = [line for line in f.read().splitlines()]
            lines = [line for line in raw_lines if line]

        self.url = lines[0]
        self.event_name = preprocess(lines[1])
        self.date = lines[2]
        self.content = preprocess(str(lines[4:]))

    def __str__(self):
        return "URL:\n{0}\nEVENT NAME:\n{1}\n\nDATE:\n{2}\n\nCONTENT:\n{3}".format(self.url,self.event_name,self.date,'\n'.join(self.content))

#e_meetup = extractor("../Docs/www.meetup.com/0.txt")
#print(e_meetup)
#e_meetup = extractor("../Docs/www.eventbrite.it/0.txt")
#print(e_meetup)

def lista_documenti():
    path = '../Docs/'
    return [path+d+'/'+f for d in os.listdir(path) for f in os.listdir(path+d)]

#e_list = [print(extractor(file).event_name) for file in lista_documenti()]
