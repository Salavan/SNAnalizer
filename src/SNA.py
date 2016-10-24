# -*- coding: utf-8 -*-
import copy
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
    __time_chapters_graphs = []

    def __init__(self, book):
        self.__book = book

        case  = 0

        if case == 1: #paragraphs
            self.prepare_data_for_graph(self.__book.get_paragraphs_matrices())
            self.build_graph_from_paragraphs()
            pos = self.get_nodes_pos(nx.compose_all(self.__chapters_graphs))
            time_pos = self.get_nodes_pos(nx.compose_all(self.__time_chapters_graphs))

            #TODO: use this :p
            # http://networkx.readthedocs.io/en/networkx-1.11/reference/algorithms.vitality.html?highlight=weight
            # degree_centrality = nx.degree_centrality(self.__chapters_graphs[i])
            # closeness_centrality = nx.closeness_centrality(self.__chapters_graphs[i])
            # eigenvector_centrality = nx.eigenvector_centrality_numpy(self.__chapters_graphs[i])

            for i in range(len(self.__chapters_graphs)):
                self.draw_chapter_graph(i, "ByParagraphs", pos)
            for i in range(len(self.__time_chapters_graphs)):
                self.draw_chapter_graph(i, "ByParagraphsWithTime", time_pos, True)
            self.draw_chapter_graph("whole", "ByParagraphs", pos)

        else: #sentences
            self.prepare_data_for_graph(self.__book.get_sentences_matrices())
            self.build_graph_from_sentences()
            pos = self.get_nodes_pos(nx.compose_all(self.__chapters_graphs))
            time_pos = self.get_nodes_pos(nx.compose_all(self.__time_chapters_graphs))
            for i in range(len(self.__chapters_graphs)):
                self.draw_chapter_graph(i, "BySentences", pos)
            for i in range(len(self.__time_chapters_graphs)):
                self.draw_chapter_graph(i, "BySentencesWithTime", time_pos, True)

            self.draw_chapter_graph("whole", "BySentences", pos)


    def add_nodes(self, graph):
        character_list = self.__book.get_character_list()
        graph.add_nodes_from(character_list)

    def add_weighted_edges(self, graph, matrix):
        rev_character_map = self.__book.get_rev_characters_map()

        for x in range(len(matrix)):
            for y in range(len(matrix)):
                if x != y and matrix[x][y] != 0:
                    graph.add_edge(rev_character_map[x], rev_character_map[y], weight=int(matrix[x][y]))

    def build_graph_from_chapter(self, graph, matrix):
        self.add_weighted_edges(graph, matrix)

    def get_nodes_pos(self, whole_graph):
        return nx.spring_layout(whole_graph, k=1,iterations=20)

    def build_whole_graph(self, matrices):
        whole_graph = nx.Graph()
        self.add_nodes(whole_graph)
        for i in range(len(matrices)):
            self.build_graph_from_chapter(whole_graph, matrices[i])
        return whole_graph

    def combined_time_graphs(self, A, B, weightA = 1, weightB=2):
        C = nx.Graph()
        for u,v,hdata in A.edges_iter(data=True):
            new_attributes = dict((key, value*weightA) if key == 'weight' else (key, value) for key,value in hdata.items())
            C.add_edge(u, v, new_attributes)

        for u,v,hdata in B.edges_iter(data=True):
            if not (u in C and v in C[u]):
                C.add_edge(u, v, hdata)
            else:
                new_attributes = dict((key, value*weightB+C[u][v]['weight']) if key == 'weight' else (key, value) for key,value in hdata.items())
                C.add_edge(u, v, new_attributes)
        return C

    def build_graphs(self, matrices):
        rev_character_map = self.__book.get_rev_characters_map()
        prev_graph = None

        for i in range(len(matrices)):
            tmp_graph = nx.Graph()
            self.build_graph_from_chapter(tmp_graph, matrices[i])
            self.__chapters_graphs.append(tmp_graph)

            if prev_graph:
                self.__time_chapters_graphs.append(self.combined_time_graphs(prev_graph, tmp_graph))
                prev_graph = self.__time_chapters_graphs[-1]
            else:
                self.__time_chapters_graphs.append(tmp_graph)
                prev_graph = tmp_graph



    def build_graph_from_paragraphs(self):
        self.build_graphs(self.__book.get_paragraphs_matrices())

    def build_graph_from_sentences(self):
        self.build_graphs(self.__book.get_sentences_matrices())

    def draw_chapter_graph(self, chap, dir, pos = None, include_time = False):
        graph = None
        if chap == "whole":
            graph = nx.compose_all(self.__chapters_graphs)
        elif include_time:
            graph = self.__time_chapters_graphs[chap]
        else:
            graph = self.__chapters_graphs[chap]

        character_map = self.__book.get_characters_map()

        nodes_size = np.ones(graph.number_of_nodes())*max_node_size

        for n in graph.nodes():
            if chap == "whole":
                nodes_size[graph.nodes().index(n)] *= self.__whole_characters_influence[character_map[n]]
            elif include_time:
                nodes_size[graph.nodes().index(n)] *= self.__time_inlude_characters_influence_per_chapter[chap][character_map[n]]
            else:
                nodes_size[graph.nodes().index(n)] *= self.__characters_influence_per_chapter[chap][character_map[n]]

        edges = graph.edges()
        weights = [graph[u][v]['weight'] for u,v in edges]
        weights = [float(w)*max_edge_width/sum(weights) for w in weights]

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

        if chap == "whole":
            plt.savefig(os.path.join("..", "data", "graphs", "{}".format(dir), "{}".format("whole")))
        else:
            plt.savefig(os.path.join("..", "data", "graphs", "{}".format(dir), "{}".format(chap)))
        plt.clf()



    def prepare_data_for_graph(self, event_matrices):
        character_map = self.__book.get_characters_map()

        characters_influence_per_chapter = {}
        whole_characters_influence = {}
        time_inlude_characters_influence_per_chapter = {}

        hist_matrix = np.zeros((len(event_matrices[0]), len(event_matrices[0])))
        for chapter in range(len(event_matrices)):
            matrix = event_matrices[chapter]
            hist_matrix /= 2
            hist_matrix += matrix

            characters_influence = {}
            time_characters_influence = {}
            for character in character_map.values():
                characters_influence[character] = np.sum(matrix[character])
                time_characters_influence[character] = np.sum(hist_matrix[character])

            characters_influence_sum = sum(characters_influence.values())
            time_characters_influence_sum = sum(time_characters_influence.values())
            for character in character_map.values():
                characters_influence[character] /= characters_influence_sum
                time_characters_influence[character] /= time_characters_influence_sum

            characters_influence_per_chapter[chapter] = characters_influence
            time_inlude_characters_influence_per_chapter[chapter] = time_characters_influence

        for character in character_map.values():
                whole_characters_influence[character] = sum([np.sum(matrix[character]) for matrix in event_matrices])

        whole_characters_influence_sum = sum(whole_characters_influence.values())
        for character in character_map.values():
                whole_characters_influence[character] /= whole_characters_influence_sum

        self.__whole_characters_influence = whole_characters_influence
        self.__characters_influence_per_chapter  = characters_influence_per_chapter
        self.__time_inlude_characters_influence_per_chapter  = time_inlude_characters_influence_per_chapter




