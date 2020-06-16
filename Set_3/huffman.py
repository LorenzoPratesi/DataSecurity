import numpy as np
import networkx as nx
import matplotlib.pyplot as plt


def level_dict(node_path_dict):
    """
    From 'node_path_dict', a dictionary of levels and nodes/symbols of the
    corresponding levels is created.  The number of levels and the amount of
    nodes/symbols of each level could be used to position the nodes/symbols for
    clearer display of the graph.
    """
    level_dictionary = {}
    for key in node_path_dict.keys():
        temp_list = node_path_dict[key]
        i = 0
        for i in range(len(temp_list)):
            if i not in level_dictionary.keys():
                level_dictionary[i] = []
            if node_path_dict[key][i] not in level_dictionary[i]:
                level_dictionary[i].append(node_path_dict[key][i])
        if (i + 1) not in level_dictionary.keys():
            level_dictionary[i + 1] = []
        level_dictionary[i + 1].append(key)
    return level_dictionary


def node_posi(node_label, y_off, node_child_dict):
    """
    Calls the function 'posi_place' recursively starting from the root node.
    The termination condition is when a symbol is placed.  NetworkX has a grid
    from -1 to 1 in both the x and y directions.  The position of the root node
    is at 0,1.  The dictionary 'posi' will be returned and conforms to the
    format of NetworkX.
    """

    def posi_place(key, width=1.0):
        child0 = node_child_dict[key][0]
        child0_x = posi[key][0] - width / 2
        child0_y = posi[key][1] - y_off
        posi[child0] = np.array([child0_x, child0_y])
        if child0 in node_child_dict.keys():
            posi_place(child0, width / 2)

        child1 = node_child_dict[key][1]
        child1_x = posi[key][0] + width / 2
        child1_y = posi[key][1] - y_off
        posi[child1] = np.array([child1_x, child1_y])
        if child1 in node_child_dict.keys():
            posi_place(child1, width / 2)

    root_node = node_label + '0'
    posi = {root_node: np.array([0, 1])}
    posi_place(root_node)

    return posi


def node_symb_prob_dict(sym, prb, node_child_dict):
    """
    Creates a dictionary of symbols and probabilities from the list of symbols
    and probablities 'sym_prb_dict'.  Then based on the information in
    'node_child_dict', a dictionary of nodes and their children, the nodes and
    their cumulative probabilities are added into 'sym_prb_dict'.
    """
    sym_prb_dict = dict(zip(sym, prb))
    node_child_dict_cp = node_child_dict.copy()

    # At first, 'sym_prb_dict' contains only childrens of nodes.  Once the nodes
    # with children of symbols only are found in 'node_child_dict_cp', the nodes
    # are added into 'sym_prb_dict' and removed from 'node_child_dict_cp'.
    while len(node_child_dict_cp) != 0:
        key_del_list = []
        for key in node_child_dict_cp.keys():
            child = node_child_dict_cp[key]
            if child[0] in sym_prb_dict.keys() and child[1] in sym_prb_dict.keys():
                sym_prb_dict[key] = sym_prb_dict[child[0]] + sym_prb_dict[child[1]]
                key_del_list.append(key)
        for key in key_del_list:
            node_child_dict_cp.pop(key)
    return sym_prb_dict


def edge_labels(node_label, symb, code_dict):
    """
    Mostly a wrapper for the function 'path' since it is recursive and
    operates on an external dictionary 'node_path_dict'.  Once 'path' had
    been executed, a dictionary of (nodeX, nodeY) and 'x' where x is either
    '1' or '0' is generated.  This is the edge label format required by NetworkX
    """

    # ------------------------------------------------------------------
    def path(symb, node_path=[node_label + '0'], node_index=0):
        """
        Build a dictionary of symbols and a list of nodes from the root
        node to the symbol.  This uses similiar strategies as in 'node_child'.
        """
        n = node_index
        current_node_path = node_path.copy()
        for i in range(2):
            if type(symb[i]) == str:
                node_path_dict[symb[i]] = current_node_path
            else:
                node = node_label + str(n + 1)
                n = n + 1
                current_node_path.append(node)
                n = path(symb[i], current_node_path, n)
                current_node_path.pop()
        return n
        # ------------------------------------------------------------------

    # initialize an empty dictionary for function 'path' and call function
    node_path_dict = {}
    path(symb)

    e_labels_dict = {}
    # Populate 'e_labels_dict' with edges((nodeA,nodeB)) and the binary digit assosciated with that edge.
    for key in node_path_dict.keys():
        temp_list = node_path_dict[key]
        if len(temp_list) > 1:
            i = 0
            for i in range(len(temp_list) - 1):
                e_labels_dict[(temp_list[i], temp_list[i + 1])] = code_dict[key][i]
            e_labels_dict[(temp_list[i + 1], key)] = code_dict[key][i + 1]
        else:
            e_labels_dict[(temp_list[0], key)] = code_dict[key][0]

    return e_labels_dict, node_path_dict


def node_child_gen(symb, node_label):
    """
    Just a wrapper for the function 'node_child' since it is recursive and
    operates on an external dictionary 'node_child_dict'.
    """

    # ------------------------------------------------------------------
    def node_child(symb, node_index=0):
        """
        Build a dictionary of nodes and their immediate two children.
        The list 'symb' is a nested list of lists of symbols generated
        by the function 'group'.  When a list is encountered, a node name
        is created and added to the list 'kid'.  After both children are
        found, the node and its children are added to 'node_child_dict'.
        'node_child' is called recursively until a symbol of type str is
        encountered.
        """
        n = node_index
        current_node_index = n
        kid = []
        for i in range(2):
            if type(symb[i]) == str:
                kid.append(symb[i])
            else:
                node = node_label + str(n + 1)
                n = n + 1
                node_child_dict[node] = ''
                kid.append(node)
                n = node_child(symb[i], n)
        node_child_dict[node_label + str(current_node_index)] = kid
        return n
        # ------------------------------------------------------------------

    # create a dictionary with the root node and unknown children
    node_child_dict = {node_label + '0': ''}

    # call the function 'node_child' to populate node_child_dict
    node_child(symb)

    return node_child_dict


def huff_code(symb, prob):
    """
    Makes copies of the lists 'symb' and 'prob' then calls the function
    'group' to generate a nested list of lists of symbols representing
    the huffman code tree structure.  A dictionary 'code_dict' of symbols
    and binary code is created with the function 'bits'.
    """

    # ------------------------------------------------------------------
    def group(symb, prob):
        """
        Taking a list of symols('symb') and a corresponding list of
        probabilities('prob'), the two least probable symbols are first
        grouped into a list and added to 'symb' as a new "symbol".
        Their individual probabilities are deleted while their combined
        or summed probabilities are added to 'prob'.  This function is
        iteratively called until 'symb' only contains two items.
        """
        if len(symb) == 2:
            return
        else:
            new_p = 0
            min_sym_lst = []
            for i in range(2):
                min_p = min(prob)
                index = prob.index(min_p)
                min_s = symb[index]
                new_p = new_p + min_p
                min_sym_lst.append(min_s)
                prob.remove(prob[index])
                symb.remove(symb[index])
            prob.append(new_p)
            symb.append(min_sym_lst)
            group(symb, prob)

    # ------------------------------------------------------------------

    # ------------------------------------------------------------------
    def bits(symb, bitstr=''):
        """
        After the operation on the original 'symb' by the function 'group',
        'symb' contains a list where each list contains two items.
        Exploiting this fact, bit '0' or '1' is appended based on the
        object's index within the operated list.  This function is
        recursively called when each item is found in the list is a list.
        The termination condition is met when the item found in the list is
        a str.
        """
        for i in range(2):
            if type(symb[i]) == str:
                code_dict[symb[i]] = bitstr + str(i)
            else:
                bits(symb[i], bitstr + str(i))
        return

    # ------------------------------------------------------------------

    # make copies of lists 'sym and 'prb'
    sym_nest = symb.copy()
    prb_cpy = prob.copy()

    # modify sym_cpy to a list of lists containing symbols and or lists
    group(sym_nest, prb_cpy)

    # global dict of key(symbol) and value(code)
    code_dict = {}

    # populate code_dict with key(symbol) and value(1's and 0's)
    bits(sym_nest)

    return sym_nest, code_dict


def avg_code_length(code_dict, prb):
    total = sum(prb)
    prob_dict = [round(i / total, 3) for i in prb]
    return sum([prob_dict[list(code_dict).index(code)] * len(code_dict[code]) for code in code_dict])


def count_character(text):
    sym, freq, prb = [], [], []
    text_no_space = text.replace(" ", "")
    for character in list(map(chr, range(97, 123))):
        char_n = text_no_space.count(character)
        if char_n is not 0:
            sym.append(character)
            freq.append(char_n)
            prb.append(round(char_n / len(text), 3))
    return sym, freq, prb


def huff_encoder(code_dict, text):
    return ''.join(code_dict[character] for character in text)


def huff_decoder(code_dict, encoded_data):
    def decoder_generator(_, text):
        _lookup = {v: k for k, v in _.items()}
        while text:
            _options = [i for i in _lookup if
                        text.startswith(i) and (any(text[len(i):].startswith(v) for v in _lookup) or not text[len(i):])]
            if not _options:
                raise Exception("Decoding error")
            yield _lookup[_options[0]]
            text = text[len(_options[0]):]

    return ''.join(decoder_generator(code_dict, encoded_data))


# Print the Main Menu
def menu():
    print("---- Huffman Codes ----\n")
    print("1) Encode text.")
    print("2) Decode text.")
    print("3) Plot Huffman tree from the previous encoding text.")
    print("4) Quit.\n")
    try:
        choice = int(input("Select a function to run: "))
        if 1 <= choice <= 4:
            return choice
        else:
            print("\nYou must enter a number from 1 to 4\n")
    except ValueError:
        print("\nYou must enter a number from 1 to 4\n")
    input("Press Enter to continue.\n")


def main():
    plain, encoded_data = "", ""
    sym, sym_nest, freq, prb = [], [], [], []
    code_dict = {}

    while True:
        # Ask the user what function wants to run
        choice = menu()
        if choice == 1:
            plain = input("\nInsert some text to be encoded, leave blank if you want to test an example: ")
            if plain is "":
                plain = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaacccccccccccccccccccccccccaaaaaaaaaadddddddddddddddddddddddddaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaabbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
                print("Text to be encoded: \n", plain, "\n")

            plain = plain.replace(" ", "")

            sym, freq, prb = count_character(plain)
            sym_nest, code_dict = huff_code(sym, freq)
            L = avg_code_length(code_dict, freq)

            encoded_data = huff_encoder(code_dict, plain)

            print('Huffman Code Dictionary')
            print(code_dict)
            print('-----------------------\n')

            print('Nested List of Lists and Symbols')
            print(sym_nest)
            print('--------------------------------\n')

            print('Huffman data encoded')
            print(encoded_data)
            print('--------------------------------\n')

            print('Average code length')
            print(L)
            print('--------------------------------\n')

        elif choice == 2:
            if encoded_data is "":
                print("\nYou need to enter a text to be encoded before doing this function.\n")
            else:
                decoded_data = huff_decoder(code_dict, encoded_data)

                print('Huffman data decoded')
                print(decoded_data)
                print('--------------------------------\n')

        elif choice == 3:
            node_child_dict = node_child_gen(sym_nest, 'N')
            print('Dictionary of Nodes and Their Children')
            print(node_child_dict)
            print('--------------------------------------\n')

            e_labels_dict, node_path_dict = edge_labels('N', sym_nest, code_dict)
            print('Edge Labels of the Graph')
            print(e_labels_dict)
            print('------------------------\n')
            print('\n\n')
            print('Dictionary of Symbols and Their Paths')
            print(node_path_dict)
            print('-------------------------------------\n')

            spd_cpy = node_symb_prob_dict(sym, prb, node_child_dict)
            print('Node Labels in Probability or Frequency')
            print(spd_cpy)
            print('---------------------------------------\n')

            level_dictionary = level_dict(node_path_dict)

            # y-offset.  Since the total height of the graph is 2, the y-axis increment is 2/levels
            y_off = 2 / len(level_dictionary)

            posi = node_posi('N', y_off, node_child_dict)

            print('Levels of the Graph and Node/Symbols in the Level')
            print(level_dict)
            print('-------------------------------------------------\n')
            print('\n\n')
            print('The positions of Nodes and Symbols')
            print(posi)
            print('----------------------------------\n')

            def huff_graph(labels):
                node = labels[0] == 'N'

                plt.clf()
                G = nx.Graph(node_child_dict)
                pos = posi
                nx.draw(G, pos=pos, with_labels=node, node_size=1000, node_color='#ebf6ff', edgecolors='#000')
                nx.draw_networkx_edge_labels(G, pos, edge_labels=e_labels_dict, font_color='blue')
                if not node:
                    nx.draw_networkx_labels(G, pos=posi, labels=spd_cpy)

                plt.savefig('huffman_tree.png')
                plt.show()

            huff_graph('P')

        elif choice == 3:
            exit(0)


if __name__ == '__main__':
    main()
