from itertools import repeat
import numpy as np
import sananmuunnin as sm


START_TOKEN = "\t"
END_TOKEN = "\n"

CHARACTERS = [START_TOKEN, END_TOKEN, " "] + list(sm.VOWELS + sm.CONSONANTS)
N_CHARACTERS = len(CHARACTERS)

START_TOKEN_INDEX = CHARACTERS.index(START_TOKEN)
END_TOKEN_INDEX = CHARACTERS.index(END_TOKEN)


class OneHot:

    def __init__(self):
        self._char_to_index = {
            char: index for index, char in enumerate(CHARACTERS)
        }
        self._index_to_char = {
            index: char for char, index in self._char_to_index.items()
        }

    def encode(self, string, length=None):
        length = len(string) if length is None else length
        output = np.zeros((length, N_CHARACTERS))
        for i, char in enumerate(string):
            output[i, self._char_to_index[char]] = 1
        return output

    def decode(self, one_hot_matrix):
        return "".join(
            self._index_to_char[row.argmax()]
            for row in one_hot_matrix
            if row.any()
        )
