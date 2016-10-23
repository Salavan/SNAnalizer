# -*- coding: utf-8 -*-
# TODO: Ogarniecie zmiany Queen's => Queen itd.
# TODO: Przemyslec duze male litery u bohaterow, i ogarnac lepsze znajdowanie ich. np. jakiś tam Cat
# TODO: zastanowić się nad she itd.
import codecs
import sys
from pprint import pprint

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
    __sentences_matrices = None
    __paragraphs_matrices = None

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

        self.find_events_in_book_by_sentences(self.__processed_book_by_sentences)
        self.find_events_in_book_by_paragraphs(self.__processed_book_by_paragraphs)

        sentences_texts_for_wordcloud = self.generate_text_for_wordcloud(self.__sentences_matrices)
        paragraphs_texts_for_wordcloud = self.generate_text_for_wordcloud(self.__paragraphs_matrices)

        list_of_words_from_book_by_sentences = ""
        list_of_words_from_book_by_paragraphs = ""
        for text in sentences_texts_for_wordcloud:
            list_of_words_from_book_by_sentences += text
        for text in paragraphs_texts_for_wordcloud:
            list_of_words_from_book_by_paragraphs += text

        # wordcloud_save(list_of_words_from_book_by_sentences, "../data/wordcloud/BookBySentences")
        wordcloud_show(list_of_words_from_book_by_sentences)
        # wordcloud_save(list_of_words_from_book_by_paragraphs, "../data/wordcloud/BookByParagraphs")
        wordcloud_show(list_of_words_from_book_by_paragraphs)

        for i in range(0, 2):
            # wordcloud_save(sentences_texts_for_wordcloud[i], "../data/wordcloud/" + str(i+1) + "_BySentences")
            wordcloud_show(sentences_texts_for_wordcloud[i])
            wordcloud_show(paragraphs_texts_for_wordcloud[i])
            # wordcloud_save(paragraphs_texts_for_wordcloud[i], "../data/wordcloud/" + str(i+1) + "_ByParagraphs")

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

    def find_events_in_book_by_sentences(self, book):
        adj_matrices = []
        for chapter in book:
            adj_matrices += [self.find_events_in_chapter_by_sentences(book[chapter])]

        self.__sentences_matrices = adj_matrices

    def find_events_in_chapter_by_sentences(self, chapter):
        adj_matrix = np.zeros((len(self.__character_list), len(self.__character_list)))
        for paragraph in chapter:
            for sentence in chapter[paragraph]:
                characters_in_event = set()
                for word in sentence:
                    if word in self.__characters_map:
                        characters_in_event.add(word)

                if len(characters_in_event) > 1:
                    for name in characters_in_event:
                        for name2 in characters_in_event:
                            if name != name2:
                                # adj_matrix[self.characters_map[name]][self.characters_map[name2]] = 1
                                adj_matrix[self.__characters_map[name]][self.__characters_map[name2]] += 1

        return adj_matrix

    def find_events_in_book_by_paragraphs(self, book):
        adj_matrices = []
        for chapter in book:
            adj_matrices += [self.find_events_in_chapter_by_paragraphs(book[chapter])]

        self.__paragraphs_matrices = adj_matrices

    def find_events_in_chapter_by_paragraphs(self, chapter):
        adj_matrix = np.zeros((len(self.__character_list), len(self.__character_list)))
        for paragraph in chapter:
            characters_in_event = set()
            for word in paragraph:
                if word in self.__characters_map:
                    characters_in_event.add(word)

            if len(characters_in_event) > 1:
                for name in characters_in_event:
                    for name2 in characters_in_event:
                        if name != name2:
                            # adj_matrix[self.characters_map[name]][self.characters_map[name2]] = 1
                            adj_matrix[self.__characters_map[name]][self.__characters_map[name2]] += 1

        return adj_matrix

    def generate_text_for_wordcloud(self, data):
        result = []
        for chapter in data:
            string = ""
            for character in self.__character_list:
                for _ in range(int(np.sum(chapter[self.__characters_map[character]]))):
                    string += character + " "
            result += [string]

        return result


def filter_alice_character_list(characters_list):
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
