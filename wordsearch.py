"""
Top-level function takes 3 arguments, with the third one, being optional, that acts as the
separator indicator used for the second argument (default is ' ').

Examples:

wordsearch('cat', 'catt aata tatc')

wordsearch('cat', 'catt aata tatc', ' ')

wordsearch('cat', 'catt;aata;tatc', ';')

wordsearch('cat', 'catt
aata
tatc' '\n')
"""


def matrixify(string_grid, separator=' '):
    """Convert STRING_GRID into matrix-style list structure (given SEPARATOR-default is ' ')"""

    return [list(x) for x in string_grid.split(separator)]


def neighbors(coordinate, matrix):
    """Return neighbor coordinates of COORDINATE inside MATRIX, starting from the upper left
neighbor."""

    row_number = coordinate[0]
    column_number = coordinate[1]

    return [[i, j] for i in xrange(row_number-1, row_number+2) for j in xrange(column_number-1,
                                                                               column_number+2)
            if i >= 0 and i < len(matrix) and j >= 0 and j < len(matrix[0])
            and not [i, j] == coordinate]


def next_coord_in_line(starting_coordinate, target_coordinate):
    """Return the next coordinate based on the direction taken from STARTING_COORDINATE to
TARGET_COORDINATE."""

    difference = [target_coordinate[0] - starting_coordinate[0], target_coordinate[1] -
                  starting_coordinate[1]]
    first = difference[0]
    second = difference[1]

    return [target_coordinate[0] + first, target_coordinate[1] + second]


def find_base_match(element, matrix):
    """Return the coordinate of the match of the first letter of WORD_SPLIT in MATRIX if found, None
if first letter doesn't exist within matrix elements."""

    matrix_coordinates = [[i, j] for i in xrange(len(matrix)) for j in xrange(len(matrix[0]))]
    base_matches = []

    for coord in matrix_coordinates:
        if element == matrix[coord[0]][coord[1]]:
            base_matches.append(coord)
    return base_matches


def find_matches(word, string_grid, separator):
    """Create a matrix of the possible matches of WORD inside MATRIX (through creating coordinates
from WORD's length)."""

    def convert_to_word(matrix_coord, matrix):
        """Convert MATRIX_COORD of coordinates inside MATRIX into its word counterpart."""
        word = []
        for first, second in matrix_coord:
            word.append(matrix[first][second])
        return word

    matrix = matrixify(string_grid, separator)
    matches = []
    base_matches = find_base_match(word[0], matrix)

    if len(word) > len(matrix) and len(word) > len(matrix[0]) or not find_base_match(word[0],
                                                                                     matrix):
        print 'Word cannot be found.'
    else:
        for base in base_matches:
            for neighbor in neighbors(base, matrix):
                matches.append([base] + [neighbor] + [next_coord_in_line(base, neighbor)])
    return [match for match in matches if list(word) == convert_to_word(match, matrix)]


def wordsearch(word, string_grid, separator=' '):
    """Top-level function; Return coordinates of the matches of the elements of WORD against
STRING_GRID."""

    find_matches(word, string_grid, separator)
