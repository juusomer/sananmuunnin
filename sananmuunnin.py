import sys
from itertools import tee


VOWELS = "aeiouyåäö"
CONSONANTS = "bcdfghjklmnpqrstvwxz"
BACK_VOWELS = "aou"
FRONT_VOWELS = "äöy"
SWITCH_VOWELS = BACK_VOWELS + FRONT_VOWELS


def pairwise(iterable):
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)


def split(word):
    """
    >>> split('musta')
    ('mu', 'sta')
    >>> split('naamio')
    ('naa', 'mio')
    >>> split('proosa')
    ('proo', 'sa')
    """
    for i, (prev, next_) in enumerate(pairwise(word)):
        if prev in VOWELS and prev != next_:
            return word[:i + 1], word[i + 1:]
    return word, ""


def switch_to_back(char):
    try:
        return BACK_VOWELS[FRONT_VOWELS.index(char)]
    except ValueError:
        return char


def switch_to_front(char):
    try:
        return FRONT_VOWELS[BACK_VOWELS.index(char)]
    except ValueError:
        return char


def switch_vowel(from_char, to_char):
    if to_char in BACK_VOWELS:
        return switch_to_back(from_char)
    elif to_char in FRONT_VOWELS:
        return switch_to_front(from_char)
    return from_char


def get_defining_vowel(chars):
    return next(filter(lambda char: char in SWITCH_VOWELS, chars), "")


def fix_vowel_harmony(word):
    to_vowel = get_defining_vowel(word)
    return "".join(switch_vowel(char, to_vowel) for char in word)


def get_vowel_repeats(chars):
    for i, (prev, next_) in enumerate(pairwise(reversed(chars))):
        if prev != next_:
            return i + 1
    return len(chars)


def fix_vowel_counts(part_1, part_3):
    """
    >>> fix_vowel_counts('naa', 'mu')
    ('na', 'muu')
    """
    count_1 = get_vowel_repeats(part_3)
    count_3 = get_vowel_repeats(part_1)
    vowel_1 = part_1[-1]
    vowel_3 = part_3[-1]
    return (
        f"{part_1[:-count_3]}{count_1 * vowel_1}",
        f"{part_3[:-count_1]}{count_3 * vowel_3}",
    )


def process(word_1, word_2):
    """
    >>> process('musta', 'naamio')
    ('nasta', 'muumio')
    >>> process('vokaaleja', 'ylös')
    ('ykäälejä', 'volos')
    >>> process('testi', 'kattavuus')
    ('kasti', 'tettavuus')
    >>> process('sata', 'prosenttia')
    ('prota', 'sasenttia')
    """
    part_3, part_2 = split(word_1)
    part_1, part_4 = split(word_2)

    part_1, part_3 = fix_vowel_counts(part_1, part_3)

    word_1 = fix_vowel_harmony(part_1 + part_2)
    word_2 = fix_vowel_harmony(part_3 + part_4)

    return word_1, word_2
