import string
import nltk
from nltk.corpus import stopwords
#nltk.download('book')
#nltk.download('stopwords')
#nltk.download('omw-1.4')
from nltk.stem.porter import PorterStemmer
from nltk.stem.lancaster import LancasterStemmer
from nltk.corpus import wordnet as wn

def removePunctuation(tokens):
        exclude = set(string.punctuation)
        return [x for x in tokens if x not in exclude]
def removeStopWords(tokens):
    return [x for x in tokens if x not in stopwords.words('english')]

#classe che implementa varie fasi di preprocessing sul testo using python nltk modules
class Preprocessor():
    def __init__(self):
        #self.porter =  PorterStemmer()
        self.lancaster = LancasterStemmer()
        self.lemmatizer = nltk.WordNetLemmatizer()
        self.inv_index = {}

#funzione che accetta un testo e restituisce una lista di token del testo
    def tokenize(self,text):
        return nltk.word_tokenize(text.lower())

#Funzione lemmatizzatrice, riceve lista di tokens e restituisce lista di lemmi senza stopwords
    def lemmatize(self,tokens,lang='english'):
        return [self.lemmatizer.lemmatize(t) for t in tokens if not t in stopwords.words(lang)]

#Funzione Stemmer using Lancaster/Porter, restituisce lista con stem di lista di tokens passati come parametro
    def stem(self,tokens):
        #stems = [self.porter.stem(t) for t in tokens]
        return [self.lancaster.stem(t) for t in tokens]

#Function that tags every token passed as parameter and returns them in a list of tuples(token,tag)
    def tag(self,tokens):
        return nltk.pos_tag(tokens)
    
#Function disambiguating the terms passed as parameters, determining the right sense using wupalmer similarity
    def disambiguateTerms(self,terms):
            for t_i in terms:    # t_i is target term
                    selSense = None
                    selScore = 0.0
    #        print(wn.synsets(t_i,wn.NOUN))
                    for s_ti in wn.synsets(t_i, wn.NOUN):
                            score_i = 0.0
                            for t_j in terms:    # t_j term in t_i's context window
                                    if (t_i==t_j):
                                            continue
                                    bestScore = 0.0
                                    for s_tj in wn.synsets(t_j, wn.NOUN):
                                            tempScore = s_ti.wup_similarity(s_tj)
                                            if (tempScore>bestScore):
                                                    bestScore=tempScore
                                    score_i = score_i + bestScore
                            if (score_i>selScore):
                                    selScore = score_i
                                    selSense = s_ti
                    if (selSense is not None):
                            print(t_i,": ",selSense,", ",selSense.definition())   
                            print("Score: ",selScore)
                    else:
                            print(t_i,": --")

#Function that creates or updates the inverted index (trie) of the docfile tokenized with a word-based posting list
#(facilita proximity search, alternativa è docbased con nomefile e occorrenze)
#non tokenizzato-> da correggere perche per esempio 'parola,' e 'parola' li salva distintamente, ma noi vogliamo che venga tolta la virgola e salvata l'occorrenza per 'parola' correttamente
    def create_trie(self,docfile):
        file = open(docfile,'r')
        trie = {}
        count = 1
        for line in file:
            for word in line.split():
                token = self.lancaster.stem(self.lemmatizer.lemmatize(''.join(removePunctuation(word.lower()))))
                print(token)
                if not token in stopwords.words('english'):
                    if token not in trie:
                        trie[token] = [docfile,count]
                    else:
                        trie[token].append(count)
                count += len(word)+1
        for token in trie:
            if token not in self.inv_index:
                self.inv_index[token] = []
                self.inv_index[token].append(trie[token])
            else:
                self.inv_index[token].append(trie[token])
            

if __name__=='__main__':
    pre = Preprocessor()
    example = 'text to try the position counting of characters. \n what do i do?'
    pre.create_trie('File1.txt')
    pre.create_trie('Doc2.txt')
    pre.create_trie('Text3.txt')
    print(pre.inv_index)
