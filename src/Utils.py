import re
from os import path
import matplotlib.pyplot as plt
from wordcloud import WordCloud

def load_stop_words(file = None):
    stoplist = set()
    with open("../data/stoplist.txt" if not file else file, "r", encoding="utf-8") as stoplisttxt:
        for line in stoplisttxt:
            word = line.strip()
            new_word = ""
            for c in word:
                if not c.isalpha():
                    continue
                new_word += c
            stoplist.add(new_word)

    return stoplist


def load_chapter(number, src = None):
    with open("../data/chapters/{0}.txt".format(number)
              if not src else "{0}/{1}.txt".format(src, number), "r", encoding="utf-8") as chapter:
        return chapter.readlines()


def load_chapters(crange = None):
    chapters = []
    for i in range(1,13) if not crange else crange:
        chapters += [load_chapter(i)]
    return chapters


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
        if line == "\n":
            if paragraph == "":
                continue
            paragraphs += [paragraph]
            paragraph = ""
        else:
            paragraph += line.replace("\n"," ")

    return paragraphs


def split_paragraph(paragraph):
    return [s for s in re.split("\.|\!|\?", paragraph)]


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

def create_wordcloud(text, name_to_save = "test.png"):
    wordcloud = WordCloud().generate(text)
    # Open a plot of the generated image.
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.savefig(name_to_save)
    # plt.show()
