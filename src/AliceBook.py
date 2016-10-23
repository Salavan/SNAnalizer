# -*- coding: utf-8 -*-
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
        self.process_book_by_paragraphs_with_nltk()
        self.process_book_by_sentences_with_nltk()

        self.load_character_list()
        self.load_character_map()
        self.find_events_in_book_by_sentences(self.__processed_book_by_sentences)
        self.find_events_in_book_by_paragraphs(self.__processed_book_by_paragraphs)

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

    def show_wordcloud_from_sencences(self):
        sentences_texts_for_wordcloud = self.generate_text_for_wordcloud(self.__sentences_matrices)
        list_of_words_from_book_by_sentences = ""
        for text in sentences_texts_for_wordcloud:
            list_of_words_from_book_by_sentences += text
        wordcloud_show(list_of_words_from_book_by_sentences)
        # wordcloud_save(list_of_words_from_book_by_sentences, "../data/wordcloud/BookBySentences")

    def show_wordcloud_from_paragraphs(self):
        paragraphs_texts_for_wordcloud = self.generate_text_for_wordcloud(self.__paragraphs_matrices)
        list_of_words_from_book_by_paragraphs = ""
        for text in paragraphs_texts_for_wordcloud:
            list_of_words_from_book_by_paragraphs += text
        wordcloud_show(list_of_words_from_book_by_paragraphs)
        # wordcloud_save(list_of_words_from_book_by_paragraphs, "../data/wordcloud/BookByParagraphs")

    def show_wordcloud_from_sencences_from_chapter(self, i):
        sentences_texts_for_wordcloud = self.generate_text_for_wordcloud(self.__sentences_matrices)

        wordcloud_show(sentences_texts_for_wordcloud[i])
        # wordcloud_save(sentences_texts_for_wordcloud[i], "../data/wordcloud/" + str(i+1) + "_BySentences")

    def show_wordcloud_from_paragraphs_from_chapter(self, i):
        paragraphs_texts_for_wordcloud = self.generate_text_for_wordcloud(self.__paragraphs_matrices)
        wordcloud_show(paragraphs_texts_for_wordcloud[i])
        # wordcloud_save(paragraphs_texts_for_wordcloud[i], "../data/wordcloud/" + str(i+1) + "_ByParagraphs")


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

    def process_book_by_paragraphs_with_nltk(self):
        book_by_paragraphs = copy.deepcopy(self.__book_by_paragraphs)
        for chapter in book_by_paragraphs:
            for paragraph in range(len(book_by_paragraphs[chapter])):
                book_by_paragraphs[chapter][paragraph] = filter_string_with_nltk(book_by_paragraphs[chapter][paragraph])
        self.__processed_book_by_paragraphs = book_by_paragraphs

    def process_book_by_sentences_with_nltk(self):
        book_by_sentences = copy.deepcopy(self.__book_by_sentences)
        for chapter in book_by_sentences:
            for paragraph in book_by_sentences[chapter]:
                for sentence in range(len(book_by_sentences[chapter][paragraph])):
                    book_by_sentences[chapter][paragraph][sentence] \
                        = filter_string_with_nltk(book_by_sentences[chapter][paragraph][sentence])
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
                characters_list += [character]
        filter_alice_character_list(characters_list)
        self.__character_list = characters_list

    def get_charactes_with_ntlk(self):
        from nltk import pos_tag
        from nltk import ne_chunk

        person_list = []
        for chapter in self.__processed_book_by_sentences:
            for paragraph in self.__processed_book_by_sentences[chapter]:
                for words_list in self.__processed_book_by_sentences[chapter][paragraph]:
                    pos = pos_tag(words_list)
                    sentt = ne_chunk(pos, binary = False)
                    person = []
                    name = ""
                    for subtree in sentt.subtrees(filter=lambda t: t.label() == 'PERSON'):
                        for leaf in subtree.leaves():
                            person.append(leaf[0])
                        if len(person) > 1: #avoid grabbing lone surnames
                            for part in person:
                                name += part + ' '
                            if name[:-1] not in person_list:
                                person_list.append(name[:-1])
                            name = ''
                        person = []
        return person_list

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
    # print(characters_list)
    characters_list.remove("Come")
    characters_list.remove("Beautiful")
    characters_list.remove("Let")
    characters_list.remove("Mock")  # turtle
    characters_list.remove("Paris")
    characters_list.remove("Majesty")
    characters_list.remove("French")
    characters_list.remove("White")
    characters_list.remove("Duchess")
    characters_list.remove("Adventures")
    characters_list.remove("Silence")
    characters_list.remove("Longitude")
    characters_list.remove("Miss")
    characters_list.remove("Pray")
    characters_list.remove("English")
    characters_list.remove("March")  # hare
    characters_list.remove("Conqueror")  # William
    characters_list.remove("Said")
    characters_list.remove("Father")  # William
    characters_list.remove("Lobster")  # Quadrille
    characters_list.remove("Sure")
    characters_list.remove("Soup")
    characters_list.remove("Uglification")
    characters_list.remove("Two")  # rarely, conflicts
    characters_list.remove("Hearts")  # specifics exists
    characters_list.remove("Yet")
    characters_list.remove("One")
    characters_list.remove("Mystery")
    characters_list.remove("Soo")
    characters_list.remove("Latitude")
    characters_list.remove("Northumbria")  # place
    characters_list.remove("Mercia")  # place
    characters_list.remove("Mary")  # Ann
    characters_list.remove("Rome")
    characters_list.remove("Well")
    # print(characters_list)