import os
import sys

if len(sys.argv) != 2:
    print("usage: python spliter.py file_to_split_path")
    exit(-1)

book_file = sys.argv[1]
book = sys.argv[1].split("/")[-1].replace('.'+sys.argv[1].split(".")[-1],"")
chapers_path = '{}/{}'.format('/'.join(sys.argv[1].split("/")[:-1]), book)
if not os.path.exists(chapers_path):
    os.makedirs(chapers_path)

chaper_counter = 0
with open(book_file, "r", encoding="utf-8") as book:
    for line in book:
        if line.lower().startswith("chapter"):
            chaper_counter += 1
            continue
        with open("{}/{}.txt".format(chapers_path, chaper_counter), "a+", encoding="utf-8") as out:
            out.write(line)
