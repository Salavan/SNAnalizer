# -*- coding: utf-8 -*-
import copy
import operator
import os

import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

max_edge_width = 5
max_node_size = 10000

def load_or_save(f):
    print(f.__name__)

class SNA:
    __book = None
    __book_name = None
    __result_dir = None

    __chapters_graphs = []
    __time_chapters_graphs = []

    __whole_characters_influence = None
    __characters_influence_per_chapter  = None
    __time_inlude_characters_influence_per_chapter  = None

    def __init__(self, book, case = None):
        self.__book = book
        self.__book_name = self.__book.get_book_name()
        self.__result_dir = os.path.join("..", "data", "results", "{}".format(self.__book_name))

        if not os.path.exists(self.__result_dir):
            os.makedirs(self.__result_dir)

        if not os.path.exists(os.path.join(self.__result_dir, "Paragraphs case")):
            os.makedirs(os.path.join(self.__result_dir, "Paragraphs case"))

        if not os.path.exists(os.path.join(self.__result_dir, "Sentences case")):
            os.makedirs(os.path.join(self.__result_dir, "Sentences case"))

        if case == "paragraphs": #paragraphs
            self.__book.save_wordcloud_from_paragraphs_from_chapter(os.path.join(self.__result_dir, "Paragraphs case"))
            plt.clf()
            self.__whole_characters_influence, self.__characters_influence_per_chapter, \
                self.__time_inlude_characters_influence_per_chapter = \
                    self.prepare_data_for_graph(self.__book.get_paragraphs_matrices())

            self.build_graph_from_paragraphs()

            pos = self.get_nodes_pos(nx.compose_all(self.__chapters_graphs))
            time_pos = self.get_nodes_pos(nx.compose_all(self.__time_chapters_graphs))

            self.plot_centralities("Paragraphs case")
            self.plot_similarities("Paragraphs case")

            for i in range(len(self.__chapters_graphs)):
                self.draw_chapter_graph(i, "Paragraphs case/characters interaction/", pos)
            for i in range(len(self.__time_chapters_graphs)):
                self.draw_chapter_graph(i, "Paragraphs case/characters interaction with previous chapter consideration/", time_pos, True)
            self.draw_chapter_graph("whole", "Paragraphs case/", pos)
            self.save("Paragraphs case")

        elif case == "sentences": #sentences
            self.__book.save_wordcloud_from_sencences_from_chapter(os.path.join(self.__result_dir, "Sentences case"))
            plt.clf()
            self.__whole_characters_influence, self.__characters_influence_per_chapter, \
                self.__time_inlude_characters_influence_per_chapter = \
                    self.prepare_data_for_graph(self.__book.get_sentences_matrices())

            self.build_graph_from_sentences()

            pos = self.get_nodes_pos(nx.compose_all(self.__chapters_graphs))
            time_pos = self.get_nodes_pos(nx.compose_all(self.__time_chapters_graphs))

            self.plot_centralities("Sentences case")
            self.plot_similarities("Sentences case")

            for i in range(len(self.__chapters_graphs)):
                self.draw_chapter_graph(i, "Sentences case/characters interaction/", pos)
            for i in range(len(self.__time_chapters_graphs)):
                self.draw_chapter_graph(i, "Sentences case/characters interaction with previous chapter consideration/", time_pos, True)

            self.draw_chapter_graph("whole", "Sentences case/", pos)
            self.save("Sentences case")
        else:
            print("Wrong case, allowed 'sentences' or 'paragraphs'")

    def save(self, path):
        np.savez(os.path.join(self.__result_dir, path, "data"),
            __book = self.__book,
            __book_name = self.__book_name,
            __result_dir = self.__result_dir,
            __chapters_graphs = self.__chapters_graphs,
            __time_chapters_graphs = self.__time_chapters_graphs,
            __whole_characters_influence = self.__whole_characters_influence,
            __characters_influence_per_chapter = self.__characters_influence_per_chapter,
            __time_inlude_characters_influence_per_chapter = self.__time_inlude_characters_influence_per_chapter)



    def plot_similarities(self, path):
        similarities = []
        for i in range(len(self.__chapters_graphs)-1):
            similarities += [self.similarity(self.__chapters_graphs[i], self.__chapters_graphs[i+1])]

        legend_handlers = []
        tmp, = plt.plot(np.arange(len(similarities))+1, similarities, label="similarity of chapter with previous one")
        legend_handlers.append(tmp)
        plt.xlabel("chapter")
        plt.ylabel("similarity")
        plt.legend(handles=legend_handlers)
        plt.savefig(os.path.join(self.__result_dir, path, 'similarity of chapters with previous ones'))
        plt.clf()

    def similarity(self, g1, g2):
        try:
            def select_k(spectrum, minimum_energy = 0.9):
                running_total = 0.0
                total = sum(spectrum)
                if total == 0.0:
                    return len(spectrum)
                for i in range(len(spectrum)):
                    running_total += spectrum[i]
                    if running_total / total >= minimum_energy:
                        return i + 1
                return len(spectrum)

            laplacian1 = nx.spectrum.laplacian_spectrum(g1)
            laplacian2 = nx.spectrum.laplacian_spectrum(g2)
            # print(laplacian1)
            # print(laplacian2)

            k1 = select_k(laplacian1)
            k2 = select_k(laplacian2)
            # print(k1)
            # print(k2)
            k = min(k1, k2)

            return sum((laplacian1[:k] - laplacian2[:k])**2)
        except:
            return 0

    def plot_centralities(self, path):
            def sort_dict(A):
                return [sorted(A[i].iteritems(),
                key=operator.itemgetter(1), reverse=True) for i in range(len(A))]

            whole = nx.compose_all(self.__chapters_graphs)
            number_of_chapters = len(self.__chapters_graphs)
            vitalities = [nx.closeness_vitality(self.__chapters_graphs[i]) for i in range(len(self.__chapters_graphs))]
            degree_centralities = [nx.degree_centrality(self.__chapters_graphs[i]) for i in range(len(self.__chapters_graphs))]
            closeness_centralities = [nx.closeness_centrality(self.__chapters_graphs[i]) for i in range(len(self.__chapters_graphs))]
            # eigenvector_centralities = [nx.eigenvector_centrality_numpy(self.__chapters_graphs[i]) for i in range(len(self.__chapters_graphs))]


            whole_vitalities = nx.closeness_vitality(whole)
            whole_degree_centralities = nx.degree_centrality(whole)
            whole_closeness_centralities = nx.closeness_centrality(whole)
            # whole_eigenvector_centralities = nx.eigenvector_centrality_numpy(whole)

            # vitalities = sort_dict(vitalities)
            # degree_centralities = sort_dict(degree_centralities)
            # closeness_centralities = sort_dict(closeness_centralities)
            # eigenvector_centralities = sort_dict(eigenvector_centralities)

            whole_vitalities = sorted(whole_vitalities.iteritems(), key=operator.itemgetter(1), reverse=True)
            whole_degree_centralities = sorted(whole_degree_centralities.iteritems(), key=operator.itemgetter(1), reverse=True)
            whole_closeness_centralities = sorted(whole_closeness_centralities.iteritems(), key=operator.itemgetter(1), reverse=True)
            # whole_whole_eigenvector_centralities = sorted(whole_eigenvector_centralities.iteritems(), key=operator.itemgetter(1), reverse=True)

            bests = [x[0] for x in whole_degree_centralities[:5]]

            vitality_values = [[vitality[best] if best in vitality else 0 for vitality in vitalities] for best in bests]
            degree_centralities_values = [[centrality[best] if best in centrality else 0 for centrality in degree_centralities] for best in bests]
            closeness_centralities_values = [[centrality[best] if best in centrality else 0 for centrality in closeness_centralities] for best in bests]
            # eigenvector_centralities_values = [[centrality[best] if best in centrality else 0 for centrality in eigenvector_centralities] for best in bests]

            ylabels = ["vitality", "degree centrality", "closeness centrality"]
            whole_values = [vitality_values, degree_centralities_values, closeness_centralities_values]
            for values, ylabel in zip(whole_values, ylabels):
                legend_handlers = []
                for i in range(len(bests)):
                    tmp, = plt.plot(range(number_of_chapters), values[i], label=bests[i])
                    legend_handlers.append(tmp)
                # plt.xlim([plt.xlim()[0]*1.2, plt.xlim()[1]*1.2])
                plt.ylim([plt.ylim()[0]*1.2, plt.ylim()[1]*1.2])
                plt.xlabel("chapter")
                plt.ylabel(ylabel)
                plt.legend(handles=legend_handlers)
                plt.savefig(os.path.join(self.__result_dir, path, 'change of {} in chapters'.format(ylabel)))
                plt.clf()

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
                self.__time_chapters_graphs.append(self.combined_time_graphs(prev_graph, tmp_graph, 0.9, 1))
                # self.__time_chapters_graphs.append(self.combined_time_graphs(prev_graph, tmp_graph))
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

        if not os.path.exists(os.path.join(self.__result_dir, dir)):
            os.makedirs(os.path.join(self.__result_dir, dir))

        if chap == "whole":
            plt.savefig(os.path.join(self.__result_dir, dir, "whole"))
        else:
            plt.savefig(os.path.join(self.__result_dir, dir, "chapter {}".format(chap+1)))
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
                characters_influence[character] = characters_influence[character] / characters_influence_sum \
                    if characters_influence_sum != 0 else 0
                time_characters_influence[character] = time_characters_influence[character] / time_characters_influence_sum \
                    if time_characters_influence_sum != 0 else 0

            characters_influence_per_chapter[chapter] = characters_influence
            time_inlude_characters_influence_per_chapter[chapter] = time_characters_influence

        for character in character_map.values():
                whole_characters_influence[character] = sum([np.sum(matrix[character]) for matrix in event_matrices])

        whole_characters_influence_sum = sum(whole_characters_influence.values())
        for character in character_map.values():
                whole_characters_influence[character] /= whole_characters_influence_sum

        return whole_characters_influence, characters_influence_per_chapter, time_inlude_characters_influence_per_chapter