import nltk
from bs4 import BeautifulSoup
import re
import matplotlib.pyplot as plt
from collections import Counter
import numpy as np
from bidi import algorithm as bidialg
import arabic_reshaper


def is_float(string):
  try:
    return float(string) and '.' in string  # True if string is a number contains a dot
  except ValueError:  # String is not a number
    return False

with open('persian.txt', 'r', encoding="utf8") as myfile:
    sw = myfile.read().replace('\n', ' ').replace("\u200c","").replace("\ufeff","").replace("."," ").split(' ')# a list of stop words


with open('attar.txt', 'r', encoding="utf8") as myfile:
    line = myfile.read().replace('\n', ' ').replace(",","").replace(":","").replace("ۀ","ه").replace("-","").replace("،","")
    masnavi = re.split('[\t\s:]+', line)   # a list of stop words

masnavi_nn = [x for x in masnavi if (not is_float(x) or not x.isdigit())] # no number

set_masnavi = set(masnavi_nn)
set_stop_word = set(sw)
actual_words = set_masnavi.difference(set_stop_word)

masnavi_nsw = [x for x in masnavi_nn if x in actual_words] # no stop word



# Creating the word frequency distribution
freqdist = nltk.FreqDist(masnavi_nsw)
freq_dict = list(zip(freqdist.keys(), freqdist.values()))
freq_dict.sort(key=lambda x: x[1], reverse=True)
freq_dict = freq_dict[:45]

labels = [x[0] for x in freq_dict]
ticks = [bidialg.get_display(arabic_reshaper.reshape (x)) for x in labels]
values = [x[1] for x in freq_dict]
index = np.arange(len(values))
color =['gold']*5+['magenta']*(len(index)-5)
plt.title(bidialg.get_display(arabic_reshaper.reshape ('نمودار بسامد لغات در اشعار شیخ محمود شبستری')))
plt.xlabel(bidialg.get_display(arabic_reshaper.reshape ('لغات')))
plt.ylabel(bidialg.get_display(arabic_reshaper.reshape ('تعداد تکرار')))

plt.bar(index, values, color=color)
plt.xticks(index,ticks, rotation=60)
plt.show()
print(color)