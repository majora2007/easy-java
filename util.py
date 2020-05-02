import re
from collections import Counter
from re import split

def word_prob(word): return dictionary[word] / total
def words(text): return re.findall('[a-z]+', text.lower()) 
dictionary = Counter(words(open('words.txt').read()))
max_word_length = max(map(len, dictionary))
total = float(sum(dictionary.values()))

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