import pyperclip
import re
from functools import reduce
from math import gcd
from string import ascii_uppercase

import numpy as np

from Vigenere import vigenereCipher

LETTERS = [letter for letter in ascii_uppercase]

# If set to True, program doesn't print anything
NON_LETTERS_PATTERN = re.compile('[^A-Z]')


def main():
    cipherText = "PNHEUAAMRMSLYZPSKWAUGAICLLMEDMDEGAEYAEZOWSEIGBWZUTJTYYFWRLEHFWFWRJWIAZLPYMMYPMGRFXPQHVOWVIZOJMLPZMLRVCHIYMMXLALNUUQWRKIXPVOFLJAFGAIHHGEHVEAOQVMEPHPNCCBEYEIEPMCWRQETENGVKWHNRLPDVXHJLAZFTMGRFXRZABSAKRTEEXAZBTOBVKGCURSFJWFLUBAUAEIDZGZUNCDEZBROLLEOJRQPUXVZPKLLCWUNGAIHHGSEJYUDUHTPMCWLPUQMVZLEJIECYQAMRUSOFBSEJMXDVXVDHQOAEYESNLWTUEPRVYXWNRWZUBSECMAKBNXQVZEHVQQCBGWAPZLTFPEYBNOYVEUUJRMSPBXTGMYRFZQSCBICYMEECJEUFGSHOMSEJGFAGXHEBZYEURAHVLGZSTPAXSQTERMYNBZRVKQMOXVHOIEHVUMSFNTAVAPDKMEALHLJLANAEUQOSYICFWFAECECBKXNPBTZVLPECNXJAWLPCYOEBYKCLIEEIQMFRMCEOMRRRTQCNFMWSMDAZBFHRZVLCM"
    hackedMessage = hackVigenere(cipherText)

    if hackedMessage is not None:
        print('Copying hacked message to clipboard...')
        print(hackedMessage)
        pyperclip.copy(hackedMessage)
    else:
        print('Failed to break encryption...')


def generateTriple(message):
    length = len(message) - 2
    return iter([message[i:i + 3] for i in range(length) if i < length])


def findRepeatSequenceSpacings(message):
    # Goes through the message and finds any 3 letter sequences
    # that are repeated. Returns a dict with the keys of the sequence and
    # values of a list of spacings (num of letters between the repeats).

    # Use a regular expression to remove non-letters from the message:
    message = NON_LETTERS_PATTERN.sub('', message.upper())
    # Compile a list of seqLen-letter sequences found in the message
    # keys = sequences, values = list of in spacings

    triple = generateTriple(message)

    dic = {}
    for i in range(len(message) - 2):
        tri = next(triple)
        dic[tri] = message.count(tri)

    max_val = max(dic, key=dic.get)

    triple = generateTriple(message)

    seqSpacings = []
    value = first = 0

    for i in range(len(message) - 2):
        if max_val == next(triple):
            if first > 0:
                seqSpacings.append(i - value)
            if first == 0:
                value = i
                first = 1

    return seqSpacings


def kasiskiExamination(ciphertext):
    # Find sequences of 3 to 5 chars that appear multiple times
    repeatedSeqSpacings = findRepeatSequenceSpacings(ciphertext)
    return reduce(gcd, repeatedSeqSpacings)


def shiftEncryption(string, k):
    # Shift encryption di string
    # each letter will be shifted of k position
    stringArray = np.array([LETTERS.index(letter) for letter in string])
    shiftedStringArray = [None] * len(stringArray)

    for i in range(len(stringArray)):
        shiftedStringArray[i] = (stringArray[i] - k) % 26

    return "".join([LETTERS[i] for i in np.array(shiftedStringArray).tolist()])


def computeLetterFrequencies(string):
    # Compute the frequency of each letter of string
    return [string.count(letter) for letter in LETTERS]


def findKeyElement(substring):
    # After substring have been shifted of k index, do the dot product of enLetterFreq
    # and the computed frequencies of the shifted substring
    # letter frequency in the english dictionary
    enLetterFreq = [0.08167, 0.01492, 0.02782, 0.04253, 0.12702,
                    0.02228, 0.02015, 0.06094, 0.06966, 0.00153,
                    0.00772, 0.04025, 0.02406, 0.06749, 0.07507,
                    0.01929, 0.00095, 0.05987, 0.06327, 0.09056,
                    0.02758, 0.00978, 0.02360, 0.00150, 0.01974, 0.00074]

    maxDotProd = 0
    maxKey = None

    for letter in LETTERS:
        letterValue = LETTERS.index(letter)
        shiftedSubString = shiftEncryption(substring, letterValue)
        dotProd = np.dot(computeLetterFrequencies(shiftedSubString), enLetterFreq)
        if dotProd > maxDotProd:
            maxDotProd = dotProd
            maxKey = letter

    return maxKey


def attemptHackWithKeyLength(ciphertext, mostLikelyKeyLength):
    # Determine the most likely letters for each letter in the key:
    ciphertextUp = ciphertext.upper()

    substrings = getSubstings(ciphertext, mostLikelyKeyLength)

    possibleKey = ""
    for i in range(len(substrings)):
        possibleKey += str(findKeyElement(substrings[i]))

    decryptedText = vigenereCipher.decryptMessage(possibleKey, ciphertextUp)
    print('Possible encryption hack with key %s: ' % possibleKey)
    print(decryptedText[:200])
    print()

    return decryptedText


def getSubstings(ciphertext, mostLikelyKeyLength):
    substrings = []
    for i in range(0, mostLikelyKeyLength):
        txt = ''
        for j in range(i, len(ciphertext), mostLikelyKeyLength):
            txt += ciphertext[j]
        substrings.append(txt)
    return substrings


def hackVigenere(ciphertext):
    # First, we need to do Kasiski Examination to figure out what the
    # length of the ciphertext's encryption key is:
    keyLength = kasiskiExamination(ciphertext)
    print('Kasiski Examination results say the most likely key length are: ', keyLength)

    print('Attempting hack with key length %s...' % keyLength)
    hackedMessage = attemptHackWithKeyLength(ciphertext, keyLength)

    return hackedMessage


# If ran instead of imported
if __name__ == '__main__':
    main()
