"""
Top-level function takes 3 arguments, with the third one, being optional, that acts as the
separator indicator used for the second argument (default is ' ').

Examples:

wordsearch('cat', 'catt aata tatc')

wordsearch('cat', 'catt aata tatc', ' ')

wordsearch('cat', 'catt;aata;tatc', ';')

If you want to use a newline character as the separator, use the quotaion marks for the docstring
(replace instances of (triple-quote) with that of the docstring's):

wordsearch('cat', (triple-quote)catt
aata
tatc(triple-quote), '\n')
"""


from itertools import izip


def matrixify(string_grid, separator='\n'):
    """
    Args:
        string_grid (str): A string containing non-whitespace and whitespace characters.
        separator (str): A whitespace character used in string_grid.

    Returns:
        list: Returns list of the strings of string_grid separated at its whitespace.
    """

    return string_grid.split(separator)


def coord_char(coord, matrix):
    """
    Args:
        coord (tuple): A coordinate in the matrix with (row, column) format.
        matrix (tuple): A tuple containing a tuple of characters.

    Returns:
        str: Returns the string located in the matrix coord.
    """

    row_index, column_index = coord

    return matrix[row_index][column_index]


def convert_to_word(coord_matrix, matrix):
    """
    Args:
        coord_matrix (tuple): A tuple of coordinate tuples.
        matrix (tuple): A tuple containing a tuple of characters.

    Returns:
        str: Returns string equivalent of coord_matrix.
    """

    return ''.join([coord_char(coord, matrix) for coord in coord_matrix])


def find_base_match(element, matrix, row_length, column_length):
    """
    Args:
        element (str): A single-length string
        matrix (tuple): A tuple containing a tuple of coordinates.

    Returns:
        list: Returns a coordinate list.
    """

    base_matches = [(row, column) for row in xrange(row_length) for column in xrange(column_length)
                    if coord_char((row, column), matrix) == element]

    return base_matches


def neighbors(coord, matrix, row_length, column_length):
    """
    Args:
        coord (tuple): A coordinate in the matrix with (row, column) format.
        matrix (tuple): A tuple containing a tuple of coordinates.

    Returns:
        itertools.izip: Returns an itertools.izip object containing pairs of the neighbors of coord,
with their corresponding character equivalents inside matrix.
    """

    row_number, column_number = coord
    neighbors_coordinates = [(row, column) for row in xrange(row_number-1, row_number+2)
                             for column in xrange(column_number-1, column_number+2)
                             if row_length > row >= 0 and column_length > column >= 0
                             and not (row, column) == coord]
    neighbors_char = [coord_char(neighbor, matrix) for neighbor in neighbors_coordinates]

    return izip(neighbors_coordinates, neighbors_char)


def nghbr_coord_extract(base_match_neighbors, char):
    """
    Args:
        base_match_coordinate (tuple): A coordinate tuple of the location of the base match.
        base_match_neighbors (list): A list containing a (coordinate, char) tuple of the
                                     neighbors of base_match_coordinate.
        char (string): A single-length string to find inside the values of base_match_neighbors.

    Returns:
        list: Returns a list containing the coordinates where char matched.
    """

    coord_list = [key for key, value in base_match_neighbors if value == char]

    return coord_list


def hybrid_line(base_coord, targ_coord, word_len, row_length, column_length):
    """
    Args:
        base_coord (tuple): A coordinate tuple of the starting position.
        targ_coord (tuple): A coordinate tuple of the target position.
        word_len (int): An integer which represents the length of the return tuple value.
        row_length (int): An integer which represents the height of the matrix.
        column_length (int): An integer which represents the horizontal length of the matrix.

    Returns:
        list: Returns a list, containing tuple coordinates, with word_len length and is a straight
              line when represented in a matrix; Retuns empty tuple if created tuple's last element
              is out of matrix bounds.
    """

    if word_len == 2:
        return base_coord, targ_coord

    max_row, max_column = row_length - 1, column_length - 1
    line = [base_coord, targ_coord]
    diff_1, diff_2 = targ_coord[0] - base_coord[0], targ_coord[1] - base_coord[1]

    for _ in xrange(word_len - 2):
        line += [(line[-1][0] + diff_1, line[-1][1] + diff_2)]

    if  0 <= line[-1][0] <= max_row and 0 <= line[-1][1] <= max_column:
        return line

    return []


def complex_match(word, matrix, base_matches, word_len, row_length, column_length):
    """
    Args:
        word (str): A string of the word to be found.
        matrix (list): A list containing strings separated at their whitespace characters.
        base_matches (list): A list containing tuple coordinates of the match of word[0] inside
                             matrix.
        word_len (int): Length of word.
        row_length (int): An integer which represents the height of the matrix.
        column_length (int): An integer which represents the horizontal length of the matrix.

    Returns:
        list: Returns a list of tuple coordinates.
    """

    match_generator = (hybrid_line(base, neighbor, word_len, row_length, column_length)
                       for base in base_matches
                       for neighbor in nghbr_coord_extract(neighbors(base, matrix, row_length,
                                                                     column_length), word[1]))

    return [match for match in match_generator if convert_to_word(match, matrix) == word]


def find_matches(word, string_grid, separator='\n'):
    """
    Args:
        word (str): A string of the word to be found.
        string_grid (str): A string containing non-whitespace and whitespace characters.
        separator (str): A string which is a whitespace character.

    Returns:
        list: Returns list matrix of the coordinate matches of word against string_grid.
    """

    word_len = len(word)
    if isinstance(string_grid, list):
        matrix = string_grid
    else:
        matrix = matrixify(string_grid, separator)
    row_length, column_length = len(matrix), len(matrix[0])
    base_matches = find_base_match(word[0], matrix, row_length, column_length)

    if word_len > row_length and word_len > column_length or not base_matches:
        return []
    elif word_len == 1:
        return base_matches

    return complex_match(word, matrix, base_matches, word_len, row_length, column_length)


def wordsearch(word, string_grid, separator='\n'):
    """
    Args:
        word (str): A string of the word to be found.
        string_grid (str): A string containing non-whitespace and whitespace characters.
        separator (str): A string which is a whitespace character.

    Returns:
        int: Returns the amount of matches from find_matches.
    """

    return len(find_matches(word, string_grid, separator))
