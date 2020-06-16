import math
import random
import time
import public_key_algorithms


# Get input from the user
def get_input(message):
    return int(input(message))


def numberDecomposition(n):
    exp = [0, 0]
    while n % 2 == 0:
        exp[0] = exp[0] + 1
        n = n // 2
    exp[1] = n
    return exp


# Implement the decryption exponent attack, return a non trivial factor of n and the total number of iterations
def decryptionexp(n, d, e):
    r, _m = numberDecomposition(e * d - 1)
    it = 0
    while True:
        it = it + 1
        x = random.randint(1, n - 1)
        if math.gcd(x, n) != 1:
            return x, it
        v = public_key_algorithms.fast_exp_alg(x, _m, n)
        if v == 1:
            continue
        while v != 1:
            v0, v = v, public_key_algorithms.fast_exp_alg(v, 2, n)
        if v0 != -1 and v0 != n - 1:
            return math.gcd(v0 + 1, n), it


# Print the Main Menu
def menu():
    print("---- Decryption Exponent Attack ----\n")
    print("1) Execute Decryption Exponent Attack.")
    print("2) Test Decryption Exponent Attack.")
    print("3) Quit.\n")
    try:
        choice = int(input("Select a function to run: "))
        if 1 <= choice <= 3:
            return choice
        else:
            print("\nYou must enter a number from 1 to 9\n")
    except ValueError:
        print("\nYou must enter a number from 1 to 9\n")
    input("Press Enter to continue.\n")


def main():
    while True:
        # Ask the user what function wants to run
        choice = menu()

        # Execute the function requested by the user

        if choice == 1:
            n = get_input("\nInsert the modulo n: ")
            d = get_input("Insert the exponent d of the private key: ")
            e = get_input("Insert the exponent e of the public key: ")
            factor, iteration = decryptionexp(n, d, e)
            print("\nNon Trivial Factor of n:", factor)
            print("Total Algorithm Iterations:", iteration, "\n")

        elif choice == 2:
            k = get_input("\nInsert the size of modules to be randomly generated (number of bits): ")
            iteration = get_input("Insert the total number of random modules to be tested: ")
            # Begin the test
            iteration_sum = 0
            decryptionexp_exec_time = []
            input("\nPress Enter to begin the test.\n")
            print("Test is Started.")
            for i in range(iteration):
                p_test, q_test, d_test = public_key_algorithms.generate_test_case(k)
                public_key, private_key = public_key_algorithms.generate_rsa_key(p_test, q_test, d_test)

                start = time.perf_counter()
                _, alg_iterations = decryptionexp(public_key[1], private_key[0], public_key[0])
                end = time.perf_counter()
                decryptionexp_exec_time.append(end - start)

                iteration_sum += alg_iterations
                print("\rCurrently Tested Modules:", i + 1, end="", flush=True)

            print("\nTest is completed.\n")

            # Calculate and display average algorithm iterations, average execution time and time variance
            avg_exec_time = sum(decryptionexp_exec_time) / iteration
            var_exec_time = sum(map(lambda x: (x - avg_exec_time) ** 2, decryptionexp_exec_time)) / iteration
            print("- Test Results -")
            print("Average Algorithm Iterations:", iteration_sum / iteration)
            print("Average Execution Time:", avg_exec_time, "seconds")
            print("Variance of Execution Time:", var_exec_time, "seconds^2\n")

        elif choice == 3:
            exit(0)


if __name__ == '__main__':
    main()
