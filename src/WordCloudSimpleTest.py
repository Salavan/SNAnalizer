from os import path
import matplotlib.pyplot as plt
from wordcloud import WordCloud

d = path.dirname(__file__)

file_to_use = 'stoplist'

# Read the whole text.
text = open(path.join(d, '../data/' + file_to_use + '.txt')).read()
wordcloud = WordCloud().generate(text)
# Open a plot of the generated image.
plt.imshow(wordcloud)
plt.axis("off")
plt.show()