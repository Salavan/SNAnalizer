# -*- coding: utf-8 -*-
import re
import codecs
import os.path
import matplotlib.pyplot as plt
import sys
from wordcloud import WordCloud
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
from nltk import wordpunct_tokenize

python_version = sys.version_info.major
wordNetLemmatizer = WordNetLemmatizer()

def load_stop_words(file=None):
    stoplist_set = set()
    default_file = os.path.join("..", "data", "stoplist.txt")
    if python_version == 3:
        with open(default_file if not file else file, "r", encoding="utf-8") as stoplist:
            for line in stoplist:
                word = line.strip()
                new_word = ""
                for c in word:
                    if not c.isalpha():
                        continue
                    new_word += c
                stoplist_set.add(new_word)
    else:
        with codecs.open(default_file if not file else file, "r", encoding="utf-8") as stoplist:
            for line in stoplist:
                word = line.strip()
                new_word = ""
                for c in word:
                    if not c.isalpha():
                        continue
                    new_word += c
                stoplist_set.add(new_word)
    return stoplist_set


def load_chapters(ch_range=None):
    chapters = []
    for i in range(1, 13) if not ch_range else ch_range:
        chapters += [load_chapter(i)]
    return chapters


def load_chapter(number):
    file = os.path.join("..", "data", "chapters", "{0}.txt".format(number))
    if python_version == 3:
        with open(file, "r", encoding="utf-8") as chapter:
            return chapter.readlines()
    else:
        with codecs.open(file, "r", encoding="utf-8") as chapter:
            return chapter.readlines()



def apply_stoplist(words_list):
    stoplist = load_stop_words()
    new_list = []
    for word in words_list:
        if not word.lower() in stoplist:
            new_list += [word]
    return new_list


def split_chapter(chapter):
    paragraphs = []
    paragraph = ""
    for line in chapter:
        if (python_version == 3 and line == "\n") or (python_version == 2 and line == "\r\n"):
            if paragraph == "":
                continue
            paragraphs += [paragraph]
            paragraph = ""
        else:
            paragraph += line.replace("\n", " ")
    return paragraphs


def split_paragraph_to_sentences(paragraph):
    return [s for s in re.split("\.|!|\?", paragraph)]


def split_to_words(text):
    words = []
    for word in text.split():
        new_word = ""
        for c in word:
            if not c.isalpha():
                continue
            new_word += c
        if new_word != "":
            words += [new_word]
    return words


def wordcloud_save(text, name_to_save="test.png"):
    wordcloud = WordCloud().generate(text)
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.savefig(name_to_save)


def wordcloud_show(text):
    wordcloud = WordCloud().generate(text)
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.show()


def split_and_apply_stoplist(book):
    for chapter in book:
        for chunks in book[chapter]:
            for i in range(len(book[chapter][chunks])):
                book[chapter][chunks][i] = apply_stoplist(split_to_words(book[chapter][chunks][i]))


def convert_to_lowercase(book):
    for chapter in book:
        for chunks in book[chapter]:
            for i in range(len(book[chapter][chunks])):
                for j in range(len(book[chapter][chunks][i])):
                    book[chapter][chunks][i][j] = book[chapter][chunks][i][j].lower()

def filter_string_with_nltk(text):
    result = []
    for word in wordpunct_tokenize(text):
        if word.isalpha() and word.lower() not in stopwords.words('english'):
            base_form = wordNetLemmatizer.lemmatize(word, 'v')
            result.append(base_form)

    return result