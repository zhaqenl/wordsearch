"""Return either the coordinates of word matches or just the match quantity, inside the matrix."""

class WordsearchSolver(object):
    """Class."""

    def __init__(self, word, string_grid, separator='\n'):
        """Initialize matrix."""
        self.word = word
        self.word_len = len(self.word)

        if isinstance(string_grid, list):
            self.matrix = string_grid
        else:
            self.matrix = string_grid.split(separator)

        self.row_length = len(self.matrix)
        self.column_length = len(self.matrix[0])

    def coord_char(self, coord):
        """Return the element of matrix at specified coord."""
        row_index, column_index = coord

        return self.matrix[row_index][column_index]

    def convert_to_word(self, coord_matrix):
        """Return concatenated character strings."""
        return ''.join([self.coord_char(coord) for coord in coord_matrix])

    def find_base_match(self, char):
        """Return list of coordinates wherein char matched inside matrix."""
        base_matches = [(row_index, column_index) for row_index, row in enumerate(self.matrix)
                        for column_index, column in enumerate(row)
                        if char == column]

        return base_matches

    def matched_neighbors(self, coord, second_char):
        """Return list of coordinates wherein second_char matched inside matrix."""
        row_number, column_number = coord
        neighbors_coordinates = [(row, column) for row in range(row_number - 1, row_number + 2)
                                 for column in range(column_number - 1, column_number + 2)
                                 if self.row_length > row >= 0 and self.column_length > column >= 0
                                 and self.coord_char((row, column)) == second_char
                                 and not (row, column) == coord]

        return neighbors_coordinates

    def complete_line(self, base_coord, targ_coord):
        """Return list of tuple coordinates which correspond to a straight inside matrix."""
        if self.word_len == 2:
            return base_coord, targ_coord

        line = [base_coord, targ_coord]
        diff_1, diff_2 = targ_coord[0] - base_coord[0], targ_coord[1] - base_coord[1]

        for _ in range(self.word_len - 2):
            line += [(line[-1][0] + diff_1, line[-1][1] + diff_2)]

        if  0 <= line[-1][0] < self.row_length and 0 <= line[-1][1] < self.column_length:
            return line

        return []

    def complete_match(self, base_matches):
        """Return list of tuple coordinates whose character elements match those of word."""
        match_candidates = (self.complete_line(base, neighbor)
                            for base in base_matches
                            for neighbor in self.matched_neighbors(base, self.word[1]))

        return [match for match in match_candidates
                if self.convert_to_word(match) == self.word]

    def find_matches(self):
        """Return list of tuple coordinates whose character elements match those of word."""
        base_matches = self.find_base_match(self.word[0])

        if self.column_length < self.word_len > self.row_length or not base_matches:
            return []
        elif self.word_len == 1:
            return base_matches

        return self.complete_match(base_matches)

    def wordsearch(self):
        """Return length of the list return value of find_matches."""
        return len(self.find_matches())
