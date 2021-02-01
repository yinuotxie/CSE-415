import math
import re
import string


def is_multiple_of_9(n):
    """Return True if n is a multiple of 9; False otherwise."""
    if n % 9 == 0:
        return True
    else:
        return False


def next_prime(m):
    """Return the first prime number p that is greater than m.
    You might wish to define a helper function for this.
    You may assume m is a positive integer."""

    p = m + 1

    while not isPrime(p):
        p = p + 1

    return p


def isPrime(n):
    """Return true if the input number if prime,false otherwise"""
    if n <= 1:
        return False

    for i in range(2, n):
        if n % i == 0:
            return False

    return True


def quadratic_roots(a, b, c):
    """Return the roots of a quadratic equation (real cases only).
    Return results in tuple-of-floats form, e.g., (-7.0, 3.0)
    Return "complex" if real roots do not exist."""
    n = b ** 2 - 4 * a * c

    if n < 0:
        return "complex"

    x1 = (-b - math.sqrt(n)) / (2 * a)
    x2 = (-b + math.sqrt(n)) / (2 * a)

    return (x1, x2)


def perfect_shuffle(even_list):
    """Assume even_list is a list of an even number of elements.
    Return a new list that is the perfect-shuffle of the input.
    For example, [0, 1, 2, 3, 4, 5, 6, 7] => [0, 4, 1, 5, 2, 6, 3, 7]"""
    new_list = []
    half = int(len(even_list) / 2)
    for i in range(0, half):
        new_list.append(even_list[i])
        new_list.append(even_list[i + half])
    return new_list


def triples_list(input_list):
    """Assume a list of numbers is input. Using a list comprehension,
    return a new list in which each input element has been multiplied
    by 3."""
    return [3 * x for x in input_list]


def double_consonants(text):
    """Return a new version of text, with all the consonants doubled.
    For example:  "The *BIG BAD* wolf!" => "TThhe *BBIGG BBADD* wwollff!"
    For this exercise assume the consonants are all letters OTHER
    THAN A,E,I,O, and U (and a,e,i,o, and u).
    Maintain the case of the characters."""

    result = ''
    for char in text:
        if isConsonate(char) and char != ' ' and \
           (char not in string.punctuation):
            result = result + char + char
        else:
            result += char

    return result


def isConsonate(char):
    """Check whether the input character is a consonate.
    Return true if it is, false otherwise"""
    vows = ['a', 'e', 'i', 'o', 'u', 'A', 'E', 'I', 'O', 'U']
    return (char not in vows)


def count_words(text):
    """Return a dictionary having the words in the text as keys,
    and the numbers of occurrences of the words as values.
    Assume a word is a substring of letters and digits and the characters
    '-', '+', '*', '/', '@', '#', '%', and "'" separated by whitespace,
    newlines, and/or punctuation (characters like . , ; ! ? & ( ) [ ]  ).
    Convert all the letters to lower-case before the counting."""

    map = {}
    char_list = re.split(r'\s+|[~^$&{}`"><=\|_\\.,:;!?&()[\]]', text)

    for char in char_list:
        char = char.lower()
        if char != '':
            if char in map.keys():
                map[char] = map[char] + 1
            else:
                map[char] = 1

    return map


def make_cubic_evaluator(a, b, c, d):
    """When called with 4 numbers, returns a function of one variable (x)
    that evaluates the cubic polynomial
    a x^3 + b x^2 + c x + d.
    For this exercise Your function definition for make_cubic_evaluator
    should contain a lambda expression."""
    return lambda x: a * pow(x, 3) + b * pow(x, 2) + c * x + d


class Polygon:
    """Polygon class."""
    """It should have a number of sides.
    It should have a list of length of sides, except its default value is None
    It should have a list of angles (in degrees), except its default value is None.
    Write methods ..."""
    def __init__(self, n_sides, lengths=None, angles=None):
        self.n_sides = n_sides
        self.lengths = lengths
        self.angles = angles

    def is_rectangle(self):
        """ returns True if the polygon is a rectangle,
        False if it is definitely not a rectangle, and None
        if the angle list is unknown (None)."""
        if self.n_sides != 4:
            return False
        
        if self._check_Length() is False:
            return False

        return self._check_Angle(90)

    def is_rhombus(self):
        if self.n_sides != 4:
            return False

        return self._check_Length()

    def is_square(self):
        if self.is_rectangle() is False:
            return False

        return self._check_Length() and self._check_Angle(90)

    def is_regular_hexagon(self):
        if self.n_sides != 6:
            return False

        if self._check_Length() is False or \
           self._check_Angle(120) is False:
            return False

        return self._check_Length() and self._check_Angle(120)

    def is_isosceles_triangle(self):
        if self.n_sides != 3:
            return False

        if self.lengths is None and self.angles is None:
            return None

        if self.lengths is not None:
            for length in self.lengths:
                if self.lengths.count(length) >= 2:
                    return True
        # Angle list exists
        else:
            for angle in self.angles:
                if self.angles.count(angle) >= 2:
                    return True

        return False

    def is_equilateral_triangle(self):
        if self.n_sides != 3:
            return False

        if self._check_Length() is False:
            return False

        return self._check_Length() or self._check_Angle(60)

    def is_scalene_triangle(self):
        if self.n_sides != 3:
            return False

        if self.is_isosceles_triangle() is not None:
            return not self.is_isosceles_triangle()
        return None

    def _check_Angle(self, angle_target):
        if self.angles is None:
            return None

        for angle in self.angles:
            if angle != angle_target:
                return False
        return True

    def _check_Length(self):
        if self.lengths is None:
            return None

        length = self.lengths[0]
        return self.lengths.count(length) == self.n_sides
