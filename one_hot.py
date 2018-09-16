from itertools import repeat
import numpy as np


class OneHot:

    def __init__(self, characters, max_len, padding=0):
        self.max_len = max_len
        self.characters = characters
        self._padding = 0
        self._char_to_index = {
            char: index for index, char in enumerate(characters)
        }
        self._index_to_char = {
            index: char for char, index in self._char_to_index.items()
        }

    @property
    def n_characters(self):
        return len(self.characters)

    def encode(self, string):
        n_padding = self.max_len - len(string)
        padding_indices = list(repeat(self._padding, n_padding))
        char_indices = [self._char_to_index[char] for char in string.lower()]
        return np.eye(self.n_characters)[
            np.array(padding_indices + char_indices).reshape(-1)
        ]

    def decode(self, one_hot_matrix):
        return "".join(
            self._index_to_char[row.argmax()] for row in one_hot_matrix
        )
