import sys
from itertools import tee


VOWELS = "aeiouyåäö"
CONSONANTS = "bcdfghjklmnpqrstvwxz"
BACK_VOWELS = "aou"
FRONT_VOWELS = "äöy"
SWITCH_VOWELS = BACK_VOWELS + FRONT_VOWELS

CLOSING_DIPHTHONGS = [
    "ai", "au", "ei", "eu", "ey", "iu", "iy", "oi",
    "ou", "ui", "yi", "äi", "äy", "öi", "öy",
]
OPENING_DIPHTHONGS = ["ie", "uo", "yö"]
CLOSING_DIPHTHONGS_MAP = {d[0]: d[1] for d in CLOSING_DIPHTHONGS}
OPENING_DIPHTHONGS_MAP = {d[0]: d[1] for d in OPENING_DIPHTHONGS}
DIPHTHONGS = OPENING_DIPHTHONGS + CLOSING_DIPHTHONGS


def pairwise(iterable):
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)


def is_vowel(char):
    return char in VOWELS


def split(word):
    for i, (prev, next_) in enumerate(pairwise(word)):
        if is_vowel(prev) and prev != next_:
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


def fix_vowel_harmony(part_1, part_2):
    to_vowel = get_defining_vowel(part_1)
    return "".join(switch_vowel(char, to_vowel) for char in part_2)


def get_vowel_repeats(chars):
    for i, (prev, next_) in enumerate(pairwise(reversed(chars))):
        if prev != next_:
            return i + 1
    return len(chars)


def fix_vowel_counts(part_1, part_3):
    count_1 = get_vowel_repeats(part_3)
    count_3 = get_vowel_repeats(part_1)
    vowel_1 = part_1[-1]
    vowel_3 = part_3[-1]
    return (
        part_1[:-count_3] + count_1 * vowel_1,
        part_3[:-count_1] + count_3 * vowel_3,
    )


def fix_diphthong(part_1, part_2, old_part_1):
    try:
        new_char = part_2[0]
        new_chars = part_1[-1] + new_char
        old_chars = old_part_1[-1] + new_char
    except IndexError:
        return part_2

    if (
        new_chars in DIPHTHONGS
        or new_chars[0] == new_chars[1]
        or not all(map(is_vowel, new_chars))
    ):
        pass
    elif old_chars in OPENING_DIPHTHONGS:
        new_char = OPENING_DIPHTHONGS_MAP.get(*new_chars)
    elif old_chars in CLOSING_DIPHTHONGS:
        new_char = CLOSING_DIPHTHONGS_MAP.get(*new_chars)

    return new_char + part_2[1:]


def transform(word_1, word_2):
    """
    >>> transform('musta', 'naamio')
    ('nasta', 'muumio')
    >>> transform('vokaaleja', 'ylös')
    ('ykäälejä', 'volos')
    >>> transform('öööök', 'ää')
    ('ääääk', 'öö')
    >>> transform('vieno', 'huntti')
    ('huono', 'vintti')
    >>> transform('testi', 'kattavuus')
    ('kasti', 'tettavuus')
    >>> transform('sata', 'prosenttia')
    ('prota', 'sasenttia')
    """
    part_3, part_2 = split(word_1)
    part_1, part_4 = split(word_2)

    part_1, part_3 = fix_vowel_counts(part_1, part_3)

    part_2 = fix_diphthong(part_1, part_2, part_3)
    part_4 = fix_diphthong(part_3, part_4, part_1)

    part_2 = fix_vowel_harmony(part_1, part_2)
    part_4 = fix_vowel_harmony(part_3, part_4)

    return part_1 + part_2, part_3 + part_4
