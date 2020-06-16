import re
import math
import matplotlib.pyplot as plot


def get_text():
    return open("texts/Moby_Dick_chapter_one.txt", 'r').read().replace('\n', '')


def trim_text(text):
    text = text.upper()  # conversione in maiuscolo
    text = re.sub(r"['\",.;:_@#()”“’—?!&$\n]+ *", " ", text)  # conversione dei caratteri speciali in uno spazio
    text = text.replace("-", " ")  # conversione del carattere - in uno spazio
    text = text.replace(" ", "")  # rimozione spazi
    return text


def get_letter_count(message, m):
    # Returns a dictionary with keys of single letters and values of the
    # count of how many times they appear in the message parameter:
    letter_count = {}
    for i in range(0, len(message)):
        t = message[i * m:(i * m) + m]
        if len(t) == m:
            if t in letter_count:
                letter_count[t] += 1
            else:
                letter_count[t] = 1

    return letter_count


def get_item_at_index_zero(items):
    return items[0]


def get_item_at_index_one(items):
    return items[1]


def get_frequency_order(message, m):
    # First, get a dictionary of each letter and its frequency count:
    letter_to_freq = get_letter_count(message, m)

    # convert the letter_to_freq dictionary to a list of
    # tuple pairs (key, value), then sort them:
    freq_pairs = list(letter_to_freq.items())
    freq_pairs.sort(key=get_item_at_index_one, reverse=True)

    xlist, ylist = set_xy_plot(freq_pairs)

    createPlot(xlist, ylist, 'letter', 'frequency', 'LetterFrequency', get_number_x_data(m))

    return freq_pairs


def get_m_grams_distributions(message, m):
    letter_to_freq = get_letter_count(message, m)
    total_grams = sum(letter_to_freq.values())

    grams_dict = {}
    for k in letter_to_freq.keys():
        grams_dict[k] = letter_to_freq[k] / total_grams

    sorted_grams_dict = list(grams_dict.items())
    sorted_grams_dict.sort(key=get_item_at_index_one, reverse=True)

    xlist, ylist = set_xy_plot(sorted_grams_dict)

    createPlot(xlist, ylist, 'letter', 'probability', 'distribution', get_number_x_data(m))

    return sorted_grams_dict


def get_number_x_data(m):
    if m == 1:
        number_x_data = 26
    elif m == 2:
        number_x_data = 20
    elif m == 3:
        number_x_data = 17
    elif m == 4:
        number_x_data = 13
    else:
        number_x_data = 10
    return number_x_data


def set_xy_plot(dict):
    xlist = [dict[i][0] for i in range(len(dict))]
    ylist = [dict[i][1] for i in range(len(dict))]
    return xlist, ylist


def index_of_confidence(message, m):
    letter_to_freq = get_letter_count(message, m)
    ic = 0.0
    total_grams = sum(letter_to_freq.values())

    for value in letter_to_freq.values():
        ic += (value * (value - 1)) / (total_grams * (total_grams - 1))
    return ic


def entropy(message, m):
    letter_to_freq = get_letter_count(message, m)
    e = 0.0
    n = math.ceil(len(message) / m)

    for value in letter_to_freq.values():
        e += (value / n) * math.log(value / n, 2)

    return -e


def createPlot(x_data, y_data, x_label, y_label, plot_title, number_x_data=26):
    if number_x_data is not None:
        x_data = x_data[0:number_x_data]
        y_data = y_data[0:number_x_data]

    plot.bar(x_data, y_data)
    plot.xlabel(x_label)
    plot.ylabel(y_label)
    plot.title(plot_title)
    plot.show()


# Print the main menu and asks user input
def menu():
    while True:
        print("\n---- Text Frequencies Analysis ----\n")
        print("1) Histogram of the frequency of the 26 letters.")
        print("2) Empirical distribution of m-grams.")
        print("3) Index of coincidence and entropy of the m-grams distribution.")
        print("4) Quit.\n")
        try:
            choice = int(input("Select a function to run: "))
            if 1 <= choice <= 4:
                return choice
            else:
                print("\nYou must enter a number from 1 to 4\n")
        except ValueError:
            print("\nYou must enter a number from 1 to 4\n")


def main():
    # Read Moby_Dick_chapter_one.txt and sanitize for the analysis
    text = trim_text(get_text())
    # text = trim_text("hello world")

    while True:
        choice = menu()
        if choice == 1:
            m = int(input("\nInsert the parameter m for the m-grams: "))
            letter_order = get_frequency_order(text, m)
            print("\nLetter ordered by frequencies: ", letter_order)
            print("\nHistogram has been plotted...")
            input("\nPress Enter to continue.")
        elif choice == 2:
            m = int(input("\nInsert the parameter m for the m-grams: "))
            distrib = get_m_grams_distributions(text, m)
            print("\nEmpirical distribution of q-grams:\n", distrib)
            input("\nPress Enter to continue.")
        elif choice == 3:
            # m = int(input("\nInsert the parameter m for the m-grams: "))
            for m in range(1, 5):
                ic = index_of_confidence(text, m)
                print("\nIndex of coincidence of the ", m, "-grams distribution: ", ic)
                print("Entropy of the m-grams distribution: ", entropy(text, m))
            input("\nPress Enter to continue.")
        elif choice == 4:
            break


if __name__ == '__main__':
    main()
