import networkx as nx
from src.AliceBook import AliceBook

class SNA:
    graph = None

    def __init__(self):
        self.graph = nx.Graph()
        self.book = AliceBook()
        self.graph.add_nodes_from(self.book.characters)
        nx.draw(self.graph)
        print("xxx")
        self.book.findEvents(self.book.chapters_by_sentences)
