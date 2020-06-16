import numpy as np
import os

random_character_distribution = dict.fromkeys(list(map(chr, range(97, 123))), 1 / 26)
english_character_distribution = {'a': 0.08167, 'b': 0.01492, 'c': 0.02782, 'd': 0.04253, 'e': 0.12702, 'f': 0.02228,
                                  'g': 0.02015, 'h': 0.06094, 'i': 0.06966, 'j': 0.00153, 'k': 0.00772, 'l': 0.04025,
                                  'm': 0.02406, 'n': 0.06749, 'o': 0.07507, 'p': 0.01929, 'q': 0.00095, 'r': 0.05987,
                                  's': 0.06327, 't': 0.09056, 'u': 0.02758, 'v': 0.00978, 'w': 0.02360, 'x': 0.00150,
                                  'y': 0.01974, 'z': 0.00074}


def count_character(text):
    occurrences = dict()

    for character in list(map(chr, range(97, 123))):
        occurrences[character] = text.count(character)
    total = sum(occurrences.values())

    for character in occurrences:
        occurrences[character] /= total
    return occurrences


def kl_divergence(p, q):
    return sum(p[letter] * np.log2(p[letter] / q[letter]) for letter in p)


def shift(seq, n):
    return seq[n:] + seq[:n]


def hypothesis_testing(text):
    occurrences = count_character(text)
    english_result = []
    english_result_qp = []
    random_result_qp = []
    random_result = []
    for n in range(0, 26):
        shifted_occurrences = dict(zip(list(occurrences.keys()), shift(list(occurrences.values()), n)))
        english_result.append(abs(kl_divergence(english_character_distribution, shifted_occurrences)))
        english_result_qp.append(abs(kl_divergence(shifted_occurrences, english_character_distribution)))
        random_result.append(abs(kl_divergence(random_character_distribution, shifted_occurrences)))
        random_result_qp.append(abs(kl_divergence(shifted_occurrences, random_character_distribution)))
    result = [] * 4  # result, divergence, an, bn
    if min(english_result) < min(random_result):
        result.append("H0 - Inglese")
        result.append(min(english_result))
        result.append(np.exp2(-len(occurrences.keys()) * min(english_result_qp)))
    else:
        result.append("H1 - Casuale")
        result.append(min(random_result))
        result.append(np.exp2(-len(occurrences.keys()) * min(random_result_qp)))
    result.append(np.exp2(-len(occurrences.keys()) * result[1]))
    return result


if __name__ == '__main__':
    results = []
    for file in os.listdir("ExerciseText/"):
        if file.endswith(".txt"):
            results.append(hypothesis_testing(open(file="ExerciseText/" + file, encoding="utf8").read()))

    print(len(list(filter(lambda x: "random" in x, os.listdir("ExerciseText/")))))
    print(len(list(filter(lambda x: "H1" in x[0], results))))
    print(len(list(filter(lambda x: "random" not in x, os.listdir("ExerciseText/")))))
    print(len(list(filter(lambda x: "H0" in x[0], results))))
