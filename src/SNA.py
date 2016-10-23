# -*- coding: utf-8 -*-
import os

import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

max_edge_width = 5
max_node_size = 10000

class SNA:
    __graph = None
    __book = None
    __characters_influence_per_chapter = None
    __chapters_graphs = []

    def __init__(self, book):
        self.__book = book

        self.prepare_data_for_graph(self.__book.get_paragraphs_matrices())
        print(self.__characters_influence_per_chapter)
        # self.build_graph_from_paragraphs()
        self.build_graph_from_sentences()

        pos = self.get_nodes_pos(nx.compose_all(self.__chapters_graphs))

        # for i in range(len(self.__chapters_graphs)):
        #     self.draw_chapter_graph(i, "ByParagraphs", pos)

        for i in range(len(self.__chapters_graphs)):
            self.draw_chapter_graph(i, "BySentences", pos)



    def add_nodes(self, graph):
        character_list = self.__book.get_character_list()
        graph.add_nodes_from(character_list)

    def add_edges(self, graph, matrix):
        rev_character_map = self.__book.get_rev_characters_map()

        for x in range(len(matrix)):
            for y in range(len(matrix)):
                if x != y and matrix[x][y] != 0:
                    for _ in range(int(matrix[x][y])):
                        try:
                            graph.edge[rev_character_map[x]][rev_character_map[y]]['weight'] += 1
                            graph.edge[rev_character_map[y]][rev_character_map[x]]['weight'] += 1
                        except:
                            graph.add_edge(rev_character_map[x], rev_character_map[y], weight=1)
                            graph.add_edge(rev_character_map[y], rev_character_map[x], weight=1)

    def build_graph_from_chapter(self, graph, matrix):
        self.add_edges(graph, matrix)

    def get_nodes_pos(self, whole_graph):
        return nx.spring_layout(whole_graph, k=1,iterations=20)

    def build_whole_graph(self, matrices):
        whole_graph = nx.Graph()
        self.add_nodes(whole_graph)
        for i in range(len(matrices)):
            self.build_graph_from_chapter(whole_graph, matrices[i])
        return whole_graph

    def build_graphs(self, matrices):
        for i in range(len(matrices)):
            tmp_graph = nx.Graph()
            self.build_graph_from_chapter(tmp_graph, matrices[i])
            self.__chapters_graphs.append(tmp_graph)

    def build_graph_from_paragraphs(self):
        self.build_graphs(self.__book.get_paragraphs_matrices())

    def build_graph_from_sentences(self):
        self.build_graphs(self.__book.get_sentences_matrices())

    def draw_chapter_graph(self, chap, dir, pos = None):
        graph = self.__chapters_graphs[chap]

        character_map = self.__book.get_characters_map()

        nodes_size = np.ones(graph.number_of_nodes())*max_node_size

        for n in graph.nodes():
            nodes_size[graph.nodes().index(n)] *= self.__characters_influence_per_chapter[chap][character_map[n]]

        edges = graph.edges()
        weights = [graph[u][v]['weight'] for u,v in edges]*10

        if pos:
            nx.draw_networkx(graph, pos = pos, node_size=nodes_size, node_color='silver', width=weights, font_size=8)

            xs = [p[0] for p in pos.values()]
            ys = [p[1] for p in pos.values()]
            lim_buffor = 0.1

            axes = plt.gca()
            axes.set_xlim([min(xs)-lim_buffor, max(xs)+lim_buffor])
            axes.set_ylim([min(ys)-lim_buffor, max(ys)+lim_buffor])
        else:
            nx.draw_networkx(graph, node_size=nodes_size, node_color='silver', width=weights, font_size=8)

        plt.savefig(os.path.join("..", "data", "graphs", "{}".format(dir), "{}".format(chap)))
        plt.clf()



    def prepare_data_for_graph(self, event_matrices):
        character_map = self.__book.get_characters_map()

        characters_influence_per_chapter = {}

        for chapter in range(len(event_matrices)):
            matrix = event_matrices[chapter]

            characters_influence = {}
            for character in character_map.values():
                characters_influence[character] = np.sum(matrix[character])

            characters_influence_sum = sum(characters_influence.values())
            for character in character_map.values():
                characters_influence[character] /= characters_influence_sum

            characters_influence_per_chapter[chapter] = characters_influence
        self.__characters_influence_per_chapter  = characters_influence_per_chapter




