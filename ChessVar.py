# Author: Allysa Gallardo
# GitHub username: allygallardo
# Date: 3/17/24
# Description: This file allows the user to virtually play chess. This file includes the ChessVar class, the Piece
# class and its 7 subclasses including the Fairy class representing the fairy pieces hunter and falcon (which are pieces
# included in a variation of standard chess), and the board class. The board class is responsible for representing
# the chess board virtually and setting the pieces on the board at the start of a game. Each piece subclass in the
# piece class is responsible for upholding the rules in how they move in a game of chess. The ChessVar class contains
# a board object and is responsible for handling a single game of chess, switching between players, and calling the
# moves for a piece to move.

class ChessVar:
    """The ChessVar object creates a Board. This will be the board that we will play a game of chess on. So the
    ChessVar class interacts with both the Board and Piece class. The ChessVar object also have a game_state data
    member, which starts off as “UNFINISHED” """

    def __init__(self):
        self._chess_board = Board()
        self._game_state = "UNFINISHED"
        self._current_player_turn = "white"

    def get_chess_board(self):
        """returns the board that this current game of chess is using"""
        return self._chess_board

    def get_game_state(self):
        """Takes in no parameters and returns “UNFINISHED”, “WHITE_WON”, or “BLACK_WON”"""

        #if white have no king, black wins
        if self._chess_board.has_no_king_on_board("white"):
            return "BLACK_WON"
        # if black have no king, white wins
        elif self._chess_board.has_no_king_on_board("black"):
            return "WHITE_WON"
        else:
            return "UNFINISHED"

    def get_current_player_turn(self):
        """returns the current player"""
        return self._current_player_turn

    def switch_player_turn(self):
        """switches to the other player"""
        if self._current_player_turn == "white":
            self._current_player_turn = "black"
        elif self._current_player_turn == "black":
            self._current_player_turn = "white"

    def make_move(self, start_id, end_id):
        """Takes in 2 strings are parameters representing locations on the board a piece is coming from and going
        too. Return False if the square contains a piece that does not belong to the player, the move is not
        legal, or the game has already been won. Else, capture the piece at the moved_to square if applicable,
        move the current piece, update the game_state if necessary, update whose turn it is, and return true. """

        result = False

        a_board = self._chess_board

        # if the start_id or end_id are not even square ids that exist on the board, return false, no need to continue
        if a_board.is_id_within_board_bounds(start_id) is False or a_board.is_id_within_board_bounds(end_id) is False:
            return False


        start_id_piece = a_board.get_Piece_from_squareID(start_id)
        if start_id_piece is not None:
            color_of_start_id_piece = start_id_piece.get_color()

        end_id_piece = a_board.get_Piece_from_squareID(end_id)
        if end_id_piece is not None:
            color_of_end_id_piece = end_id_piece.get_color()

        current_color_turn = self.get_current_player_turn()
        if start_id_piece is None:
            result = False

        # if the start_id contains a color that doesn't match the color of the player whose turn it is
            # return false (can't move a piece that's not urs)
        elif color_of_start_id_piece != current_color_turn:
            result = False
        # if the end_id contains a color that is the same as the color of the player whose turn it is
            # return false (not allowed to capture ur own piece)
        elif end_id_piece is not None and color_of_end_id_piece == current_color_turn:
            result = False
        # if the move is not legal (call the piece's move function if it returns false..)
            #return false
        elif start_id_piece.make_move(start_id, end_id, a_board) is False:
            result = False
        # if the game has already been won
            # return false
        elif self.get_game_state() != "UNFINISHED":
            result = False
        else:
            # move the current piece from start_id to the end_id
            # update the game start if necessary (get_game_state)
            # this function also updates the tracker if a piece was captured
            a_board.set_piece_at_square(start_id, end_id)
             # update whose turn it is
            self.switch_player_turn()
            result = True

        return result

    def is_mismatched_for_fairy_piece(self, color, letter):
        """black gets their hunter/falcon using lower case letter h and f. white gets their hunter/falcon using
        upper case letters H and F. If black uses upper case or white uses lower case letters, then
         they are trying to get the wrong colored pieces, so return true because they are mismatched"""
        result = False
        if color == "white":
            if letter == "f" or letter == "h":
                result = True
        if color == "black":
            if letter == "F" or letter == "H":
                result = True

        return result

    def enter_fairy_piece(self, letter, start_id):
        """takes in the type of fairy piece and a location on the board and places that fairy piece on the board if
        possible, update whose turn it is, and return True. Else return false. """
        #white falcon 'F', white hunter 'H', black falcon 'f', black hunter 'h'

        a_board = self._chess_board
        result = False

        # if the start_id is not even square ids that exist on the board, return false, no need to continue
        if a_board.is_id_within_board_bounds(start_id) is False:
            return False

        current_color_turn = self.get_current_player_turn()
        row_of_start_id = a_board.get_row_from_id(start_id)
        col_of_start_id = a_board.get_col_from_id(start_id)
        start_id_piece = a_board.get_Piece_from_squareID(start_id)
        name_of_piece = ""

        if letter == "H" or letter == "h":
            name_of_piece = "hunter"
        if letter == "F" or letter == "f":
            name_of_piece = "falcon"
        else:
            result = False

        # if the game is finished, return false
        if self.get_game_state() != "UNFINISHED":
            result = False
        # if we are trying to create a fairy piece that doesn't align with the current player's color, return false
        elif self.is_mismatched_for_fairy_piece(current_color_turn, letter):
            result = False
        # if the start_id is not at the home ranks, return false:
             #   if current color turn = white, row of start_id should be 1 [7]
            #  if current color turn = black, row of start_id should be 8 [0]
        elif current_color_turn == "black" and row_of_start_id != 0:
            result = False
        elif current_color_turn == "white" and row_of_start_id != 7:
            result = False
        #if start_id is not empty, return false
        elif start_id_piece is not None:
            result = False
        else:
            # add fairy piece will return false if we are trying to add a fairy that is already there
            # if we are trying to enter our first piece, and qualified to do so, and havent added that piece
            # already, then add that piece to the tracker and the board
            if a_board.has_no_fairy_on_board(current_color_turn):
                if a_board.get_current_num_major_pieces(current_color_turn) <= 6:
                    if a_board.add_fairy_piece_tracker(current_color_turn, letter):
                        # add actual piece to the board
                        virtual_board = a_board.get_board()
                        virtual_board[row_of_start_id][col_of_start_id] = Fairy(current_color_turn, name_of_piece)
                        result = True
            else: # we have at least 1 fairy on the board
                if a_board.get_current_num_major_pieces(current_color_turn) <= 5:
                    if a_board.add_fairy_piece_tracker(current_color_turn, letter):
                        # add the actual piece to the board
                        virtual_board = a_board.get_board()
                        virtual_board[row_of_start_id][col_of_start_id] = Fairy(current_color_turn, name_of_piece)
                        result = True

        # update whose turn it is after a successful entering of a fairy piece
        if result is True:
            self.switch_player_turn()

        return result


class Piece:
    """A piece object represents a chess piece. They have a location (either a string representing a number on the
    board or None representing the piece being off the board), a color (either black or white), and a name
    (ex. “Knight”, “Pawn”)"""

    def __init__(self, color, name):
        self._color = color
        self._name = name

    def get_color(self):
        """returns the color of the piece, either black or white"""
        return self._color

    def get_name(self):
        """returns the name of the piece, ex. 'Rook' """
        return self._name

    def make_move(self, start, end, board):
        """will be modified by each child of Piece, so that each piece has their unique move"""
        pass


class Pawn(Piece):
    """A type of chess piece"""

    def __init__(self, color, name):
        super().__init__(color, name)
        self._is_first_move = True

    def set_is_first_move_to_false(self):
        self._is_first_move = False

    def make_move(self, start_id, end_id, a_board):
        """takes in 2 location parameters as strings and if the end location is valid,
        the Pawn will move according to its abilities in chess and return True. Else return False."""

        result = False
        piece_at_end_id = a_board.get_Piece_from_squareID(end_id)
        color_of_piece = self.get_color()

        if piece_at_end_id is not None:
            if self.pawn_capture_valid(color_of_piece, start_id, end_id, a_board):
                result = True
        else: #else there is not a piece at the end_id, so we must be trying to move
            if self._is_first_move:
                #if we can move double or single correctly, then set to true and set is_first_move to false
                if self.pawn_double_move_valid(color_of_piece, start_id, end_id, a_board) or self.pawn_move_valid(color_of_piece, start_id, end_id, a_board):
                    result = True
                    self.set_is_first_move_to_false()
            else:
                #it's not the first move for this pawn
                if self.pawn_move_valid(color_of_piece, start_id, end_id, a_board):
                    result = True
        return result


    def pawn_double_move_valid(self, color_of_piece, start_id, end_id, a_board):
        """the pawn double move is valid if the end id is 2 rows down from black pieces and 2 rows up
        from white pieces. Else return false """

        result = False
        row_col_difference = a_board.find_row_and_col_difference(start_id, end_id)
        row_difference = row_col_difference[0]
        col_difference = row_col_difference[1]

        if color_of_piece == "black":
            if row_difference == 2 and col_difference == 0:
                result = True

        if color_of_piece == "white":
            if row_difference == -2 and col_difference == 0:
                result = True

        return result

    def pawn_move_valid(self, color_of_piece, start_id, end_id, a_board):
        """the pawn regular (single) move is valid if the end id is 1 row down from black pieces and 1 row up
        from white pieces. Else return false """

        result = False
        row_col_difference = a_board.find_row_and_col_difference(start_id, end_id)
        row_difference = row_col_difference[0]
        col_difference = row_col_difference[1]

        if color_of_piece == "black":
            if row_difference == 1 and col_difference == 0:
                result = True

        if color_of_piece == "white":
            if row_difference == -1 and col_difference == 0:
                result = True

        return result


    def pawn_capture_valid(self, color_of_piece, start_id, end_id, a_board):
        """if the pawn is black and trying to capture a piece, then it can move diagonally down left
        or diagonally down right. if the pawn is white and trying to capture a piece, then it can move
        diagonally up left or up right. in both cases return true. else the end_id isn't valid so return false."""

        result = False
        row_col_difference = a_board.find_row_and_col_difference(start_id, end_id)
        row_difference = row_col_difference[0]
        col_difference = row_col_difference[1]

        if color_of_piece == "black":
            if row_difference == 1 and col_difference == -1:
                result = True
            elif row_difference == 1 and col_difference == 1:
                result = True

        if color_of_piece == "white":
            if row_difference == -1 and col_difference == -1:
                result = True
            elif row_difference == -1 and col_difference == 1:
                result = True

        return result


class Rook(Piece):
    "A type of chess piece"

    def __init__(self, color, name):
        super().__init__(color, name)

    def make_move(self, start_id, end_id, a_board):
        """takes in 2 location parameters as strings and if the end location is valid,
        the Rook will move according to its abilities in chess and return True. Rooks can move
        left, right, up, or down as long as there are no pieces in its path (not including if there is a
        piece at the end square). Else return False."""

        result = False
        if a_board.is_up_down_left_right_valid(start_id, end_id):
            result = True

        return result

class Knight(Piece):
    "A type of chess piece"

    def __init__(self ,color, name):
        super().__init__(color, name)

    def make_move(self, start_id, end_id, a_board):
        """takes in 2 location parameters as strings and if the end location is valid,
        the Knight will move according to its abilities in chess and return True. Else return False."""

        result = False
        row_col_difference = a_board.find_row_and_col_difference(start_id, end_id)

        if row_col_difference == [-2, 1]:
            result = True
        elif row_col_difference == [-2, -1]:
            result = True
        elif row_col_difference == [2, 1]:
            result = True
        elif row_col_difference == [2, -1]:
            result = True
        elif row_col_difference == [-1, 2]:
            result = True
        elif row_col_difference == [1, 2]:
            result = True
        elif row_col_difference == [-1, -2]:
            result = True
        elif row_col_difference == [1, -2]:
            result = True

        return result



class Bishop(Piece):
    "A type of chess piece"

    def __init__(self, color, name):
        super().__init__(color, name)

    def make_move(self, start_id, end_id, a_board):
        """takes in 2 location parameters as strings and if the end location is valid,
        the bishop will move according to its abilities in chess and return True. bishops can move diagonally
        up left, up right, down left, or down right as long as there are no pieces in its path
         (not including if there is a piece at the end square). Else return False."""

        result = False
        if a_board.is_diag_up_down_left_right_valid(start_id, end_id):
            result = True

        return result

class Queen(Piece):
    "A type of chess piece."

    def __init__(self, color, name):
        super().__init__(color, name)

    def make_move(self, start_id, end_id, a_board):
        """takes in 2 location parameters as strings and if the end location is valid,
        the Queen will move according to its abilities in chess and return True. Else return False."""

        result = False
        #if the queen can move like a rook
        if a_board.is_up_down_left_right_valid(start_id, end_id):
            result = True
        #if the queen can move like a bishop
        elif a_board.is_diag_up_down_left_right_valid(start_id, end_id):
            result = True

        return result

class King(Piece):
    "A type of chess piece"

    def __init__(self, color, name):
        super().__init__(color, name)

    # idk
    def make_move(self, start_id, end_id, a_board):
        """takes in 2 location parameters as strings and if the end location is valid,
        the King will move according to its abilities in chess and return True. Else return False."""

        result = False
        row_col_difference = a_board.find_row_and_col_difference(start_id, end_id)

        if row_col_difference == [-1, 0]:
            result = True
        elif row_col_difference == [-1, -1]:
            result = True
        elif row_col_difference == [0, -1]:
            result = True
        elif row_col_difference == [1, -1]:
            result = True
        elif row_col_difference == [1, 0]:
            result = True
        elif row_col_difference == [1, 1]:
            result = True
        elif row_col_difference == [0, 1]:
            result = True
        elif row_col_difference == [-1, 1]:
            result = True

        return result

class Fairy(Piece):
    "A type of chess piece"

    def __init__(self, color, name):
        super().__init__(color, name)

    def make_move(self, start_id, end_id, a_board):
        """takes in 2 location parameters as strings and if the end location is valid,
        the Fairy will move according to its abilities in chess and return True. Else return False."""

        result = False
        fairy_color = self.get_color()
        fairy_name = self.get_name()

        if fairy_color == "black":
            if fairy_name == "hunter":
                if self.black_hunter_move_valid(start_id, end_id, a_board):
                    result = True
            elif fairy_name == "falcon":
                if self.black_falcon_move_valid(start_id, end_id, a_board):
                    result = True
        elif fairy_color == "white":
            if fairy_name == "hunter":
                if self.white_hunter_move_valid(start_id, end_id, a_board):
                    result = True
            elif fairy_name == "falcon":
                if self.white_falcon_move_valid(start_id, end_id, a_board):
                    result = True

        return result

    def black_hunter_move_valid(self, start_id, end_id, a_board):
        """takes in a start_id and end_id as strings and a board object. returns true if the black hunter
        moves according to its rules. else return false"""

        result = False
        row_col_difference = a_board.find_row_and_col_difference(start_id, end_id)
        row_difference = row_col_difference[0]

        # if black hunter is moving forward/down board, we need to check if its properly moving like a rook
        if a_board.is_going_down(start_id, end_id):
            if a_board.is_up_down_left_right_valid(start_id, end_id):
                result = True
        #if black hunter is moving backwards/up board, we need to check if its properly moving like a bishop
        elif a_board.is_going_up(start_id, end_id):
            if a_board.is_diag_up_down_left_right_valid(start_id, end_id):
                result = True

        return result

    def black_falcon_move_valid(self, start_id, end_id, a_board):
        """takes in a start_id and end_id as strings and a board object. returns true if the black falcon
                moves according to its rules. else return false"""
        result = False
        row_col_difference = a_board.find_row_and_col_difference(start_id, end_id)
        row_difference = row_col_difference[0]

        # if black falcon is moving forward/down board, we need to check if its properly moving like a bishop
        if a_board.is_going_down(start_id, end_id):
            if a_board.is_diag_up_down_left_right_valid(start_id, end_id):
                result = True
        #if black hunter is moving backwards/up board, we need to check if its properly moving like a rook
        elif a_board.is_going_up(start_id, end_id):
            if a_board.is_up_down_left_right_valid(start_id, end_id):
                result = True

        return result

    def white_hunter_move_valid(self, start_id, end_id, a_board):
        """takes in a start_id and end_id as strings and a board object. returns true if the white hunter
                moves according to its rules. else return false"""
        result = False
        row_col_difference = a_board.find_row_and_col_difference(start_id, end_id)
        row_difference = row_col_difference[0]

        # if white hunter is moving forward/up board, we need to check if its properly moving like a rook
        if a_board.is_going_up(start_id, end_id):
            if a_board.is_up_down_left_right_valid(start_id, end_id):
                result = True
        # if white hunter is moving backwards/down board, we need to check if its properly moving like a bishop
        elif a_board.is_going_down(start_id, end_id):
            if a_board.is_diag_up_down_left_right_valid(start_id, end_id):
                result = True

        return result

    def white_falcon_move_valid(self, start_id, end_id, a_board):
        """takes in a start_id and end_id as strings and a board object. returns true if the white falcon
                moves according to its rules. else return false"""
        result = False
        row_col_difference = a_board.find_row_and_col_difference(start_id, end_id)
        row_difference = row_col_difference[0]

        # if white falcon is moving forward/up board, we need to check if its properly moving like a bishop
        if a_board.is_going_up(start_id, end_id):
            if a_board.is_diag_up_down_left_right_valid(start_id, end_id):
                result = True
        # if white falcon is moving backwards/down board, we need to check if its properly moving like a rook
        elif a_board.is_going_down(start_id, end_id):
            if a_board.is_up_down_left_right_valid(start_id, end_id):
                result = True

        return result


class Board:
    """A board object is a list of 8 lists. Each list represents a row on the chessboard. For instance,
    the 0 index of the first list refers to spot “a8” on the chess board, the 7th index of the first list
    refers to spot “h8”, the 0 index of the 8th list refers to spot “a1” on the chess board, and the 7th index
    of the 8th list refers to spot “1h” on the chessboard. When a board object is created, it also creates Piece
    objects like “rook” and “pawn” and places them on their proper starting position on the board. So the board
    class interacts with the Piece class."""

    def __init__(self):
        self._board = []
        self._white_pieces_on_board = {"rook": 2, "knight": 2, "bishop": 2, "king": 1, "queen": 1,"pawn": 8,"hunter": 0,
                                       "falcon": 0}
        self._black_pieces_on_board = {"rook": 2, "knight": 2, "bishop": 2, "king": 1, "queen": 1,"pawn": 8,"hunter": 0,
                                       "falcon": 0}
        self.create_new_board()
        self.get_pieces_on_board()


    def create_new_board(self):
        """adds 8 lists to the chess_board list. Each element will hold a Piece or None."""

        row_number = 7
        while row_number > -1:
            # create a row
            self._board.append(self.create_board_row())
            row_number -= 1

    def create_board_row(self):
        """fills a list with a size of 8 with None"""

        row = [None, None, None, None,
               None, None, None, None
              ]

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

        self._board[0][0] = Rook("black", "rook")
        self._board[0][7] = Rook("black", "rook")

        self._board[7][0] = Rook("white", "rook")
        self._board[7][7] = Rook("white", "rook")

    def get_knights_on_board(self):
        """creates knight pieces and places them for the start of the game """

        self._board[0][1] = Knight("black", "knight")
        self._board[0][6] = Knight("black", "knight")

        self._board[7][1] = Knight("white", "knight")
        self._board[7][6] = Knight("white", "knight")

    def get_bishops_on_board(self):
        """creates bishop pieces and places them for the start of the game """

        self._board[0][2] = Bishop("black", "bishop")
        self._board[0][5] = Bishop("black", "bishop")

        self._board[7][2] = Bishop("white", "bishop")
        self._board[7][5] = Bishop("white", "bishop")

    def get_kings_on_board(self):
        """creates king pieces and places them for the start of the game """

        self._board[0][4] = King("black", "king")

        self._board[7][4] = King("white", "king")

    def get_queens_on_board(self):
        """creates queen pieces and places them for the start of the game """

        self._board[0][3] = Queen( "black", "queen")

        self._board[7][3] = Queen("white", "queen")

    def get_pawns_on_board(self):
        """creates pawn pieces and places them for the start of the game """

        self._board[1][0] = Pawn("black", "pawn")
        self._board[1][1] = Pawn("black", "pawn")
        self._board[1][2] = Pawn("black", "pawn")
        self._board[1][3] = Pawn("black", "pawn")
        self._board[1][4] = Pawn("black", "pawn")
        self._board[1][5] = Pawn("black", "pawn")
        self._board[1][6] = Pawn("black", "pawn")
        self._board[1][7] = Pawn("black", "pawn")

        self._board[6][0] = Pawn( "white", "pawn")
        self._board[6][1] = Pawn("white", "pawn")
        self._board[6][2] = Pawn("white", "pawn")
        self._board[6][3] = Pawn("white", "pawn")
        self._board[6][4] = Pawn("white", "pawn")
        self._board[6][5] = Pawn("white", "pawn")
        self._board[6][6] = Pawn("white", "pawn")
        self._board[6][7] = Pawn("white", "pawn")


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

    def is_id_within_board_bounds(self, square_id):
        """takes in a string square id and checks whether this id even exists on the board. This helps us makes sure
        we are not inputting any numbers that do not exist on the board ex. i5"""
        result = False

        row_at_id = self.get_row_from_id(square_id)
        col_at_id = self.get_col_from_id(square_id)

        if row_at_id is not None and col_at_id is not None:
            result = True

        return result


    def get_Piece_from_squareID(self, square_id):
        """return piece from the chessboard at square id ex. "a8". If no piece there return None"""

        result = None

        row_index = self.get_row_from_id(square_id)
        col_index = self.get_col_from_id(square_id)
        result = self._board[row_index][col_index]

        return result

    def display_board(self):
        """display the current board"""

        row_index = 0
        col_index = 0
        for row_index in range(8):
            row_str = ""
            while col_index < 8:
                piece_at_indices = self._board[row_index][col_index]
                if piece_at_indices is None:
                    row_str += ". "
                elif piece_at_indices.get_name() == "rook":
                    row_str += "R "
                elif piece_at_indices.get_name() == "knight":
                    row_str += "N "
                elif piece_at_indices.get_name() == "bishop":
                    row_str += "B "
                elif piece_at_indices.get_name() == "king":
                    row_str += "K "
                elif piece_at_indices.get_name() == "queen":
                    row_str += "Q "
                elif piece_at_indices.get_name() == "pawn":
                    row_str += "P "
                elif piece_at_indices.get_name() == "hunter":
                    row_str += "H "
                elif piece_at_indices.get_name() == "falcon":
                    row_str += "F "
                else:
                    row_str += ""

                col_index += 1

            #now col_index > 8
            print(row_str)
            col_index = 0

    def get_white_pieces_on_board(self):
        """returns the dict of white pieces currently on board"""
        return self._white_pieces_on_board

    def get_black_pieces_on_board(self):
        """returns the dict of white pieces currently on board"""
        return self._black_pieces_on_board

    def get_num_of_piece_on_board(self, color, piece_name):
        """takes in a color and piece_name as a string and returns the amount currently on the board"""
        dict_of_pieces = {}

        if color == "white":
            dict_of_pieces = self._white_pieces_on_board
        else:
            # color == black
            dict_of_pieces = self._black_pieces_on_board

        result = dict_of_pieces[piece_name]

        return result

    def has_no_king_on_board(self, color):
        """used for game_state in ChessVar. if a color does not have their king, then they lose"""
        result = False
        num_of_king = None

        if color == "white":
            num_of_king = self.get_num_of_piece_on_board(color, "king")
        elif color == "black":
            num_of_king = self.get_num_of_piece_on_board(color, "king")

        if num_of_king == 0:
            result = True

        return result

    def has_no_fairy_on_board(self, color):
        """used for enter fairy piece in ChessVar. if a color has no fairy on board, then they are trying
        to enter their first one. If a color does have a fairy on board, then they are trying to enter their
        second one. """

        result = False

        dict_of_pieces = {}
        if color == "white":
            dict_of_pieces = self._white_pieces_on_board
        else:
            # color == black
            dict_of_pieces = self._black_pieces_on_board

        if dict_of_pieces["hunter"] == 0 and dict_of_pieces["falcon"] == 0:
            result = True

        return result

    def get_current_num_major_pieces(self, color):
        dict_of_pieces = {}
        num_of_major_pieces, num_of_rook, num_of_bishop, num_of_knight, num_of_queen = 0, 0, 0, 0, 0

        if color == "white":
            dict_of_pieces = self._white_pieces_on_board
        else:
            # color == black
            dict_of_pieces = self._black_pieces_on_board

        num_of_rook = dict_of_pieces["rook"]
        num_of_bishop = dict_of_pieces["bishop"]
        num_of_knight = dict_of_pieces["knight"]
        num_of_queen = dict_of_pieces["queen"]

        num_of_major_pieces = num_of_rook + num_of_bishop + num_of_knight + num_of_queen

        return num_of_major_pieces



    def remove_piece_from_tracker(self, color, piece_name):
        """take in color and piece_name as strings and remove decrement its amount in the dictionary tracker by 1.
        If its value is 0, do nothing"""

        dict_of_pieces = {}
        if color == "white":
            dict_of_pieces = self._white_pieces_on_board
        else:
            # color is black
            dict_of_pieces = self._black_pieces_on_board

        num_of_piece = dict_of_pieces[piece_name]

        # if value is greater than 0, decrement by 1
        if num_of_piece > 0:
            num_of_piece -= 1
            dict_of_pieces[piece_name] = num_of_piece

    def add_fairy_piece_tracker(self, color, a_letter):
        """takes in a color and name of a fairy piece and adds its amount in the dictionary tracker by 1, returns true.
        If we already added this fairy (its value is already 1), return false"""

        result = False
        dict_of_pieces = {}
        piece_name = ""

        if color == "white":
            dict_of_pieces = self._white_pieces_on_board
        else:
            # color is black
            dict_of_pieces = self._black_pieces_on_board

        if a_letter == "H" or a_letter == "h":
            piece_name = "hunter"
        elif a_letter == "F" or a_letter == "f":
            piece_name = "falcon"

        num_of_piece = dict_of_pieces[piece_name]

        # if the number of this piece is equal to zero, incremenet is by 1, update tracker, set result to Trye
        if num_of_piece == 0:
            num_of_piece += 1
            dict_of_pieces[piece_name] = num_of_piece
            result = True
        # else, then we already have that piece in the tracker and result will be false

        return result



    def find_row_and_col_difference(self, start_id, end_id):
        """Use two square ids to figure where the end_id row and col is relative to the start_id.
        If the row difference is positive we will go down the board. If negative we will go up the board.
        If the col difference is positive we will go right. If negative we will go left.
        Return row difference and col difference as a list"""

        row_col_difference = []

        start_row = self.get_row_from_id(start_id)
        end_row = self.get_row_from_id(end_id)
        row_difference = end_row - start_row
        row_col_difference.append(row_difference)

        start_col = self.get_col_from_id(start_id)
        end_col = self.get_col_from_id(end_id)
        col_difference = end_col - start_col
        row_col_difference.append(col_difference)
        return row_col_difference

    def remove_piece_from_board(self, square_id):
        """takes in a string square_id and removes the piece at that id by making it hold None instead"""

        piece_at_id = self.get_Piece_from_squareID(square_id)
        row_at_id = self.get_row_from_id(square_id)
        col_at_id = self.get_col_from_id(square_id)

        if piece_at_id is None:
            return
        else:
            self._board[row_at_id][col_at_id] = None

    def set_piece_at_square(self, start_id, end_id):
        """
        If the square at the end_id is occupied, then we must capture it. remove that piece at the end_id, update
        the piece tracker, and place the piece from the start id onto the end_id square.
        if the square at the end_id is empty then just place the piece from the start_id onto the end_id
        and remove the piece from the start id.
        """
        piece_at_start_id = self.get_Piece_from_squareID(start_id)

        piece_at_end_id = self.get_Piece_from_squareID(end_id)
        row_at_end_id = self.get_row_from_id(end_id)
        col_at_end_id = self.get_col_from_id(end_id)

        #if there is a piece at the end square
        if piece_at_end_id is not None:
            # remove that piece from the dict_tracker
            color_of_end_piece = piece_at_end_id.get_color()
            name_of_end_piece = piece_at_end_id.get_name()
            self.remove_piece_from_tracker(color_of_end_piece, name_of_end_piece)

        # remove that piece at the end_id by replacing it with None
            self._board[row_at_end_id][col_at_end_id] = None

        piece_at_end_id = self.get_Piece_from_squareID(end_id)

        # if there not piece at the end square, or we removed the piece from the end square
        if piece_at_end_id is None:
            #set the piece at the start_id to be at the end_id
            self._board[row_at_end_id][col_at_end_id] = piece_at_start_id

            #remove the piece at the start_id
            self.remove_piece_from_board(start_id)

    def vertical_path_down_is_clear(self, start_id, end_id):
        """takes in 2 square ids as strings and returns false if there is a piece on the way vertically DOWN from the
        start_id to the end_id. the path does NOT include any pieces on the end_id square. return true otherwise"""

        row_difference = self.find_row_and_col_difference(start_id, end_id)[0]
        start_row = self.get_row_from_id(start_id)
        start_col = self.get_col_from_id(start_id)
        end_row = self.get_row_from_id(end_id)
        result = False

        # if going down, row difference should be postive
        distance_from_start_row = 1
        while distance_from_start_row <= row_difference:
            temp_row = start_row + distance_from_start_row
            temp_square = self._board[temp_row][start_col]
            if temp_row == end_row:
                result = True
                break
            else:
                if temp_square is not None:
                    result = False
                    break
            distance_from_start_row += 1

        return result

    def vertical_path_up_is_clear(self, start_id, end_id):
        """takes in 2 square ids as strings and returns false if there is a piece on the way vertically up from the
        start_id to the end_id. the path does NOT include any pieces on the end_id square. return true otherwise"""

        row_difference = self.find_row_and_col_difference(start_id, end_id)[0]
        start_row = self.get_row_from_id(start_id)
        start_col = self.get_col_from_id(start_id)
        end_row = self.get_row_from_id(end_id)
        result = False

        # if going up, row difference should be negative
        distance_from_start_row = -1
        while distance_from_start_row >= row_difference:
            temp_row = start_row + distance_from_start_row
            temp_square = self._board[temp_row][start_col]
            if temp_row == end_row:
                result = True
                break
            else:
                if temp_square is not None:
                    result = False
                    break
            distance_from_start_row -= 1

        return result

    def horizontal_path_right_is_clear(self, start_id, end_id):
        """takes in 2 square ids as strings and returns false if there is a piece on the way horizontally right from the
        start_id to the end_id. the path does NOT include any pieces on the end_id square. return true otherwise"""

        col_difference = self.find_row_and_col_difference(start_id, end_id)[1]
        start_row = self.get_row_from_id(start_id)
        start_col = self.get_col_from_id(start_id)
        end_col = self.get_col_from_id(end_id)
        result = False

        # if going right, col difference should be positive
        distance_from_start_col = 1
        while distance_from_start_col <= col_difference:
            temp_col = start_col + distance_from_start_col
            temp_square = self._board[start_row][temp_col]
            if temp_col == end_col:
                result = True
                break
            else:
                if temp_square is not None:
                    result = False
                    break
            distance_from_start_col += 1

        return result

    def horizontal_path_left_is_clear(self, start_id, end_id):
        """takes in 2 square ids as strings and returns false if there is a piece on the way horizontally LEFT from the
        start_id to the end_id. the path does NOT include any pieces on the end_id square. return true otherwise"""

        col_difference = self.find_row_and_col_difference(start_id, end_id)[1]
        start_row = self.get_row_from_id(start_id)
        start_col = self.get_col_from_id(start_id)
        end_col = self.get_col_from_id(end_id)
        result = False

        # if going left, col difference should be negative
        distance_from_start_col = -1
        while distance_from_start_col >= col_difference:
            temp_col = start_col + distance_from_start_col
            temp_square = self._board[start_row][temp_col]
            if temp_col == end_col:
                result = True
                break
            else:
                if temp_square is not None:
                    result = False
                    break
            distance_from_start_col -= 1

        return result

    def is_going_up(self, start_id, end_id):
        """return true if piece is moving up based on start and end ids. else return false"""
        result = False
        row_difference = self.find_row_and_col_difference(start_id, end_id)[0]
        if row_difference < 0:
            result = True

        return result

    def is_going_down(self, start_id, end_id):
        """return true if piece is moving up based on start and end ids. else return false"""
        result = False
        row_difference = self.find_row_and_col_difference(start_id, end_id)[0]
        if row_difference > 0:
            result = True

        return result

    def is_going_left(self, start_id, end_id):
        """return true if piece is moving up based on start and end ids. else return false"""
        result = False
        col_difference = self.find_row_and_col_difference(start_id, end_id)[1]
        if col_difference < 0:
            result = True

        return result

    def is_going_right(self, start_id, end_id):
        """return true if piece is moving up based on start and end ids. else return false"""
        result = False
        col_difference = self.find_row_and_col_difference(start_id, end_id)[1]
        if col_difference > 0:
            result = True

        return result

    def is_up_down_left_right_valid(self, start_id, end_id):
        """used for queen and rook, king, hunter, falcon movement. if the end_id is up, down, left, OR right to the start_id, and there
        is no pieces in between the start_id and end_id (not including the end_id) return true. Else return false"""
        result = False
        list_of_row_col_path = self.find_row_and_col_difference(start_id, end_id)

        # if end is on the same row as start
        if self.get_row_from_id(end_id) == self.get_row_from_id(start_id):
            # if going left, check if there is a clear path left
            if self.is_going_left(start_id, end_id):
                if self.horizontal_path_left_is_clear(start_id, end_id):
                    result = True
            # if going right, check if there is a clear path right
            elif self.is_going_right(start_id, end_id):
                if self.horizontal_path_right_is_clear(start_id, end_id):
                    result = True
        # if end is on the same column as start
        elif self.get_col_from_id(end_id) == self.get_col_from_id(start_id):
            # if going up, check if up path is clear
            if self.is_going_up(start_id, end_id):
                if self.vertical_path_up_is_clear(start_id, end_id):
                    result = True
            # if going down, check if down path is clear
            elif self.is_going_down(start_id, end_id):
                if self.vertical_path_down_is_clear(start_id, end_id):
                    result = True
        else:
            result = False

        return result

    def is_diag_up_left_valid(self, start_id, end_id):
        """takes in 2 string ids and returns true if there is a clear path diagonal up left from start_id to end_id"""

        #we are gonna keep doing decrementing row and col by 1 until we reach end_id
        result = False
        row_col_difference = self.find_row_and_col_difference(start_id, end_id)
        row_difference = row_col_difference[0]
        col_difference = row_col_difference[1]

        start_row = self.get_row_from_id(start_id)
        start_col = self.get_col_from_id(start_id)
        end_row = self.get_row_from_id(end_id)
        end_col = self.get_col_from_id(end_id)

        # if going up left, row and col difference should be both be negative
        distance_from_start_col = -1
        distance_from_start_row = -1

        #this could be distance_from_start_row or column
        while distance_from_start_row >= row_difference:
            temp_col = start_col + distance_from_start_col
            temp_row = start_row + distance_from_start_row
            temp_square = self._board[temp_row][temp_col]
            if temp_row == end_row:
                result = True
                break
            else:
                if temp_square is not None:
                    result = False
                    break
            distance_from_start_row -= 1
            distance_from_start_col -= 1

        return result

    def is_diag_up_right_valid(self, start_id, end_id):
        """takes in 2 string ids and returns true if there is a clear path diagonal right up from start_id to end_id"""

        result = False
        row_col_difference = self.find_row_and_col_difference(start_id, end_id)
        row_difference = row_col_difference[0]
        col_difference = row_col_difference[1]

        start_row = self.get_row_from_id(start_id)
        start_col = self.get_col_from_id(start_id)
        end_row = self.get_row_from_id(end_id)
        end_col = self.get_col_from_id(end_id)

        # if going up right, row should be both be negative and col should be positive
        distance_from_start_row = -1
        distance_from_start_col = 1

        #this could be distance_from_start_row or column
        while distance_from_start_row >= row_difference:
            temp_col = start_col + distance_from_start_col
            temp_row = start_row + distance_from_start_row
            temp_square = self._board[temp_row][temp_col]
            if temp_row == end_row:
                result = True
                break
            else:
                if temp_square is not None:
                    result = False
                    break
            distance_from_start_row -= 1
            distance_from_start_col += 1

        return result

    def is_diag_down_left_valid(self, start_id, end_id):
        """takes in 2 string ids and returns true if there is a clear path diagonal down left from start_id to end_id"""

        result = False
        row_col_difference = self.find_row_and_col_difference(start_id, end_id)
        row_difference = row_col_difference[0]
        col_difference = row_col_difference[1]

        start_row = self.get_row_from_id(start_id)
        start_col = self.get_col_from_id(start_id)
        end_row = self.get_row_from_id(end_id)
        end_col = self.get_col_from_id(end_id)

        # if going down right, row should be positive and col should be negative
        distance_from_start_row = 1
        distance_from_start_col = -1

        #this could be distance_from_start_row or column
        while distance_from_start_row <= row_difference:
            temp_col = start_col + distance_from_start_col
            temp_row = start_row + distance_from_start_row
            temp_square = self._board[temp_row][temp_col]
            if temp_row == end_row:
                result = True
                break
            else:
                if temp_square is not None:
                    result = False
                    break
            distance_from_start_row += 1
            distance_from_start_col -= 1

        return result

    def is_diag_down_right_valid(self, start_id, end_id):
        """takes in 2 string ids and returns true if there is a clear path diagonal right down from start_id to end_id"""
        result = False
        row_col_difference = self.find_row_and_col_difference(start_id, end_id)
        row_difference = row_col_difference[0]
        col_difference = row_col_difference[1]

        start_row = self.get_row_from_id(start_id)
        start_col = self.get_col_from_id(start_id)
        end_row = self.get_row_from_id(end_id)
        end_col = self.get_col_from_id(end_id)

        # if going down right, row and col should be both be positive
        distance_from_start_row = 1
        distance_from_start_col = 1

        #this could be distance_from_start_row or column
        while distance_from_start_row <= row_difference:
            temp_col = start_col + distance_from_start_col
            temp_row = start_row + distance_from_start_row
            temp_square = self._board[temp_row][temp_col]
            if temp_row == end_row:
                result = True
                break
            else:
                if temp_square is not None:
                    result = False
                    break
            distance_from_start_row += 1
            distance_from_start_col += 1

        return result

    def is_diag_up_down_left_right_valid(self, start_id, end_id):
        """takes in 2 string ids and returns true if there is a clear path diagonal either diagonal up, down, left or
        right between the start_id and end_id"""

        result = False
        row_col_difference = self.find_row_and_col_difference(start_id, end_id)
        row_difference = row_col_difference[0]
        col_difference = row_col_difference[1]

        #if we are going up left: row and col difference both negative
        if row_difference < 0 and col_difference < 0:
            # if there are no pieces up left diagonally not including end_id square, then valid
            if self.is_diag_up_left_valid(start_id, end_id):
               result = True
        #if we are going up right: row is negative and col is positive
        elif row_difference < 0 and col_difference > 0:
            # if there are no pieces up right diagonally not including end_id square, then valid
            if self.is_diag_up_right_valid(start_id, end_id):
               result = True
        #if we are going down left: row is positive, and col is negative
        elif row_difference > 0 and col_difference < 0:
            if self.is_diag_down_left_valid(start_id, end_id):
               result = True
        #if we are going down right: row is positive and col is postive
        elif row_difference > 0 and col_difference > 0:
            if self.is_diag_down_right_valid(start_id, end_id):
               result = True
        else:
            result = False

        return result

