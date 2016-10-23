# -*- coding: utf-8 -*-
from src.AliceBook import AliceBook
from src.SNA import SNA


if __name__ == "__main__":
    alice = AliceBook()
    sna = SNA(alice)

    # book_by_paragraphs = alice.get_book_by_paragraphs()
    # book_by_sentences = alice.get_book_by_sentences()
    # processed_book_by_paragraphs = alice.get_processed_book_by_paragraphs()
    # processed_book_by_sentences = alice.get_processed_book_by_sentences()
    # character_list = alice.get_character_list()
    #
    # alice.show_wordcloud_from_sencences()
    # alice.show_wordcloud_from_paragraphs()

    # for i in range(0, 12):
    #     alice.save_wordcloud_from_sencences_from_chapter(i)
    #     alice.save_wordcloud_from_paragraphs_from_chapter(i)

    # print(book_by_paragraphs[0][5])
    # print(processed_book_by_paragraphs[0][5])
    # print()
    #
    # print(book_by_sentences[0][5][0])
    # print(processed_book_by_sentences[0][5][0])
    # print()
    #
    # print(book_by_sentences[0][5][1])
    # print(processed_book_by_sentences[0][5][1])
    # print()
    #
    # print(book_by_sentences[0][5])
    # print(processed_book_by_sentences[0][5])
    # print()
    #
    #
    # print(character_list)
