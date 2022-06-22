from logging import exception
import os, os.path
from whoosh import index
from whoosh.fields import *
from whoosh.qparser import MultifieldParser
from whoosh import scoring
from preprocessor import preprocess


DOCPATH = os.path.abspath(os.getcwd()) + "\Docs"
SCHEMA = Schema(title=TEXT(stored=True),body=TEXT(stored=True))

#funzione che legge un documento e lo aggiunge all'indice secondo lo schema, per path si intende il nome del documento.
#Ho presupposto che questi documenti vadano preprocessati
def add_doc(writer, path):
  fileobj = open(path, "r",encoding='utf-8')
  content = fileobj.read()
  content = preprocess(content)
  fileobj.close()
  writer.add_document(title=path, body=content)


#oggetto schema serve per definire come viene salvato l'indice 
#schema = Schema(id=NUMERIC, title=TEXT(stored=True), body=TEXT(stored=True), url=TEXT(stored=True))

#creo directory degli indici, per ogni cartella in Docs creo un indice
def create_index():
  if not os.path.exists("indexdir"):
      os.mkdir("indexdir")
  for dir in os.listdir(DOCPATH):
    ix = index.create_in("indexdir", SCHEMA,indexname=dir)
    writer = ix.writer()
    for doc in os.listdir(os.path.join(DOCPATH,dir)):
      add_doc(writer,os.path.join(DOCPATH,dir,doc))
    writer.commit()

def search_index(indexname,keyword):
  ix = index.open_dir("indexdir",indexname=indexname)
  q = MultifieldParser(['title', 'body'], schema=ix.schema)
  keyquery = preprocess(keyword.lower())
  query = q.parse(keyquery)
  with ix.searcher(weighting=scoring.TF_IDF()) as searcher:
        results = searcher.search(query, limit=30)
        for r in results:
          print(r)

if __name__ == '__main__':
  create_index()
  search_index("www.meetup.com",preprocess("concert"))

  '''
  # Only show documents in the "rendering" chapter
    allow_q = query.Term("chapter", "rendering")
    # Don't show any documents where the "tag" field contains "todo"
    restrict_q = query.Term("tag", "todo")

    results = s.search(user_q, filter=allow_q, mask=restrict_q)
    '''
