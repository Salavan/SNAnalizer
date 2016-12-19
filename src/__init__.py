# -*- coding: utf-8 -*-

if __name__ == "__main__":
    from src.SNA import SNA
    from src.Book import Book

    oliver = Book("C:/studia/ed/SNAnalizer/data/Books/Charles Dickens - Oliver Twist.txt")
    oliver_sna = SNA(oliver, "paragraphs")
    # oliver = Book("C:/studia/ed/SNAnalizer/data/Books/Charles Dickens - Oliver Twist.txt")
    # oliver_sna = SNA(oliver, "sentences")

    # alice = Book("C:/studia/ed/SNAnalizer/data/Books/Lewis Carroll - Alice's Adventures in Wonderland.txt")
    # alice_sna = SNA(alice, "paragraphs")
    # alice = Book("C:/studia/ed/SNAnalizer/data/Books/Lewis Carroll - Alice's Adventures in Wonderland.txt")
    # alice_sna = SNA(alice, "sentences")

    # harry = Book("C:/studia/ed/SNAnalizer/data/Books/J.K. Rowling - Harry Potter and the Sorcerer's Stone.txt")
    # harry_sna = SNA(harry, "paragraphs")
    # harry = Book("C:/studia/ed/SNAnalizer/data/Books/J.K. Rowling - Harry Potter and the Sorcerer's Stone.txt")
    # harry_sna = SNA(harry, "sentences")











    # book_by_paragraphs = alice.get_book_by_paragraphs()
    # book_by_sentences = alice.get_book_by_sentences()
    # processed_book_by_paragraphs = alice.get_processed_book_by_paragraphs()
    # processed_book_by_sentences = alice.get_processed_book_by_sentences()
    # character_list = alice.get_character_list()
    #
    # alice.show_wordcloud_from_sencences()
    # alice.show_wordcloud_from_paragraphs()
    # for i in range(0, 12):
    #     alice.show_wordcloud_from_sencences_from_chapter(i)
    #     alice.show_wordcloud_from_paragraphs_from_chapter(i)



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
