import os, os.path
from whoosh import index
from whoosh.fields import *
#from . import Preprocessor

DOCPATH = os.path.abspath(os.getcwd()) + "\Docs"
SCHEMA = Schema(title=TEXT(stored=True),body=TEXT(stored=True))

def add_doc(writer, path):
  fileobj = open(path, "rb")
  content = fileobj.read()
  fileobj.close()
  writer.add_document(title=path, content=content)


def get_schema():
  return Schema(title=TEXT(stored=True),body=TEXT(stored=True))

#oggetto schema serve per definire come viene salvato l'indice 
#schema = Schema(id=NUMERIC, title=TEXT(stored=True), body=TEXT(stored=True), url=TEXT(stored=True))
#creo directory che contiene inverted index
def create_index():
  if not os.path.exists("indexdir"):
      os.mkdir("indexdir")

#oggetto index a partire dallo schema
  ix = index.create_in("indexdir", SCHEMA)
#ix = index.open_dir("indexdir", indexname='')
  writer = ix.writer()
  for doc in os.listdir(DOCPATH):
    add_doc(writer,doc)
#commit all' index
  writer.commit()

if __name__ == '__main__':
  create_index()


#templates commentati di codici presi da internet 
'''
def clean_index(dirname):
  # Always create the index from scratch
  ix = index.create_in(dirname, schema=get_schema())
  writer = ix.writer()

  # Assume we have a function that gathers the filenames of the
  # documents to be indexed
  for path in my_docs():
    add_doc(writer, path)

  writer.commit()


def get_schema()
  return Schema(path=ID(unique=True, stored=True), content=TEXT)


def add_doc(writer, path):
  fileobj = open(path, "rb")
  content = fileobj.read()
  fileobj.close()
  writer.add_document(path=path, content=content)

#da passare al creatore dell'indice docid,titolo,body preprocessato e url da cui deriva
'''


'''
for p in pagine:
    writer.add_document(id=p.getId(), title=preProcess(p.getTitolo().lower()), body=preProcess(p.getContenuto().lower()), url=p.getURL())
'''