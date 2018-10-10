"""This module contains the core functions needed by wordsearch.py.

Top-level function takes 3 arguments, with the third one, being optional, that acts as the
separator indicator used for the second argument (default is ' ').

Examples:

wordsearch('cat', 'catt aata tatc')

wordsearch('cat', 'catt aata tatc', ' ')

wordsearch('cat', 'catt;aata;tatc', ';')

If you want to use a newline character as the separator, use triple double quotes in the second
argument with the corresponding newline character as the third argument (minus the backslash escape
characters):

wordsearch('cat', \"\"\"catt
aata
tatc\"\"\", '\\n')
"""


def matrixify(string_grid, separator='\n'):
    """Return a matrix out of string_grid.

    Args:
        string_grid (str): A string containing non-whitespace and whitespace characters.
        separator (str): A whitespace character used in string_grid.

    Returns:
        list: Returns list of the strings of string_grid separated at its whitespace.
    """
    return string_grid.split(separator)


def coord_char(coord, matrix):
    """Return the element of matrix at specified coord.

    Args:
        coord (tuple): A coordinate in the matrix with (row, column) format.
        matrix (list): A list containing lines of string.

    Returns:
        str: Returns the string located in the matrix coord.
    """
    row_index, column_index = coord

    return matrix[row_index][column_index]


def convert_to_word(coord_matrix, matrix):
    """Return concatenated character strings.

    Args:
        coord_matrix (list): A list of coordinate tuples.
        matrix (list): A list containing lines of string.

    Returns:
        str: Returns string equivalent of coord_matrix.
    """
    return ''.join([coord_char(coord, matrix) for coord in coord_matrix])


def find_base_match(char, matrix):
    """Return list of coordinates wherein char matched inside matrix.

    Args:
        char (str): A single-length string
        matrix (list): A list containing lines of string.
        row_length (int): An integer which represents the height of the matrix.
        column_length (int): An integer which represents the horizontal length of the matrix.

    Returns:
        list: Returns a coordinate list.
    """
    base_matches = [(row_index, column_index) for row_index, row in enumerate(matrix)
                    for column_index, column in enumerate(row)
                    if char == column]

    return base_matches


def matched_neighbors(coord, second_char, matrix, row_length, column_length):
    """Return list of coordinates wherein second_char matched inside matrix.

    Args:
        coord (tuple): A coordinate in the matrix with (row, column) format.
        second_char (str): The second character of the word.
        matrix (list): A list containing lines of string.
        row_length (int): An integer which represents the height of the matrix.
        column_length (int): An integer which represents the horizontal length of the matrix.

    Returns:
        list: Returns a list containing the coordinates where second_char matched inside matrix.
    """
    row_number, column_number = coord
    neighbors_coordinates = [(row, column) for row in xrange(row_number - 1, row_number + 2)
                             for column in xrange(column_number - 1, column_number + 2)
                             if row_length > row >= 0 and column_length > column >= 0
                             and coord_char((row, column), matrix) == second_char
                             and not (row, column) == coord]

    return neighbors_coordinates


def complete_line(base_coord, targ_coord, word_len, row_length, column_length):
    """Return list of tuple coordinates which correspond to a straight line inside the matrix.

    Args:
        base_coord (tuple): A coordinate tuple of the starting position.
        targ_coord (tuple): A coordinate tuple of the target position.
        word_len (int): An integer which represents the length of the return tuple value.
        row_length (int): An integer which represents the height of the matrix.
        column_length (int): An integer which represents the horizontal length of the matrix.

    Returns:
        list: Returns a list, containing tuple coordinates, with word_len length and is a straight
              line when represented in a matrix; Retuns empty tuple if tuple's last coordinate is
              out of matrix bounds.
    """
    if word_len == 2:
        return base_coord, targ_coord

    line = [base_coord, targ_coord]
    diff_1, diff_2 = targ_coord[0] - base_coord[0], targ_coord[1] - base_coord[1]

    for _ in xrange(word_len - 2):
        line += [(line[-1][0] + diff_1, line[-1][1] + diff_2)]

    if  0 <= line[-1][0] < row_length and 0 <= line[-1][1] < column_length:
        return line

    return []


def complete_match(word, matrix, base_matches, word_len, row_length, column_length):
    """Return list of tuple coordinates whose character elements match those of word.

    Args:
        word (str): A string of the word to be found.
        matrix (list): A list containing lines of string.
        base_matches (list): A list containing tuple coordinates of the match of word[0] inside
                             matrix.
        word_len (int): Length of word.
        row_length (int): An integer which represents the height of the matrix.
        column_length (int): An integer which represents the horizontal length of the matrix.

    Returns:
        list: Returns a list of tuple coordinates.
    """
    match_candidates = (complete_line(base, neighbor, word_len, row_length, column_length)
                        for base in base_matches
                        for neighbor in matched_neighbors(base, word[1], matrix, row_length,
                                                          column_length))

    return [match for match in match_candidates if convert_to_word(match, matrix) == word]


def find_matches(word, string_grid, separator='\n'):
    """Return list of tuple coordinates whose character elements match those of word.

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
    base_matches = find_base_match(word[0], matrix)

    if column_length < word_len > row_length or not base_matches:
        return []
    elif word_len == 1:
        return base_matches

    return complete_match(word, matrix, base_matches, word_len, row_length, column_length)


def wordsearch(word, string_grid, separator='\n'):
    """Return length of the list return value of find_matches.

    Args:
        word (str): A string of the word to be found.
        string_grid (str): A string containing non-whitespace and whitespace characters.
        separator (str): A string which is a whitespace character.

    Returns:
        int: Returns the amount of matches from find_matches.
    """
    return len(find_matches(word, string_grid, separator))
