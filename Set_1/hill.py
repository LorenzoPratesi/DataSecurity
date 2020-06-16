import math
import random

import numpy as np
from collections import OrderedDict

# dictionary for keyboard characters
alphabet = '0213456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~ \t\x0b2'


def cipher_operation(operation_type, message):
    if operation_type == 'e':
        dimension = int(input("What dimension would you like your key to be? "))
        encrypted = encrypt(message, dimension)
        print("Encrypted message: ", encrypted[0])
        print("Key: ", encrypted[1])

    elif operation_type == 'd':
        key = input("What is your key? ")
        decrypted = decrypt(message, key)
        print("Unscrambled message: ", decrypted)


def inverse_matrix(inputMatrix, modulo):
    # Inverted modulus matrix subroutine
    a = inputMatrix
    m = modulo
    p = np.round(np.linalg.det(a) * np.linalg.inv(a))
    a = np.round(np.linalg.det(a))
    num = np.arange(1, m + 1)  # creates a modulo dictionary
    res = np.mod(a * num, m)
    b = np.where(res == 1)
    err = np.size(b)
    if err == 0:
        print("The matrix has no modular inverse")
        return 0
    b = b[0].item(0) + 1
    return np.mod(b * p, m).astype(int)


def random_mod_matrix(min, max, dimension):
    random_matrix = np.random.randint(min, max, dimension)
    if random_matrix.all == 0:
        random_matrix = random_mod_matrix(min, max, dimension)
    else:
        inverse_mod = inverse_matrix(random_matrix, max)
        if np.size(inverse_mod) == 1:
            return random_mod_matrix(min, max, dimension)
    return random_matrix


def text_to_matrix(dimension, text):
    plaintext_matrix_dimension = (dimension, np.ceil(len(text) / dimension).astype(int))
    p = to_matrix(text, plaintext_matrix_dimension, alphabet)
    return p


def to_matrix(message, dimension, character_string):
    modulo = len(character_string) - 1
    character_to_number = OrderedDict(zip(character_string, range(0, modulo)))
    return np.resize([character_to_number[x] for x in list(message)], dimension)


def to_message(matrix, character_string):
    modulo = len(character_string) - 1
    number_to_character = OrderedDict(zip(range(0, modulo), character_string))
    return ''.join(number_to_character[x] for x in list(np.concatenate(list(matrix))))


def encrypt(input_message, dimension):
    modulo = len(alphabet) - 1
    input_message_matrix = text_to_matrix(dimension, input_message)
    cipher_matrix_dimension = (dimension, dimension)
    cipher_matrix = random_mod_matrix(0, modulo, cipher_matrix_dimension)
    key_matrix = inverse_matrix(cipher_matrix, modulo)
    scrambled_message_matrix = np.mod(np.dot(cipher_matrix, input_message_matrix), modulo)
    return to_message(scrambled_message_matrix, alphabet), to_message(key_matrix, alphabet)


def decrypt(input_message, key):
    modulo = len(alphabet) - 1
    key_matrix_column_length = int(len(key) ** .5)
    key_matrix_dimension = (key_matrix_column_length, key_matrix_column_length)
    scrambled_message_matrix_dimension = (
        key_matrix_column_length, int(np.ceil(len(input_message) / key_matrix_column_length))
    )
    key_matrix = to_matrix(key, key_matrix_dimension, alphabet)
    scrambled_message_matrix = to_matrix(input_message, scrambled_message_matrix_dimension, alphabet)
    unscrambled_message_matrix = np.mod(np.dot(key_matrix, scrambled_message_matrix), modulo)
    return to_message(unscrambled_message_matrix, alphabet)


def get_star_matrix(p, c, dimension):
    modulo = len(alphabet) - 1

    p_star = np.zeros(shape=(dimension, dimension), dtype=int)
    c_star = np.zeros(shape=(dimension, dimension), dtype=int)
    index = det = 0
    while det <= 0 or math.gcd(det, modulo) != 1:
        chosenBlocks = random.sample(range(np.size(p, 0)), dimension)
        chosenBlocks.sort()
        for i in chosenBlocks:
            p_star[index] = p[i]
            c_star[index] = c[i]
            index += 1
        p_star = p_star.transpose()
        c_star = c_star.transpose()
        det = int(round(np.linalg.det(p_star)))  # compute determinant of p_star
        index = 0
    return c_star, p_star


def known_plaintext_attack(plaintext, ciphertext, dimension):
    modulo = len(alphabet) - 1

    p = text_to_matrix(dimension, plaintext)
    c = text_to_matrix(dimension, ciphertext)

    c_star, p_star = get_star_matrix(p, c, dimension)

    inverse_p_star = inverse_matrix(p_star, modulo)
    key = c_star.dot(inverse_p_star) % modulo
    return to_message(key, alphabet)


def main():
    while True:
        print("---- Hill Cipher ----")
        print("1) Encrypt a Message.")
        print("2) Decrypt a Message.")
        print("3) Force a Ciphertext (Known Plaintext Attack).")
        print("4) Quit.\n")

        command = int(input("Select an option: "))

        if command == 1:
            msg = input("Enter the message to be encrypted: ")
            cipher_operation('e', msg)

        elif command == 2:
            msg = input("Enter the message to be decrypted: ")
            cipher_operation('d', msg)

        elif command == 3:
            plaintext = input("Enter the known plaintext: ")
            ciphertext = input("Enter the ciphertext: ")
            dimension = int(input("Enter the key dimension: "))

            key = known_plaintext_attack(plaintext, ciphertext, dimension)
            print("The key retrived is: ", key)

        elif command == 4:
            break

        else:
            print("Only one character from 1 to 4 is accepted\n")


if __name__ == "__main__":
    main()
