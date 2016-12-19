# -*- coding: utf-8 -*-

import codecs
import sys
from pprint import pprint

from src.Utils import *
import numpy as np
import copy

python_version = sys.version_info.major


class Book:
    __book = None
    __chapters_path = None

    __chapters = None
    __processed_book_by_paragraphs = None
    __processed_book_by_sentences = None

    __character_list = None
    __characters_map = None
    __rev_characters_map = None
    __sentences_matrices = None
    __paragraphs_matrices = None

    def __init__(self, book_file = None):
        book = book_file.split("/")[-1].replace('.'+book_file.split(".")[-1],"")
        chapters_path = '{}/{}'.format('/'.join(book_file.split("/")[:-1]), book)

        loadBook = None

        try:
            loadBook = np.load(os.path.join("..", "data", "results", "{}.npz".format(book)))
            print("Previous book object found. Using it.")
        except:
            print("No previous file found. Generating book object...")

        if loadBook:
            self.__book = loadBook['book']
            self.__chapters_path = loadBook['chapters_path']
            self.__chapters = loadBook['chapters']
            self.__processed_book_by_paragraphs = loadBook['processed_book_by_paragraphs']
            self.__processed_book_by_sentences = loadBook['processed_book_by_sentences']
            self.__character_list = loadBook['character_list']
            self.__characters_map = loadBook['characters_map'][()]
            self.__rev_characters_map = loadBook['rev_characters_map'][()]
            self.__sentences_matrices = loadBook['sentences_matrices']
            self.__paragraphs_matrices = loadBook['paragraphs_matrices']
        else:
            self.__book = book
            self.__chapters_path = chapters_path
            self.__book_by_paragraphs = None
            self.__book_by_sentences = None

            if not os.path.exists(os.path.join("..", "data", "tmp")):
                os.makedirs(os.path.join("..", "data", "tmp"))


            try:
                self.__processed_book_by_paragraphs = np.load(os.path.join("..", "data", "tmp", "[{}] processed_by_paragraphs.npy".format(self.__book)))[()]
                print("Previous processed_by_paragraphs object found. Using it.")
            except:
                print("No previous processed_by_paragraphs object found. Generating...")
                self.__chapters = self.load_chapters(self.__chapters_path)
                self.__book_by_paragraphs = self.load_book_by_paragraphs()
                self.__processed_book_by_paragraphs = self.process_book_by_paragraphs_with_nltk()
                np.save(os.path.join("..", "data", "tmp", "[{}] processed_by_paragraphs.npy".format(self.__book)), self.__processed_book_by_paragraphs)

            try:
                self.__processed_book_by_sentences = np.load(os.path.join("..", "data", "tmp", "[{}] processed_book_by_sentences.npy".format(self.__book)))[()]
                print("Previous processed_book_by_sentences object found. Using it.")
            except:
                print("No previous processed_book_by_sentences object found. Generating...")
                if not not self.__book_by_paragraphs:
                    self.__chapters = self.load_chapters(self.__chapters_path)
                    self.__book_by_paragraphs = self.load_book_by_paragraphs()
                self.__book_by_sentences = self.load_book_by_sentences()
                self.__processed_book_by_sentences = self.process_book_by_sentences_with_nltk()
                np.save(os.path.join("..", "data", "tmp", "[{}] processed_book_by_sentences.npy".format(self.__book)), self.__processed_book_by_sentences)

            self.__character_list = self.load_character_list(self.__chapters_path)
            self.__characters_map, self.__rev_characters_map = self.load_character_map()

            self.__sentences_matrices = self.find_events_in_book_by_sentences(self.__processed_book_by_sentences)
            self.__paragraphs_matrices = self.find_events_in_book_by_paragraphs(self.__processed_book_by_paragraphs)

            self.save()

    def save(self):
        np.savez(os.path.join("..", "data", "results", "{}".format(self.__book)),
            book = self.__book,
            chapters_path = self.__chapters_path,
            chapters = self.__chapters,
            processed_book_by_paragraphs = self.__processed_book_by_paragraphs,
            processed_book_by_sentences = self.__processed_book_by_sentences,
            character_list = self.__character_list,
            characters_map = self.__characters_map,
            rev_characters_map = self.__rev_characters_map,
            sentences_matrices = self.__sentences_matrices,
            paragraphs_matrices = self.__paragraphs_matrices)


    def get_book_by_paragraphs(self):
        return self.__book_by_paragraphs

    def get_book_name(self):
        return self.__book

    def get_book_by_sentences(self):
        return self.__book_by_sentences

    def get_processed_book_by_paragraphs(self):
        return self.__processed_book_by_paragraphs

    def get_processed_book_by_sentences(self):
        return self.__processed_book_by_sentences

    def get_character_list(self):
        return self.__character_list

    def get_characters_map(self):
        return self.__characters_map

    def get_rev_characters_map(self):
        return self.__rev_characters_map

    def get_sentences_matrices(self):
        return self.__sentences_matrices

    def get_paragraphs_matrices(self):
        return self.__paragraphs_matrices

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

    def save_wordcloud_from_sencences_from_chapter(self, path):
        sentences_texts_for_wordcloud = self.generate_text_for_wordcloud(self.__sentences_matrices)

        if not os.path.exists(os.path.join(path, "wordclouds")):
            os.makedirs(os.path.join(path, "wordclouds"))

        for i in range(len(sentences_texts_for_wordcloud)):
            if sentences_texts_for_wordcloud[i] != "":
                wordcloud_save(sentences_texts_for_wordcloud[i], os.path.join(path, "wordclouds", "chapter {}".format(i+1)))

    def show_wordcloud_from_paragraphs_from_chapter(self, i):
        paragraphs_texts_for_wordcloud = self.generate_text_for_wordcloud(self.__paragraphs_matrices)
        wordcloud_show(paragraphs_texts_for_wordcloud[i])

    def save_wordcloud_from_paragraphs_from_chapter(self, path):
        paragraphs_texts_for_wordcloud = self.generate_text_for_wordcloud(self.__paragraphs_matrices)

        if not os.path.exists(os.path.join(path, "wordclouds")):
            os.makedirs(os.path.join(path, "wordclouds"))

        for i in range(len(paragraphs_texts_for_wordcloud)):
            if paragraphs_texts_for_wordcloud[i] != "":
                wordcloud_save(paragraphs_texts_for_wordcloud[i], os.path.join(path, "wordclouds", "chapter {}".format(i+1)))

    def load_whole_book(self, file):
        if python_version == 3:
            with open(file, "r", encoding="utf-8") as book:
                whole_book = book.readlines()
        else:
            with codecs.open(file, "r", encoding="utf-8") as book:
                whole_book = book.readlines()
        return whole_book

    def load_chapters(self, path):
        return load_chapters(path)

    def load_book_by_paragraphs(self):
        book_by_paragraphs = {}
        for chapter in range(len(self.__chapters)):
            book_by_paragraphs[chapter] = split_chapter(self.__chapters[chapter])
        return book_by_paragraphs

    def load_book_by_sentences(self):
        book_by_sentences = {}
        for chapter in range(len(self.__chapters)):
            book_by_sentences[chapter] = {}
            for paragraph in range(len(self.__book_by_paragraphs[chapter])):
                book_by_sentences[chapter][paragraph] \
                    = split_paragraph_to_sentences(self.__book_by_paragraphs[chapter][paragraph])
        return book_by_sentences

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
        return book_by_paragraphs

    def process_book_by_sentences_with_nltk(self):
        book_by_sentences = copy.deepcopy(self.__book_by_sentences)
        for chapter in book_by_sentences:
            for paragraph in book_by_sentences[chapter]:
                for sentence in range(len(book_by_sentences[chapter][paragraph])):
                    book_by_sentences[chapter][paragraph][sentence] \
                        = filter_string_with_nltk(book_by_sentences[chapter][paragraph][sentence])
        return book_by_sentences


    def load_character_list(self, path):
        with open('{}/characters.txt'.format(path), 'r') as characters_file:
            characters_list = [x.lower() for x in characters_file.read().split("\n")]
        return characters_list


    def load_character_map(self):
        characters_map = {}
        rev_characters_map = {}
        counter = 0
        for character in self.__character_list:
            characters_map[character] = counter
            rev_characters_map[counter] = character
            counter += 1
        return characters_map, rev_characters_map

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

        return adj_matrices

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

        return adj_matrices

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