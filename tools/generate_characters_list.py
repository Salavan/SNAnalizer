import codecs
import os
import sys
from src.Utils import filter_string_with_nltk, split_paragraph_to_sentences, split_chapter, load_chapters
import enchant
from nltk import wordpunct_tokenize

d = enchant.Dict("en_US")

if len(sys.argv) != 3:
    print("usage: python spliter.py file_to_split_path min_occurs")
    exit(-1)

book_file = sys.argv[1]
min_occurs = int(sys.argv[2])
book = sys.argv[1].split("/")[-1].replace('.'+sys.argv[1].split(".")[-1],"")
chapers_path = '{}/{}'.format('/'.join(sys.argv[1].split("/")[:-1]), book)

if not os.path.exists(chapers_path):
    print("Error chapter directory not found.")
    exit(-1)

__processed_book_by_sentences = None
__chapters = None
__book_by_paragraphs = None

chapters = load_chapters(chapers_path)
__chapters = chapters

book_by_paragraphs = {}
for chapter in range(len(__chapters)):
    book_by_paragraphs[chapter] = split_chapter(__chapters[chapter])
__book_by_paragraphs = book_by_paragraphs

book_by_sentences = {}
for chapter in range(len(__chapters)):
    book_by_sentences[chapter] = {}
    for paragraph in range(len(__book_by_paragraphs[chapter])):
        book_by_sentences[chapter][paragraph] \
            = split_paragraph_to_sentences(__book_by_paragraphs[chapter][paragraph])
__book_by_sentences = book_by_sentences

book_by_sentences = __book_by_sentences
for chapter in book_by_sentences:
    for paragraph in book_by_sentences[chapter]:
        for sentence in range(len(book_by_sentences[chapter][paragraph])):
            book_by_sentences[chapter][paragraph][sentence] \
                = filter_string_with_nltk(book_by_sentences[chapter][paragraph][sentence], False)
__processed_book_by_sentences = book_by_sentences

characters_map = {}
for chapter in __processed_book_by_sentences:
    for paragraph in __processed_book_by_sentences[chapter]:
        for words_list in __processed_book_by_sentences[chapter][paragraph]:
            for i in range(len(words_list[1:])):
                word = words_list[i+1]
                prev_word = words_list[i]
                if len(word) > 2 and word[0].isupper() and not word[1].isupper():
                    if not word in characters_map:
                        characters_map[word] = 1
                    characters_map[word] += 1
characters_list = []

for character in characters_map:
    if characters_map[character] > min_occurs:
        characters_list += [character]
__character_list = characters_list

with codecs.open("{}/characters.txt".format(chapers_path), "w+", encoding="utf-8") as out:
    for c in __character_list:
        out.write("{}\n".format(c))
