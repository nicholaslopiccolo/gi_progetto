import re
import os
<<<<<<< HEAD

emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        u"\U00002500-\U00002BEF"  # chinese char
        u"\U00002702-\U000027B0"
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        u"\U0001f926-\U0001f937"
        u"\U00010000-\U0010ffff"
        u"\u2640-\u2642" 
        u"\u2600-\u2B55"
        u"\u200d"
        u"\u23cf"
        u"\u23e9"
        u"\u231a"
        u"\ufe0f"  # dingbats
        u"\u3030"
                      "]+", re.UNICODE)

=======
from pprint import pprint
enc = 'utf-8'
>>>>>>> 2feae9e6604c96e47603f134279e5ca3a6ae1dbd
class extractor:
    def __init__(self,path):
        self.path = path
    
        self.extract()

    def extract(self):
<<<<<<< HEAD
        print(self.path)
        with open(self.path) as f:
            raw_lines = [emoji_pattern.sub(r'', line) for line in f.read().splitlines()]
=======
        with open(self.path,encoding=enc) as f:
            raw_lines = [line for line in f.read().splitlines()]
>>>>>>> 2feae9e6604c96e47603f134279e5ca3a6ae1dbd
            lines = [line for line in raw_lines if line]

        self.url = lines[0]
        self.event_name = lines[1]
        self.date = lines[2]
        self.content = lines[4:]

    def __str__(self):
        return "URL:\n{0}\nEVENT NAME:\n{1}\n\nDATE:\n{2}\n\nCONTENT:\n{3}".format(self.url,self.event_name,self.date,'\n'.join(self.content))

<<<<<<< HEAD


'''e_meetup = extractor("./Docs/www.meetup.com/0.txt")
print(e_meetup)

e_meetup = extractor("../Docs/www.eventbrite.it/0.txt")
print(e_meetup)'''
=======
#e_meetup = extractor("../Docs/www.meetup.com/0.txt")
#print(e_meetup)
#e_meetup = extractor("../Docs/www.eventbrite.it/0.txt")
#print(e_meetup)

def lista_documenti():
    path = '../Docs/'
    return [path+d+'/'+f for d in os.listdir(path) for f in os.listdir(path+d)]

e_list = [print(extractor(file).event_name) for file in lista_documenti()]
>>>>>>> 2feae9e6604c96e47603f134279e5ca3a6ae1dbd
