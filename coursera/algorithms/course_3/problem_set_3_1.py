"""
Your task in this problem is to run the
Huffman coding algorithm from lecture on
this data set.

1) What is the maximum length of a codeword
in the resulting Huffman code?

2) What is the minimum length of a codeword
in your Huffman code?
"""

import heapq


class Symbol:
    def __init__(self, symbol, freq):
        self.symbol = symbol
        self.freq = freq

    def is_singleton(self):
        return not isinstance(self.symbol, tuple)

    def expand(self):
        return self.symbol

    def __lt__(self, other):
        return self.freq < other.freq

    def __gt__(self, other):
        return self.freq > other.freq


class Huffman:
    def __init__(self, symbol_list):
        self.symbol_list = symbol_list
        self.symbol_encoding = {}

    def _expand_symbols(self, sym_tree, path):
        if sym_tree.is_singleton():
            sym = sym_tree.symbol
            self.symbol_encoding[sym] = path

        else:
            left, right = sym_tree.expand()
            self._expand_symbols(left, path + '0')
            self._expand_symbols(right, path + '1')

    def encode(self):
        # starting bottom up merge until 1 symbol only
        heapq.heapify(self.symbol_list)
        while len(self.symbol_list) > 1:
            symb_1 = heapq.heappop(self.symbol_list)
            symb_2 = heapq.heappop(self.symbol_list)
            new_symb = Symbol(
                symbol=(symb_1, symb_2),
                freq=symb_1.freq + symb_2.freq)
            heapq.heappush(self.symbol_list, new_symb)

        # now expand the symbols
        sym_tree = self.symbol_list[0]
        self._expand_symbols(sym_tree=sym_tree, path='')

    def get_encoding(self):
        if not self.symbol_encoding:
            self.encode()

        return self.symbol_encoding

    def min_code_word(self):
        if not self.symbol_encoding:
            self.encode()

        min_sym = None
        min_len = None
        for sym, cw in self.symbol_encoding.items():
            if not min_sym:
                min_sym = sym
                min_len = len(cw)

            elif len(cw) < min_len:
                min_sym = sym
                min_len = len(cw)

        return min_sym, min_len

    def max_code_word(self):
        if not self.symbol_encoding:
            self.encode()

        max_sym = None
        max_len = None
        for sym, cw in self.symbol_encoding.items():
            if not max_sym:
                max_sym = sym
                max_len = len(cw)

            elif len(cw) > max_len:
                max_sym = sym
                max_len = len(cw)

        return max_sym, max_len


def main():
    data = "/Users/brendonsullivan/Documents/docs/coursera_hw/huffman.txt"
    sym_list = []
    with open(data, 'r') as f:
        for index, line in enumerate(f):
            # skipping header row
            if index == 0:
                continue
            sym = Symbol(symbol=index, freq=int(line))
            sym_list.append(sym)
    encoding = Huffman(sym_list)
    print(encoding.max_code_word())
    print(encoding.min_code_word())


if __name__ == '__main__':
    main()
