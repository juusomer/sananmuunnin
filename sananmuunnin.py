import sys
from itertools import tee


VOWELS = "aeiouyåäö"
CONSONANTS = "bcdfghjklmnpqrstvwxz"
BACK_VOWELS = "aou"
FRONT_VOWELS = "äöy"
SWITCH_VOWELS = BACK_VOWELS + FRONT_VOWELS

CLOSING_DIPHTHONGS = [
    "ai",
    "au",
    "ei",
    "eu",
    "ey",
    "iu",
    "iy",
    "oi",
    "ou",
    "ui",
    "yi",
    "äi",
    "äy",
    "öi",
    "öy",
]
OPENING_DIPHTHONGS = ["ie", "uo", "yö"]
DIPHTHONGS = OPENING_DIPHTHONGS + CLOSING_DIPHTHONGS


def pairwise(iterable):
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)


def is_vowel(char):
    return char in VOWELS


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
        part_1[:-count_3] + count_1 * vowel_1,
        part_3[:-count_1] + count_3 * vowel_3,
    )


def fix_diphthongs_and_join(old_beginning, new_beginning, ending):
    """
    >>> fix_diphthongs_and_join('vi', 'hu', 'eno')
    'huono'
    """
    try:
        old_chars = old_beginning[-1] + ending[0]
        new_chars = new_beginning[-1] + ending[0]
    except IndexError:
        return new_beginning + ending

    char = new_chars[0]

    if new_chars in DIPHTHONGS or not all(map(is_vowel, new_chars)):
        pass
    elif old_chars in OPENING_DIPHTHONGS:
        new_chars = char + {d[0]: d[1] for d in OPENING_DIPHTHONGS}[char]
    elif old_chars in CLOSING_DIPHTHONGS:
        new_chars = char + {d[0]: d[1] for d in CLOSING_DIPHTHONGS}[char]

    return new_beginning[:-1] + new_chars + ending[1:]


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
    >>> process('öööök', 'ää')
    ('ääääk', 'öö')
    >>> process('vieno', 'huntti')
    ('huono', 'vintti')
    """
    part_3, part_2 = split(word_1)
    part_1, part_4 = split(word_2)

    part_1, part_3 = fix_vowel_counts(part_1, part_3)

    word_1 = fix_diphthongs_and_join(part_3, part_1, part_2)
    word_2 = fix_diphthongs_and_join(part_1, part_3, part_4)

    word_1 = fix_vowel_harmony(word_1)
    word_2 = fix_vowel_harmony(word_2)

    return word_1, word_2
