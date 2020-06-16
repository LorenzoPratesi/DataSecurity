import math
import random
import time


# Compute the Fast modular exponentiation algorithm
def fast_exp_alg(a, n, m):
    d, c = 1, 0
    bin_n = "{0:b}".format(n)
    for i in bin_n:
        d = (d * d) % m
        if int(i) == 1:
            d = (d * a) % m
    return d


# Compute the extended euclidean algorithm, returns the GCD and the inverse of a mod b
def extended_euclidean_algorithm(a, b):
    rm = b
    rm1 = a
    qm1 = 1
    t = 0
    while rm1 != 0:
        q = math.floor(rm / rm1)
        temp = t
        t = qm1
        qm1 = temp - q * qm1
        temp = rm
        rm = rm1
        rm1 = temp - q * rm1
    if t < 0:
        t = t + b
    if rm > 1:
        t = "ND"
    return rm, t


# Compute the Miller-Rabin for a number given the number of rounds, return True if the number is composite
def rabin_test(x, n):
    m, r, xr = n - 1, 0, []
    while m % 2 == 0:
        m = m // 2
        r = r + 1
    xr.append(fast_exp_alg(x, m, n))
    for i in range(1, r + 1):
        xr.append(fast_exp_alg(xr[i - 1], 2, n))
    return (xr[0] != 1) and all(xi % n != n - 1 for xi in xr[0:-1])


# Generate a random k-bit prime number
def generate_random_prime(minimum, limit, accuracy):
    random_number = 0
    condition = True
    while condition:
        random_number = random.randint(minimum, limit)
        if random_number % 2 != 0:
            test_sample = [random.randint(2, limit) for i in range(0, accuracy)]
            condition = any(rabin_test(x, random_number) for x in test_sample)
    return random_number


# RSA encryption
def rsa_encrypt(m, kp):
    return fast_exp_alg(m, kp[0], kp[1])


# RSA decryption
def rsa_decrypt(c, km):
    return fast_exp_alg(c, km[0], km[1])


# Generates a RSA public and private key pair
def generate_rsa_key(p, q, d):
    n = p * q
    phi = (p - 1) * (q - 1)
    if d == 0:
        d = generate_random_prime(2, n - 1, 5)
        while extended_euclidean_algorithm(d, phi)[0] != 1:
            d = generate_random_prime(2, n - 1, 16)
    e = extended_euclidean_algorithm(d, phi)
    kp = (e[1], n)
    km = (d, n)
    return kp, km


# Generates a RSA public and private key pair with CRT
def generate_rsa_crt_key(p, q, d):
    n = p * q
    phi = (p - 1) * (q - 1)
    if d == 0:
        d = generate_random_prime(2, n - 1, 5)
        while d != 1 and extended_euclidean_algorithm(d, phi)[0] != 1:
            d = generate_random_prime(2, n - 1, 5)
    q_inv = extended_euclidean_algorithm(q, p)[1]
    p_inv = extended_euclidean_algorithm(p, q)[1]
    e = extended_euclidean_algorithm(d, phi)
    kp = (e[1], n)
    km = (p, q, d, p_inv * p, q_inv * q)
    return kp, km


# RSA decryption with CRT
def rsa_decrypt_crt(c, km):
    mp = fast_exp_alg(c, km[2], km[0])
    mq = fast_exp_alg(c, km[2], km[1])
    return ((mp * km[4]) + (mq * km[3])) % (km[0] * km[1])


def generate_test_case(dimension):
    big_p_test = generate_random_prime(10 ** dimension, (10 ** (dimension + 1)) - 1, 16)
    big_q_test = generate_random_prime(10 ** dimension, (10 ** (dimension + 1)) - 1, 16)
    big_phi_test = (big_p_test - 1) * (big_q_test - 1)
    big_n_test = big_p_test * big_q_test
    big_d_test = generate_random_prime(2, big_n_test - 1, 16)
    while big_d_test != 1 and extended_euclidean_algorithm(big_d_test, big_phi_test)[0] != 1:
        big_d_test = generate_random_prime(2, big_n_test - 1, 16)
    return big_p_test, big_q_test, big_d_test


def decrypting_test(cypher_text, keys):
    for c in cypher_text:
        rsa_decrypt(c, keys)


def decrypting_test_crt(cypher_text, keys):
    for c in cypher_text:
        rsa_decrypt_crt(c, keys)


# Print the Main Menu
def menu():
    print("---- Public Key Cryptography, RSA ----\n")
    print("1) Extended Euclidean Algorithm.")
    print("2) Fast Modular Exponentiation.")
    print("3) Miller-Rabin Test (True=Composite).")
    print("4) Prime Number Generator.")
    print("5) RSA keys Generator (Public and Private Key).")
    print("6) RSA Encryption.")
    print("7) RSA Decryption.")
    print("8) Test RSA Decryption with CRT.")
    print("9) Generate test case.")
    print("10) Quit.\n")

    try:
        choice = int(input("Select a function to run: "))
        if 1 <= choice <= 9:
            return choice
        else:
            print("\nYou must enter a number from 1 to 9\n")
    except ValueError:
        print("\nYou must enter a number from 1 to 9\n")
    input("Press Enter to continue.\n")


# Get input from the user
def get_input(message):
    return int(input(message))


def main():
    while True:
        # Ask the user what function wants to run
        choice = menu()

        # Execute the function requested by the user
        try:
            if choice == 1:
                a = get_input("\nInsert the first integer: ")
                b = get_input("Insert the second integer: ")
                gcd, inv = extended_euclidean_algorithm(a, b)
                print("\nGreatest Common Divisor (GCD):", gcd)
                print("inv: ", inv, "\n")

            elif choice == 2:
                a = get_input("\nInsert the base: ")
                exp = get_input("Insert the exponent: ")
                n = get_input("Insert the modulo: ")
                print("\nModular Exponentiation:", fast_exp_alg(a, exp, n), "\n")

            elif choice == 3:
                n = get_input("\nInsert an integer: ")
                rounds = get_input("Insert the number of rounds to execute (default=40): ")
                print("\nTest Miller-Rabin:", rabin_test(n, rounds), "\n")

            elif choice == 4:
                k = get_input("\nInsert number of bits (k>1): ")
                rounds = get_input("Insert the number of rounds for Miller-Rabin Test (default=40): ")
                print("\nGenerated Prime Number:", generate_random_prime(10 ** 2, 10 ** k, rounds), "\n")

            elif choice == 5:
                p = get_input("\nInsert the first prime number p: ")
                q = get_input("\nInsert the second prime number q: ")
                d = get_input("\nInsert the exponent d: ")
                public_key, private_key = generate_rsa_key(p, q, d)
                print("\nPublic Key (e, n):", public_key)
                print("Private Key (d, n):", private_key, "\n")

            elif choice == 6:
                m = get_input("\nInsert the message m: ")
                e = get_input("Insert the exponent e of the public key: ")
                n = get_input("Insert the modulo n of the public key: ")
                print("\nGenerated ciphertext c:", rsa_encrypt(m, (e, n)), "\n")

            elif choice == 7:
                c = get_input("\nInsert the ciphertext c: ")
                d = get_input("Insert the exponent d of the private key: ")
                n = get_input("Insert the modulo n of the private key: ")
                print("\nOriginal message m:", rsa_decrypt(c, (d, n)), "\n")

            elif choice == 8:
                p = get_input("\nInsert the first prime number p: ")
                q = get_input("\nInsert the second prime number q: ")
                d = get_input("\nInsert the exponent d: ")
                public_key, private_key = generate_rsa_crt_key(p, q, d)
                print("\nPublic Key (e, n):", public_key)
                print("Private Key (d, n):", private_key, "\n")

                m = get_input("\nInsert the message m: ")
                c = rsa_encrypt(m, public_key)
                print("\nGenerated ciphertext c:", c, "\n")

                m = rsa_decrypt_crt(c, private_key)
                print("\nOriginal message m:", m, "\n")

            elif choice == 9:
                dim = get_input("\nInsert the dimension: ")
                p_test, q_test, d_test = generate_test_case(dim)
                standard_test_keys = generate_rsa_key(p_test, q_test, d_test)
                print(standard_test_keys)

                crt_test_keys = generate_rsa_crt_key(p_test, q_test, d_test)
                print(crt_test_keys)

                plain_text_test = [random.randint(1, 10 ** dim) for i in range(0, 100)]
                cypher_text_test = [rsa_encrypt(m, standard_test_keys[0]) for m in plain_text_test]
                result_vector = [rsa_decrypt(c, standard_test_keys[1]) for c in cypher_text_test]
                result_vector_2 = [rsa_decrypt_crt(c, crt_test_keys[1]) for c in cypher_text_test]
                if result_vector == plain_text_test == result_vector_2:
                    print("\nBegin the test...\n")
                    decryption_exec_time = 0
                    crt_decryption_exec_time = 0
                    print("Test is Started.")

                    # RSA Decryption without CRT
                    start = time.perf_counter()
                    decrypting_test(cypher_text_test, standard_test_keys[1])
                    end = time.perf_counter()
                    decryption_exec_time += end - start

                    # RSA Decryption with CRT
                    start = time.perf_counter()
                    decrypting_test_crt(cypher_text_test, crt_test_keys[1])
                    end = time.perf_counter()
                    crt_decryption_exec_time += end - start

                    print("\nTest is completed.\n")

                    print("- RSA Decryption without CRT -")
                    print("Total Execution Time on 100 Random Ciphertext:", decryption_exec_time, "seconds")
                    print("\n- RSA Decryption with CRT -")
                    print("Total Execution Time on 100 Random Ciphertext:", crt_decryption_exec_time, "seconds\n")

                    print("\n- Speedup:", ((decryption_exec_time / crt_decryption_exec_time) - 1) * 100, "seconds\n")

                elif choice == 10:
                    exit(0)

        except ValueError:
            print("\nYou must enter an integer\n")
            input("Press Enter to continue.\n")


if __name__ == '__main__':
    main()
