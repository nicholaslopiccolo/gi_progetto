"""
Prende in fase di costruzione l'inveted index e fa i controlli in base alle 
query richieste dall'utente.

Whoosh
https://whoosh.readthedocs.io/en/latest/quickstart.html
"""
from whoosh import index
class QuerySystem:
    def __init__(self):
        self.queries = []

    def search(self):
        q = QuerySystem.query(input("Type your query: "))
        self.queries.append(q)
    class query:
        def __init__(self):
            self.str = str
