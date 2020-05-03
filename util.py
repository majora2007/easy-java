import re
from collections import Counter
from re import split

from os import chdir, environ
from os.path import join, dirname
import sys

def pyinstaller_get_full_path(filename):
    """ If bundling files in onefile with pyinstaller, use thise to get the temp directory where file actually resides """
    if hasattr(sys, '_MEIPASS'):
        # PyInstaller >= 1.6
        #chdir(sys._MEIPASS)
        filename = join(sys._MEIPASS, filename)
    elif '_MEIPASS2' in environ:
        # PyInstaller < 1.6 (tested on 1.5 only)
        #chdir(environ['_MEIPASS2'])
        filename = join(environ['_MEIPASS2'], filename)
    else:
        #chdir(dirname(sys.argv[0]))
        filename = join(dirname(sys.argv[0]), filename)
    
    return filename




words_path = pyinstaller_get_full_path('words.txt')

def word_prob(word): return dictionary[word] / total
def words(text): return re.findall('[a-z]+', text.lower()) 
dictionary = Counter(words(open(words_path).read()))
max_word_length = max(map(len, dictionary))
total = float(sum(dictionary.values()))
print('Loading words.txt from {0}'.format(words_path))

print('total: {0}'.format(total))

def viterbi_segment(text):
    probs, lasts = [1.0], [0]
    for i in range(1, len(text) + 1):
        prob_k, k = max((probs[j] * word_prob(text[j:i]), j)
                        for j in range(max(0, i - max_word_length), i))
        probs.append(prob_k)
        lasts.append(k)
    words = []
    i = len(text)
    while 0 < i:
        words.append(text[lasts[i]:i])
        i = lasts[i]
    words.reverse()
    return words, probs[-1]


def first_upper(s):
    return s[0].upper() + s[1:]

def camel_case(s):
    sentence = ' '.join(viterbi_segment(s.lower())[0])
    word = ''.join(a.capitalize() for a in split('([^a-zA-Z0-9])', sentence)
       if a.isalnum())
    return word[0].lower() + word[1:]

def first_chars(s):
    """ Returns first characters combined of string. ApplicationGroup returns ag """
    words = viterbi_segment(s.lower())[0]
    end = len(words) - 1
    return ''.join(words[0:end])

def spinal_case(s):
    sentence = ' '.join(viterbi_segment(s.lower())[0])
    word = '-'.join(a.capitalize() for a in split('([^a-zA-Z0-9])', sentence)
       if a.isalnum())
    return word


if __name__ == '__main__':
    print(viterbi_segment('ACTIONITEMIMPACTID'.lower()))

    sentence = ' '.join(viterbi_segment('ACTIONITEMIMPACTID'.lower())[0])
    print('sentence: {0}'.format(sentence))
    word = ''.join(a.capitalize() for a in split('([^a-zA-Z0-9])', sentence)
       if a.isalnum())
    print('word: {0}'.format(word[0].lower() + word[1:]))