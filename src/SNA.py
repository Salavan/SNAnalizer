# -*- coding: utf-8 -*-
import os

import networkx as nx
import matplotlib.pyplot as plt

class SNA:
    __graph = None
    __book = None

    def __init__(self, book):
        self.__graph = nx.Graph()
        self.__graph2 = nx.Graph()
        self.__book = book

        self.build_graph_from_paragraphs()
        # self.build_graph_from_sentences()




    def add_nodes(self):
        character_list = self.__book.get_character_list()

        self.__graph.add_nodes_from(character_list)
        self.__graph2.add_nodes_from(character_list)


    def add_eages(self, matrices, dir = None):
        rev_character_map = self.__book.get_rev_characters_map()

        for i in range(len(matrices)):
            for x in range(len(matrices[i])):
                for y in range(len(matrices[i])):
                    if x != y and matrices[i][x][y] != 0:
                        for _ in range(int(matrices[i][x][y])):
                            self.__graph.add_edge(rev_character_map[x], rev_character_map[y]) #add_weighted_edge

            self.draw_graph(dir, i)

    def add_eages2(self, matrices, dir = None):
        rev_character_map = self.__book.get_rev_characters_map()

        for i in range(len(matrices)):
            for x in range(len(matrices[i])):
                for y in range(len(matrices[i])):
                    if x != y and matrices[i][x][y] != 0:
                        for _ in range(int(matrices[i][x][y])):
                            self.__graph2.add_edge(rev_character_map[x], rev_character_map[y]) #add_weighted_edge


    def build_graph(self, matrices, dir = None):
        self.add_nodes()
        self.add_eages2(matrices)
        self.global_pos=nx.fruchterman_reingold_layout(self.__graph2)
        self.add_eages(matrices, dir)

    def build_graph_from_paragraphs(self):
        self.build_graph(self.__book.get_paragraphs_matrices(), "ByParagraphs")

    def build_graph_from_sentences(self):
        self.build_graph(self.__book.get_sentences_matrices(), "BySentences")

    def draw_graph(self, dir, file_name):
        nx.draw_networkx(self.__graph, pos = self.global_pos, node_size=1000, node_color='silver', width=1, font_size=8)
        plt.savefig(os.path.join("..", "data", "graphs", "{}".format(dir), "{}".format(file_name)))
        plt.clf()