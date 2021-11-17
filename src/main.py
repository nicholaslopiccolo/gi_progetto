from preprocessor import Preprocessor

FILES_PATH = '../files/'

pre = Preprocessor()
example = 'text to try the position counting of characters. \n what do i do?'
pre.create_trie(FILES_PATH + 'File1.txt')
pre.create_trie(FILES_PATH + 'Doc2.txt')
pre.create_trie(FILES_PATH + 'Text3.txt')
print(pre.inv_index)
