# -*- coding: utf-8 -*-
import networkx as nx
import matplotlib.pyplot as plt

class SNA:
    __graph = None
    __book = None

    def __init__(self, book):
        self.__graph = nx.Graph()
        self.__book = book




        self.__graph.add_nodes_from(self.__book.get_character_list())
        nx.draw(self.__graph)
        plt.show()
