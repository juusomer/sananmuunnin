from itertools import repeat
import numpy as np
import sananmuunnin as sm


MAX_LEN = 20
CHARACTERS = ["", " "] + list(sm.VOWELS + sm.CONSONANTS)
N_CHARACTERS = len(CHARACTERS)
PADDING = 0


class OneHot:

    def __init__(self):
        self._char_to_index = {
            char: index for index, char in enumerate(CHARACTERS)
        }
        self._index_to_char = {
            index: char for char, index in self._char_to_index.items()
        }

    def encode(self, string):
        n_padding = MAX_LEN - len(string)
        padding_indices = list(repeat(PADDING, n_padding))
        char_indices = [self._char_to_index[char] for char in string.lower()]
        return np.eye(N_CHARACTERS)[
            np.array(padding_indices + char_indices).reshape(-1)
        ]

    def decode(self, one_hot_matrix):
        return "".join(
            self._index_to_char[row.argmax()] for row in one_hot_matrix
        )
