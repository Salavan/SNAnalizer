from src.Utils import *
from pprint import pprint


class Alice_book():
    chapter_to_paragraph = None
    chapter_to_paragraph_to_sentences = None

    chapters_by_paragraphs = None #{[]}
    chapters_by_sentences = None #{{[]}}

    def __init__(self):
        chapters = load_chapters()



        self.chapter_to_paragraph = {}
        self.chapter_to_paragraph_to_sentences = {}

        for c in range(0,12):
            self.chapter_to_paragraph[c] = {}
            self.chapter_to_paragraph[c][0] = split_chapter(chapters[c])

        for c in range(0,12):
            for p in range(len(self.chapter_to_paragraph[c])):
                if not c in self.chapter_to_paragraph_to_sentences:
                    self.chapter_to_paragraph_to_sentences[c] = {}
                self.chapter_to_paragraph_to_sentences[c][p] = split_paragraph(self.chapter_to_paragraph[c][p])

        self.chapter_to_paragraph_to_sentences_to_words = []

        for c in range(0,12):
            for p in range(len(self.chapter_to_paragraph[c])):
                if not c in self.chapter_to_paragraph_to_sentences_to_words:
                    self.chapter_to_paragraph_to_sentences_to_words[c] = {}
                if not p in self.chapter_to_paragraph_to_sentences_to_words[c]:
                    self.chapter_to_paragraph_to_sentences_to_words[c][p] = {}

                self.chapter_to_paragraph_to_sentences_to_words[c][p]

        print(self.chapter_to_paragraph[0][6])
        print(split_to_words(self.chapter_to_paragraph[0][6]))

        # pprint(self.chapter_to_paragraph_to_sentences)

alice = Alice_book()