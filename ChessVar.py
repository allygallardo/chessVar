# Author: Allysa Gallardo
# GitHub username: allygallardo
# Date: 4/6/24
# Description:

class ChessVar:
    """The ChessVar object creates a Board. This will be the board that we will play a game of chess on. So the
    ChessVar class interacts with both the Board and Piece class. The ChessVar object also have a game_state data
    member, which starts off as “UNFINISHED” """

    def __init__(self):
        self._chess_board = Board()
        self._game_state = "UNFINISHED"
        self._current_player = "white"

    def get_game_state(self):
        """Takes in no parameters and returns “UNFINISHED”, “WHITE_WON”, or “BLACK_WON”"""
        pass

    def make_move(self):
        """Takes in 2 strings are parameters representing locations on the board a piece is coming from and going
        too. Return False if the square contains a piece that does not belong to the player, the move is not
        legal, or the game has already been won. Else, capture the piece at the moved_to square if applicable,
        move the current piece, update the game_state if necessary, update whose turn it is, and return true. """
        pass

    def enter_fairy_piece(self):
        """takes in the type of fairy piece and a location on the board and places that fairy piece on the board if
        possible, update whose turn it is, and return True. Else return false. """
        pass


class Piece:
    """A piece object represents a chess piece. They have a location (either a string representing a number on the
    board or None representing the piece being off the board), a color (either black or white), and a name
    (ex. “Knight”, “Pawn”)"""

    def __init__(self, location, color, name):
        self._location = location
        self._color = color
        self._name = name

    def get_location(self):
        """returns the location of the Piece on the board"""
        return self._location

    def get_color(self):
        """returns the color of the piece, either black or white"""
        return self._color

    def get_name(self):
        """returns the name of the piece, ex. 'Rook' """
        return self._name

    def is_move_possible(self, a_board, start, end):
        return None

    def make_move(self, start, end):
        """will be modified by each child of Piece, so that each piece has their unique move"""
        pass


class Pawn(Piece):
    "A type of chess piece"

    def __init__(self, location, color, name):
        super().__init((location, color, name))


    def make_move(self, start, end):
        """takes in 2 location parameters as strings and if the end location is valid,
        the Pawn will move according to its abilities in chess and return True. Else return False."""
        pass

class Rook(Piece):
    "A type of chess piece"

    def __init__(self, location, color, name):
        super().__init((location, color, name))

    def make_move(self, start, end):
        """takes in 2 location parameters as strings and if the end location is valid,
        the Rook will move according to its abilities in chess and return True. Else return False."""
        pass

class Knight(Piece):
    "A type of chess piece"

    def __init__(self, location, color, name):
        super().__init((location, color, name))

    def make_move(self, start, end):
        """takes in 2 location parameters as strings and if the end location is valid,
        the Knight will move according to its abilities in chess and return True. Else return False."""
        pass

class Bishop(Piece):
    "A type of chess piece"

    def __init__(self, location, color, name):
        super().__init((location, color, name))

    def make_move(self, start, end):
        """takes in 2 location parameters as strings and if the end location is valid,
        the Bishop will move according to its abilities in chess and return True. Else return False."""
        pass

class Queen(Piece):
    "A type of chess piece"

    def __init__(self, location, color, name):
        super().__init((location, color, name))

    def make_move(self, start, end):
        """takes in 2 location parameters as strings and if the end location is valid,
        the Queen will move according to its abilities in chess and return True. Else return False."""
        pass

class King(Piece):
    "A type of chess piece"

    def __init__(self, location, color, name):
        super().__init((location, color, name))

    def make_move(self, start, end):
        """takes in 2 location parameters as strings and if the end location is valid,
        the King will move according to its abilities in chess and return True. Else return False."""
        pass

class Fairy(Piece):
    "A type of chess piece"

    def __init__(self, location, color, name):
        super().__init((location, color, name))

    def make_move(self, start, end):
        """takes in 2 location parameters as strings and if the end location is valid,
        the Fairy will move according to its abilities in chess and return True. Else return False."""
        pass

class Board:
    """A board object is a list of 8 lists. Each list represents a row on the chessboard. For instance,
    the 0 index of the first list refers to spot “a8” on the chess board, the 7th index of the first list
    refers to spot “h8”, the 0 index of the 8th list refers to spot “a1” on the chess board, and the 7th index
    of the 8th list refers to spot “1h” on the chessboard. When a board object is created, it also creates Piece
    objects like “rook” and “pawn” and places them on their proper starting position on the board. So the board
    class interacts with the Piece class."""

    def __init__(self):
        self._board = []
        self.create_new_board()
        self.get_pieces_on_board()

    def create_new_board(self):
        """adds 8 lists to the chess_board list. Each element holds a dictionary. The key is a
        string representing the letter and number at that spot in the board. As of now the value the dictionary
        holds is None"""

        row_number = 8
        while row_number > 0:
            # create a row with the current row_number
            row_num_str = str(row_number)
            self._board.append(self.create_board_row(row_num_str))
            row_number -= 1

    def create_square(self, letter, row_number):
        """uses a letter and a row_number to return a dictionary with the key as a string of letter + row_number.
        As of now, the value is none."""

        square = {}
        square = {letter + row_number: None}
        return square

    def create_board_row(self, row_number):
        """fills a list with a size of 8 with dictionaries. each of the 8 dictionaries in a row has a different letter.
       Since we are creating a single row, the row_number will remain the same"""

        row = [self.create_square("a", row_number), self.create_square("b", row_number),
               self.create_square("c", row_number), self.create_square("d", row_number),
               self.create_square("e", row_number), self.create_square("f", row_number),
               self.create_square("g", row_number), self.create_square("h", row_number)]

        return row

    def get_board(self):
        """returns the board data member"""
        return self._board

    def get_pieces_on_board(self):
        """Uses the board we created and gets chess pieces to their starting positions on the board"""

        self.get_rooks_on_board()
        self.get_knights_on_board()
        self.get_bishops_on_board()
        self.get_kings_on_board()
        self.get_queens_on_board()
        self.get_pawns_on_board()


    def get_rooks_on_board(self):
        """creates rook pieces and places them for the start of the game """

        self._board[0][0]["a8"] = Piece("a8", "black", "rook")
        self._board[0][7]["h8"] = Piece("h8", "black", "rook")

        self._board[7][0]["a1"] = Piece("a1", "white", "rook")
        self._board[7][7]["ah"] = Piece("ah", "white", "rook")

    def get_knights_on_board(self):
        """creates knight pieces and places them for the start of the game """

        self._board[0][1]["b8"] = Piece("b8", "black", "knight")
        self._board[0][6]["g8"] = Piece("g8", "black", "knight")

        self._board[7][1]["b1"] = Piece("b1", "white", "knight")
        self._board[7][6]["g1"] = Piece("g1", "white", "knight")

    def get_bishops_on_board(self):
        """creates bishop pieces and places them for the start of the game """

        self._board[0][2]["c8"] = Piece("c8", "black", "bishop")
        self._board[0][5]["f8"] = Piece("f8", "black", "bishop")

        self._board[7][2]["c1"] = Piece("c1", "white", "bishop")
        self._board[7][5]["f1"] = Piece("f1", "white", "bishop")

    def get_kings_on_board(self):
        """creates king pieces and places them for the start of the game """

        self._board[0][3]["d8"] = Piece("d8", "black", "king")

        self._board[7][3]["d1"] = Piece("d1", "white", "king")

    def get_queens_on_board(self):
        """creates queen pieces and places them for the start of the game """

        self._board[0][4]["e8"] = Piece("e8", "black", "queen")

        self._board[7][4]["e1"] = Piece("e1", "white", "queen")

    def get_pawns_on_board(self):
        """creates pawn pieces and places them for the start of the game """

        self._board[1][0]["a7"] = Piece("a7", "black", "pawn")
        self._board[1][1]["b7"] = Piece("b7", "black", "pawn")
        self._board[1][2]["c7"] = Piece("c7", "black", "pawn")
        self._board[1][3]["d7"] = Piece("d7", "black", "pawn")
        self._board[1][4]["e7"] = Piece("d7", "black", "pawn")
        self._board[1][5]["f7"] = Piece("f7", "black", "pawn")
        self._board[1][6]["g7"] = Piece("g7", "black", "pawn")
        self._board[1][7]["h7"] = Piece("h7", "black", "pawn")

        self._board[6][0]["a2"] = Piece("a2", "white", "pawn")
        self._board[6][1]["b2"] = Piece("b2", "white", "pawn")
        self._board[6][2]["c2"] = Piece("c2", "white", "pawn")
        self._board[6][3]["d2"] = Piece("d2", "white", "pawn")
        self._board[6][4]["e2"] = Piece("d2", "white", "pawn")
        self._board[6][5]["f2"] = Piece("f2", "white", "pawn")
        self._board[6][6]["g2"] = Piece("g2", "white", "pawn")
        self._board[6][7]["h2"] = Piece("h2", "white", "pawn")


    def get_row_from_id(self, square_id):
        """uses the square id to return the row representational row on the board"""

        row_index = None

        if square_id[1] == "8":
            row_index = 0
        elif square_id[1] == "7":
            row_index = 1
        elif square_id[1] == "6":
            row_index = 2
        elif square_id[1] == "5":
            row_index = 3
        elif square_id[1] == "4":
            row_index = 4
        elif square_id[1] == "3":
            row_index = 5
        elif square_id[1] == "2":
            row_index = 6
        elif square_id[1] == "1":
            row_index = 7

        return row_index

    def get_col_from_id(self, square_id):
        """uses the square id to return the row representational column on the board"""
        column_index = None

        if square_id[0] == "a":
            column_index = 0
        elif square_id[0] == "b":
            column_index = 1
        elif square_id[0] == "c":
            column_index = 2
        elif square_id[0] == "d":
            column_index = 3
        elif square_id[0] == "e":
            column_index = 4
        elif square_id[0] == "f":
            column_index = 5
        elif square_id[0] == "g":
            column_index = 6
        elif square_id[0] == "h":
            column_index = 7

        return column_index



    def get_Piece_from_squareID(self, square_id):
        """return piece from the chessboard at square id ex. "a8". If no piece there return None"""
        result = None

        row_index = self.get_row_from_id(square_id)
        chess_board_row = self._board[row_index]

        for square_index in range(8): # 8 columns per row aka 8 elements per list so indices = 0-7
            potential_square = chess_board_row[square_index]
            if square_id in potential_square:
                result = potential_square[square_id]
                break

        return result




    ## get square id from


    #def display_board(self):
        #  print 8 lists to represent the rows (8 print statements)
        # if get_Piece_from_squareID("a" + row_index ).get_name == "Rook"
        #       print("R")
        # like this

a_board = Board()

# lets say we are moving from h8
start_row = a_board.get_row_from_id("h8")
start_col = a_board.get_col_from_id("h8")
print(a_board.get_board()[start_row][start_col])
print(a_board.get_Piece_from_squareID("h8"))


