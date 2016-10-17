# TODO: Ogarniecie zmiany Queen's => Queen itd.
# TODO: Przemyslec duze male litery u bohaterow, i ogarnac lepsze znajdowanie ich. np. jakiś tam Cat
# TODO: zastanowić się nad she itd.

from src.Utils import *
import numpy as np
# from nltk.stem.wordnet import WordNetLemmatizer


class AliceBook():
    chapters = None
    chapters_by_paragraphs = None #slownik: rozdzial -> 0 -> list  paragrafow
    chapters_by_sentences = None #slownik: rozdzial -> parafraf -> lista slow

    characters = None
    characters_map = None

    def __init__(self):
        self.chapters = load_chapters()
        self.split_chapters()
        self.split_paragraphs()

        self.preproces_book(self.chapters_by_paragraphs)
        self.preproces_book(self.chapters_by_sentences)

        self.characters = self.find_characters()
        self.characters_map = self.get_characters_map()

        self.data_to_lower(self.chapters_by_paragraphs)
        self.data_to_lower(self.chapters_by_sentences)

        A = self.find_events_in_book(self.chapters_by_sentences)
        B = self.find_events_in_book(self.chapters_by_paragraphs)

        Astr = self.generate_text_for_wordcloud(A)
        Bstr = self.generate_text_for_wordcloud(B)

        megaA = ""
        megaB = ""
        for text in Astr:
            megaA += text
        for text in Bstr:
            megaB += text

        create_wordcloud(megaA)
        # create_wordcloud(megaB)



        print(A)
        print(B)

    def get_characters_map(self):
        characters_map = {}

        counter = 0
        for character in self.characters:
            characters_map[character] = counter
            counter += 1

        return characters_map

    def data_to_lower(self, data):
        for chapter in data:
            for chunks in data[chapter]:
                for i in range(len(data[chapter][chunks])):
                    for j in range(len(data[chapter][chunks][i])):
                        data[chapter][chunks][i][j] = data[chapter][chunks][i][j].lower()

    def split_chapters(self):
        self.chapters_by_paragraphs = {}
        self.chapters_by_sentences = {}

        for c in range(0,12):
            self.chapters_by_paragraphs[c] = {}
            self.chapters_by_paragraphs[c][0] = split_chapter(self.chapters[c])

    def split_paragraphs(self):
        for c in range(0,12):
            self.chapters_by_sentences[c] = {}
            for p in range(len(self.chapters_by_paragraphs[c][0])):
                self.chapters_by_sentences[c][p] = split_paragraph(self.chapters_by_paragraphs[c][0][p])

    def preproces_book(self, data):
        for chapter in data:
            for chunks in data[chapter]:
                for i in range(len(data[chapter][chunks])):
                    data[chapter][chunks][i] = apply_stoplist(split_to_words(data[chapter][chunks][i]))

    def find_characters(self):
        names = {}
        for chapter in self.chapters_by_sentences:
            for pharagraph in self.chapters_by_sentences[chapter]:
                for words_list in self.chapters_by_sentences[chapter][pharagraph]:
                    for word in words_list[1:]:
                        if len(word) > 2 and word[0].isupper() and not word[1].isupper():
                            if not word in names:
                                names[word] = 0
                            names[word] += 1
        result = []
        for name in names:
            if names[name] > 2:
                result += [name.lower()]

        self.preproces_characters(result)

        return result

    def preproces_characters(self, characters_list):
        characters_list.remove("let")
        characters_list.remove("said")
        characters_list.remove("time")
        characters_list.remove("come")
        characters_list.remove("english")
        characters_list.remove("soooop")
        characters_list.remove("white")
        characters_list.remove("cat")
        characters_list.append("sister")

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

AliceBook()
