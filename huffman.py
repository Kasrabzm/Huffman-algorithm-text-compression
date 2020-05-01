import pickle
from heapnode import HeapNode

class Huffman():
    def __init__(self):
        self.text_frequency = {}
        self.heap = []
        self.codes = {}
        self.reverse_mapping = {}
        self.one_char = False
        self.decoded_text = ""
        self.char = None

    def __make_frequency_dict__(self, text):
        """
        make a (char, frequency) pair dictionary from the given text input

        Arguments:
            text [str] -- text to parse through

        Returns:
            [dict] -- (char, frquency) pair dictionary
        """
        print("Generating frequency dictionary...")
        occ = {}
        for char in text:
            if char not in occ:
                occ[char] = 0
            occ[char] += 1
        self.text_frequency = occ
        print("Dictionary generated!")
        if len(self.text_frequency) == 1:
            print("Doctionary has only one item!")
            self.one_char = True
        return occ

    def __sort__(self):
        """
        sort the class heap object

        Returns:
            [list] -- sorted heap object
        """
        self.heap = sorted(self.heap, reverse=True)
        return self.heap

    def __make_nodes__(self, frequency_dict):
        """
        make HeapNode object from given frequncy dictionary

        Arguments:
            frequency_dict [dict] -- frequency dictionary

        Returns:
            [list] -- class heap object with created nodes
        """
        print("Generating first nodes...")
        for char in frequency_dict:
            self.heap.append(HeapNode(char, frequency=frequency_dict[char]))
        self.heap = self.__sort__()
        print("Node generation done!")
        return self.heap

    def __pop_last_node__(self, heap):
        """
        pop the last node of the given heap

        Arguments:
            heap [list] -- heap list of nodes

        Returns:
            [HeapNode] -- removed item from the heap list
        """
        return heap.pop(-1)

    def __merge_last_two_and_push__(self):
        """
        merge last two nodes of the heap, remove them and add the parent

        Returns:
            [list] -- class heap object
        """
        self.heap = self.__sort__()
        node1 = self.heap[-1]
        node2 = self.heap[-2]
        merged_node = HeapNode(None, node1.frequency + node2.frequency, left=node1, right=node2)
        self.heap.append(merged_node)
        self.heap = self.__sort__()
        return self.heap


    def __make_heap_tree__(self):
        """
        make a full heap tree with only one node (root node)

        Returns:
            [list] -- class heap object with only one node
        """
        print("Generating heap tree...")
        while not len(self.__sort__()) == 1:
            self.__merge_last_two_and_push__()
            for i in range(2):
                self.__pop_last_node__(self.heap)
            self.heap = self.__sort__()
        print("Heap tree generation done!")
        return self.heap

    def __pretraversal__(self, root, current_code=""):
        """
        preorder traversal method

        Arguments:
            node [HeapNode] -- node to traverse trough it's childrens

        Keyword Arguments:
            current_code [str] -- string for code (default: {""})
        """
        if root == None:
            return
        elif root.char != None:
            self.codes[root.char] = current_code
            self.reverse_mapping[current_code] = root.char

        self.__pretraversal__(root.left, current_code + "0")
        self.__pretraversal__(root.right, current_code + "1")

    def __get_encoded_text__(self, text):
        """
        convert text to codes

        Arguments:
            text [str] -- input text tot convert to code

        Returns:
            [str] -- encoded text
        """
        encoded_text = ""
        print("Generating encoded text...")
        for char in text:
            encoded_text += self.codes[char]
        print("Encoded text generated!")
        return encoded_text

    def __make_byte_array__(self, encoded_text):
        """
        make a byte array object from encoded text

        Arguments:
            encoded_text [str] -- encoded text to make byte array from

        Returns:
            [bytearray] -- byte array object created form encoded text
        """
        b = bytearray()
        byte = ""
        print("Generating bytearray...")
        if len(encoded_text) % 8 != 0:
            extra_zero = 8 - len(encoded_text) % 8
        else:
            extra_zero = 0

        for char in (encoded_text + "0" * extra_zero):
            byte += char
            if len(byte) == 8:
                b.append(int(bytes(byte, "utf-8"), 2))
                byte = ""
        print("Bytearray generated!")
        return b

    def compress(self, path):
        """
        compress a given file content to a .ckf file

        Arguments:
            path [str] -- path to the file to compress
        """
        file_name = path.split(".")[1].replace("/", "")
        with open(path, "r") as inputf:
            self.text = inputf.read()

        self.__make_frequency_dict__(self.text)
        self.__make_nodes__(self.text_frequency)
        self.__make_heap_tree__()
        self.__pretraversal__(self.heap[0], "")
        encoded_text = self.__get_encoded_text__(self.text)
        bytearray_encoded_text = self.__make_byte_array__(encoded_text)

        with open(file_name + ".ckf", "wb") as outputf:
            pickle.dump(self.heap, outputf)
            pickle.dump(bytearray_encoded_text, outputf)


    def __get_formated_text__(self, bytearray_encoded_text):
        """
        get bytes from a bytearray object to fromat them

        Arguments:
            bytearray_encoded_text [bytearray] -- bytearray object to format text

        Returns:
            [str] -- formated text
        """
        print("Generating fortmated text...")
        formated_text = ""
        for byte in bytearray_encoded_text:
            formated_text += "{0:08b}".format(byte)

        print("Formated text generated")
        return formated_text

    def __char_gen__(self, formated_text):
        """
        make a generator object form formated text

        Arguments:
            formated_text [str] -- formated text for generator

        Yields:
            [generator] -- generator object
        """
        for char in formated_text:
            yield char

    def __code_finder__(self, root):
        """
        find codes from the given tree object in the file

        Arguments:
            root [NodeHeap] -- whole tree object
        """
        if root.char != None:
            # print(root.char, end="")
            self.decoded_text += root.char
            return

        char = next(self.char)
        if char == "0":
            self.__code_finder__(root.left)
        elif char == "1":
            self.__code_finder__(root.right)


    def decompress(self, path):
        """
        decompress a .ckf file to a .txt

        Arguments:
            path [str] -- path to file
        """
        file_name = path.split(".")[1].replace("/", "")
        with open(path, "rb") as inputf:
            self.heap = pickle.load(inputf)
            bytearray_encoded_text = pickle.load(inputf)

        foramted_text = self.__get_formated_text__(bytearray_encoded_text)
        self.char = self.__char_gen__(foramted_text)
        print("Decompressing...")
        try:
            while True:
                self.__code_finder__(self.heap[0])
        except StopIteration:
            with open(file_name + "_dc.txt", "w") as outputf:
                outputf.write(self.decoded_text)
                print("Decompressing done!")
