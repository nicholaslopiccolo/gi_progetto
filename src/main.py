from preprocessor import Preprocessor
from webcrawler import WebCrawler

FILES_PATH = '../files/'

# Fase di crwling e ottenimento corpus dei documenti
# potremmo usare i thread per parallelizzare le operazioni


# Fase di preprocessing del corpus dei documenti
pre = Preprocessor()
example = 'text to try the position counting of characters. \n what do i do?'
pre.create_trie(FILES_PATH + 'File1.txt')
pre.create_trie(FILES_PATH + 'Doc2.txt')
pre.create_trie(FILES_PATH + 'Text3.txt')
print(pre.inv_index)






