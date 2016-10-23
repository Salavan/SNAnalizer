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

        self.__graph = self.build_graph_from_paragraphs()
        # self.__graph = self.build_graph_from_sentences()


    def add_nodes(self, graph):
        character_list = self.__book.get_character_list()
        graph.add_nodes_from(character_list)

    def add_eages(self, graph, matrix):
        rev_character_map = self.__book.get_rev_characters_map()

        for x in range(len(matrix)):
            for y in range(len(matrix)):
                if x != y and matrix[x][y] != 0:
                    for _ in range(int(matrix[x][y])):
                        graph.add_edge(rev_character_map[x], rev_character_map[y]) #add_weighted_edge

    def build_graph_from_chapter(self, graph, matrix):
        self.add_eages(graph, matrix)

    def get_nodes_pos(self, whole_graph):
        return nx.fruchterman_reingold_layout(whole_graph)

    def build_whole_graph(self, matrices):
        whole_graph = nx.Graph()
        self.add_nodes(whole_graph)
        for i in range(len(matrices)):
            self.build_graph_from_chapter(whole_graph, matrices[i])
        return whole_graph

    def build_graph(self, matrices, graph, dir = None):
        self.add_nodes(graph)

        if dir:
            pos = self.get_nodes_pos(self.build_whole_graph(matrices))

        for i in range(len(matrices)):
            self.build_graph_from_chapter(graph, matrices[i])
            if dir:
                self.draw_graph(graph, pos, dir, i)

    def build_graph_from_paragraphs(self):
        graph = nx.Graph()
        self.build_graph(self.__book.get_paragraphs_matrices(), graph, "ByParagraphs")

        return graph

    def build_graph_from_sentences(self):
        graph = nx.Graph()
        self.build_graph(self.__book.get_sentences_matrices(), graph, "BySentences")

        return graph

    def draw_graph(self, graph, pos, dir, file_name):
        nx.draw_networkx(graph, pos = pos, node_size=1000, node_color='silver', width=1, font_size=8)
        plt.savefig(os.path.join("..", "data", "graphs", "{}".format(dir), "{}".format(file_name)))
        plt.clf()

