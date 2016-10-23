# -*- coding: utf-8 -*-
# TODO: Ogarniecie zmiany Queen's => Queen itd.
# TODO: Przemyslec duze male litery u bohaterow, i ogarnac lepsze znajdowanie ich. np. jakiś tam Cat
# TODO: zastanowić się nad she itd.
import codecs
import sys

from src.Utils import *
import numpy as np
import copy

python_version = sys.version_info.major



class AliceBook:
    __whole_book = None
    __chapters = None
    __book_by_paragraphs = None
    __book_by_sentences = None
    __processed_book_by_paragraphs = None
    __processed_book_by_sentences = None
    __character_list = None
    __characters_map = None

    def __init__(self):
        self.load_whole_book()
        self.load_chapters()
        self.load_book_by_paragraphs()
        self.load_book_by_sentences()
        self.process_book_by_paragraphs()
        self.process_book_by_sentences()

        self.load_character_list()
        self.load_character_map()

        self.process_book_by_paragraphs_to_lower()
        self.process_book_by_sentences_to_lower()


        sentences_matrices = self.find_events_in_book(self.chapters_by_sentences)
        paragraphs_matrices = self.find_events_in_book(self.chapters_by_paragraphs)

        sentences_texts_for_wordcloud = self.generate_text_for_wordcloud(sentences_matrices)
        paragraphs_texts_for_wordcloud = self.generate_text_for_wordcloud(paragraphs_matrices)

        megaA = ""
        megaB = ""
        for text in sentences_texts_for_wordcloud:
            megaA += text
        for text in paragraphs_texts_for_wordcloud:
            megaB += text

        wordcloud_save(megaA, "../data/wordcloud/BookBySentences")
        wordcloud_save(megaB, "../data/wordcloud/BookByParagraphs")

        for i in range(0, 12):
            wordcloud_save(sentences_texts_for_wordcloud[i], "../data/wordcloud/" + str(i+1) + "_BySentences")
            wordcloud_save(paragraphs_texts_for_wordcloud[i], "../data/wordcloud/" + str(i+1) + "_ByParagraphs")

    def get_book_by_paragraphs(self):
        return self.__book_by_paragraphs

    def get_book_by_sentences(self):
        return self.__book_by_sentences

    def get_processed_book_by_paragraphs(self):
        return self.__processed_book_by_paragraphs

    def get_processed_book_by_sentences(self):
        return self.__processed_book_by_sentences

    def get_character_list(self):
        return self.__character_list



    def find_events_in_chapter(self, chapter):
        adj_matrix = np.zeros((len(self.characters), len(self.characters)))
        for chunks in chapter:
            for chunk in chapter[chunks]:
                characters_in_event = set()
                for word in chunk:
                    if word in self.characters_map:
                        characters_in_event.add(word)

                if len(characters_in_event) > 1:
                    for name in characters_in_event:
                        for name2 in characters_in_event:
                            if name != name2:
                                # adj_matrix[self.characters_map[name]][self.characters_map[name2]] = 1
                                adj_matrix[self.characters_map[name]][self.characters_map[name2]] += 1

        return adj_matrix

    def find_events_in_book(self, book):
        adj_matrices = []
        for chapter in book:
            adj_matrices += [self.find_events_in_chapter(book[chapter])]

        return adj_matrices

    def generate_text_for_wordcloud(self, data):
        result = []
        for chapter in data:
            string = ""
            for name in self.characters:
                for _ in range(int(np.sum(chapter[self.characters_map[name]]))):
                    string += name + " "
            result += [string]

        return result

    def load_whole_book(self):
        file = os.path.join("..", "data", "alice.txt")

        if python_version == 3:
            with open(file, "r", encoding="utf-8") as book:
                whole_book = book.readlines()
        else:
            with codecs.open(file, "r", encoding="utf-8") as book:
                whole_book = book.readlines()
        self.__whole_book = whole_book

    def load_chapters(self):
        chapters = load_chapters()
        self.__chapters = chapters

    def load_book_by_paragraphs(self):
        book_by_paragraphs = {}
        for chapter in range(len(self.__chapters)):
            book_by_paragraphs[chapter] = split_chapter(self.__chapters[chapter])
        self.__book_by_paragraphs = book_by_paragraphs

    def load_book_by_sentences(self):
        book_by_sentences = {}
        for chapter in range(len(self.__chapters)):
            book_by_sentences[chapter] = {}
            for paragraph in range(len(self.__book_by_paragraphs[chapter])):
                book_by_sentences[chapter][paragraph] \
                    = split_paragraph_to_sentences(self.__book_by_paragraphs[chapter][paragraph])
        self.__book_by_sentences = book_by_sentences

    def process_book_by_paragraphs(self):
        book_by_paragraphs = copy.deepcopy(self.__book_by_paragraphs)
        for chapter in book_by_paragraphs:
            for paragraph in range(len(book_by_paragraphs[chapter])):
                book_by_paragraphs[chapter][paragraph] \
                    = apply_stoplist(split_to_words(book_by_paragraphs[chapter][paragraph]))
        self.__processed_book_by_paragraphs = book_by_paragraphs

    def process_book_by_sentences(self):
        book_by_sentences = copy.deepcopy(self.__book_by_sentences)
        for chapter in book_by_sentences:
            for paragraph in book_by_sentences[chapter]:
                for sentence in range(len(book_by_sentences[chapter][paragraph])):
                    book_by_sentences[chapter][paragraph][sentence] \
                        = apply_stoplist(split_to_words(book_by_sentences[chapter][paragraph][sentence]))
        self.__processed_book_by_sentences = book_by_sentences

    def load_character_list(self):
        characters_map = {}
        for chapter in self.__processed_book_by_sentences:
            for paragraph in self.__processed_book_by_sentences[chapter]:
                for words_list in self.__processed_book_by_sentences[chapter][paragraph]:
                    for word in words_list[1:]:
                        if len(word) > 2 and word[0].isupper() and not word[1].isupper():
                            if not word in characters_map:
                                characters_map[word] = 1
                            characters_map[word] += 1
        characters_list = []
        for character in characters_map:
            if characters_map[character] > 2:
                characters_list += [character.lower()]

        filter_alice_character_list(characters_list)
        self.__character_list = characters_list

    def load_character_map(self):
        characters_map = {}
        counter = 0
        for character in self.__character_list:
            characters_map[character] = counter
            counter += 1
        self.__characters_map = characters_map

    def process_book_by_paragraphs_to_lower(self):
        for chapter in self.__processed_book_by_paragraphs:
            for paragraph in range(len(self.__processed_book_by_paragraphs[chapter])):
                for word in range(len(self.__processed_book_by_paragraphs[chapter][paragraph])):
                    self.__processed_book_by_paragraphs[chapter][paragraph][word] \
                        = self.__processed_book_by_paragraphs[chapter][paragraph][word].lower()

    def process_book_by_sentences_to_lower(self):
        for chapter in self.__processed_book_by_sentences:
            for paragraph in range(len(self.__processed_book_by_sentences[chapter])):
                for sentence in range(len(self.__processed_book_by_sentences[chapter][paragraph])):
                    for word in range(len(self.__processed_book_by_sentences[chapter][paragraph][sentence])):
                        self.__processed_book_by_sentences[chapter][paragraph][sentence][word] \
                            = self.__processed_book_by_sentences[chapter][paragraph][sentence][word].lower()

    # def load_simplify_book_by_paragraphs(self):
    #     # book = copy.deepcopy(self.__processed_book_by_paragraphs)
    #     # print(book)
    #     # book = {0, [ [["111", "222"], ["333", "444"]] ]}
    #     book = {0: [['alice', 'beginning'], ['considering', 'mind', 'hot'], [], [], []]}
    #     chapter__ = [['alice', 'beginning'], ['considering', 'mind', 'hot'], [], [], []]
    #     paragraph__ = ['alice', 'beginning']
    #
    #     nbook = {}
    #     for c in range(len(book)):
    #         for p in range(len(book[c])):
    #             if book[c][p]:
    #                 nbook[c] = book[c][p]
    #     print(book)
    #     print("****")
    #
    #     # for chapter in book.keys():
    #     #     for paragraph in range(len(book[chapter])):
    #     #         book[chapter][paragraph] = list(filter(None, book[chapter][paragraph]))
    #     #     if not book[chapter]:
    #     #         del book[chapter]
    #     return book

    #
    # def remove_empty_keys(d):
    #     for k in d.keys():
    #         if not d[k]:
    #             del d[k]
    #
    # def not_empty_paragraphs_len(self, book, chapter):
    #     lenth = 0
    #     for paragraph in range(len(book[chapter])):
    #         if book[chapter][paragraph]:
    #             lenth += 1
    #     return lenth
    #
    # def not_empty_sentences_len(self, book, chapter, paragraph):
    #     lenth = 0
    #     for sentence in range(len(book[chapter][paragraph])):
    #         if book[chapter][paragraph][sentence]:
    #             lenth += 1
    #     return lenth
    #
    # def load_simplify_book_by_paragraphs2(self):
    #     simplified_book = {}
    #     for chapter in range(len(self.__processed_book_by_paragraphs)):
    #         simplified_book[chapter] = {}
    #         for paragraph in range(len(self.__processed_book_by_paragraphs[chapter])):
    #             simplified_book[chapter][paragraph] = []
    #             for word in range(len(self.__processed_book_by_paragraphs[chapter][paragraph])):
    #                 if self.__processed_book_by_paragraphs[chapter][paragraph][word]:
    #                     simplified_book[chapter][paragraph]\
    #                         .append(self.__processed_book_by_paragraphs[chapter][paragraph][word])
    #     return simplified_book


def filter_alice_character_list(characters_list):
    print(characters_list)
    characters_list.remove("let")
    characters_list.remove("time")
    characters_list.remove("come")
    characters_list.remove("english")
    characters_list.remove("soooop")
    characters_list.remove("white")
    characters_list.remove("cat")
    characters_list.remove("turtle")
    characters_list.remove("hare")
    characters_list.append("sister")
