"""
Top-level function takes 3 arguments, with the third one, being optional, that acts as the
separator indicator used for the second argument (default is ' ').

Examples:

wordsearch('cat', 'catt aata tatc')

wordsearch('cat', 'catt aata tatc', ' ')

wordsearch('cat', 'catt;aata;tatc', ';')

If you want to use a newline character as the separator, use the !!!

wordsearch('cat', 'catt
aata
tatc' '\n')
"""


def matrixify(string_grid, separator='\n'):
    """
    Args:
        string_grid (str): A string containing none-whitespace and whitespace characters.
        separator (str): The whitespace character used in string_grid.

    Returns:
        tuple: Returns a tuple mapping (matrix-style) of string_grid.
    """

    return tuple(string_grid.split(separator))


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
        tuple: Returns tuple of strings.
    """

    return tuple([coord_char(coord, matrix) for coord in coord_matrix])


def find_base_match(element, matrix):
    """
    Args:
        element (str): A single length string
        matrix (tuple): A tuple containing a tuple of coordinates.

    Returns:
        tuple: Returns a coordinate tuple.
    """

    matrix_coordinates = [(row, column) for row in xrange(len(matrix)) for column
                          in xrange(len(matrix[0]))]
    base_matches = [coordinate for coordinate in matrix_coordinates
                    if element == coord_char(coordinate, matrix)]

    return tuple(base_matches)


def neighbors(coord, matrix):
    """
    Args:
        coord (tuple): A coordinate in the matrix with (row, column) format.
        matrix (tuple): A tuple containing a tuple of coordinates.

    Returns:
        dict: Returns a dict containing the a {coordinate: char} pair of the neighbors of coord
              inside matrix.
    """

    row_number, column_number = coord
    neighbors_coordinates = [(row, column) for row in xrange(row_number-1, row_number+2)
                             for column in xrange(column_number-1, column_number+2)
                             if row >= 0 and row < len(matrix) and column >= 0
                             and column < len(matrix[0]) and not (row, column) == coord]
    neighbors_char = [coord_char(neighbor, matrix) for neighbor in neighbors_coordinates]

    return dict(zip(neighbors_coordinates, neighbors_char))


def nghbr_coord_extract(base_match_neighbors, char):
    """
    Args:
        base_match_coordinate (tuple): A coordinate tuple of the location of the base match.
        base_match_neighbors (dict): A dictionary containing a {coordinate: char} pair of the
                                     neighbors of base_match_coordinate.
        char (string): A single-length string to find inside the values of base_match_neighbors
                       dict.

    Returns:
        tuple: Returns a tuple containing the coordinates where char matched.
    """

    coord_list = [key for key, value in base_match_neighbors.viewitems() if value == char]

    return tuple(coord_list)


def hybrid_line(base_coord, targ_coord, word_len, matrix):
    """
    Args:
        base_coord (tuple): A coordinate tuple of the starting position.
        targ_coord (tuple): A coordinate tuple of the target position.
        word_len (int): An int which represents the length of the return tuple value.
        matrix (tuple): A tuple containing tuples containing single-length strings.

    Returns:
        tuple: Returns a tuple, containing tuple coordinates, with word_len length and is a straight
               line when represented in a matrix; Retuns empty tuple if created tuple's last element
               is out of matrix bounds.
    """

    if word_len == 2:
        return base_coord, targ_coord

    max_row, max_column = len(matrix) - 1, len(matrix[0]) - 1
    line = [base_coord, targ_coord]
    difference_1, difference_2 = targ_coord[0] - base_coord[0], targ_coord[1] - base_coord[1]

    while len(line) != word_len:
        line.append((line[-1][0] + difference_1, line[-1][1] + difference_2))

    if  0 <= line[-1][0] <= max_row and 0 <= line[-1][1] <= max_column:
        return tuple(line)

    return tuple()


def complex_match(word, matrix, base_matches):
    """
    Args:
        word (str): A string of the word to be found.
        matrix (tuple): A tuple containing tuples containing single-Length strings.
        base_matches (tuple): A tuple containing tuple coordinates of the match of word[0] inside
                              matrix.

    Returns:
        list: Returns a list of tuple coordinates.
    """

    match_generator = (hybrid_line(base, neighbor, len(word), matrix)
                       for base in base_matches
                       for neighbor in nghbr_coord_extract(neighbors(base, matrix), word[1]))

    return [match for match in match_generator if convert_to_word(match, matrix) == word]


def find_matches(word, string_grid, separator='\n'):
    """
    Args:
        word (str): A string of the word to be found.
        string_grid (str): A string containing none-whitespace and whitespace characters.
        separator (str): A string which is a whitespace character.

    Returns:
        tuple: Returns tuple matrix of the coordinates matches of word against string_grid.
    """

    word = tuple(word)
    word_len = len(word)
    matrix = matrixify(string_grid, separator)
    base_matches = find_base_match(word[0], matrix)

    if word_len > len(matrix) and word_len > len(matrix[0]) or not base_matches:
        return tuple()
    elif word_len == 1:
        return base_matches
    return complex_match(word, matrix, base_matches)


def wordsearch(word, string_grid, separator='\n'):
    """Top-level function; Return coordinates of WORD matches against STRING_GRID."""

    return len(find_matches(word, string_grid, separator))
