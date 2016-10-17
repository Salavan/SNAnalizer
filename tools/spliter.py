chaper_counter = 0
with open("..\\data\\alice.txt", "r", encoding="utf-8") as alice:
    for line in alice:
        if line.startswith("CHAPTER"):
            chaper_counter += 1
            continue
        with open("..\data\chapters\{0}.txt".format(chaper_counter), "a+", encoding="utf-8") as out:
            out.write(line)
