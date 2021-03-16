from typing import List
import math
from dataclasses import dataclass


@dataclass
class Player(object):
    """
    Player Class:
    Used to keep track of player
    """
    is_white: bool
    turn: int
    castled: bool = False

    def __init__(self, white: bool):
        self.is_white = white
        self.set_turn()

    def set_turn(self):
        """
        Used to set the which player's turn it is
        """
        if self.is_white:
            self.turn = 0
        else:
            self.turn = 1


class Piece(object):
    """
    SuperClass Piece used to define the subclasses:
    King, Queen, Rook, Bishop, Knight, Pawn
    """
    x: int
    y: int
    captured: bool
    is_white: bool
    piece_name: str = "Empty"

    def __init__(self, white: bool, x: int, y: int):
        """
        Initializes the piece and sets whether the piece is white or black

        :param white: true for white and false for black
        """
        self.captured = False
        self.is_white = white
        self.set_piece_name()
        self.x = x
        self.y = y

    def set_piece_name(self):
        """
        sets the Piece Name
        :return: None
        """
        self.piece_name = "Empty"

    def get_piece_name(self) -> str:
        """
        Gets the piece name
        :return: Piece name in string
        """
        return self.piece_name

    def is_white(self) -> bool:
        """
        Ask if the piece is white

        :return: true if piece is white, false if piece is black
        """
        return self.is_white

    def set_coords(self, x:int, y: int):
        """
        Sets the location of the piece
        :param x: the row it is on
        :param y: the column it is on
        :return:
        """
        self.x = x
        self.y = y

    def is_captured(self) -> bool:
        """
        Ask if the piece has been captured

        :return: if true piece captured else piece is still on board
        """
        return self.captured

    def set_captured(self):
        """
        Used when the piece has been captured

        :return: None
        """
        self.captured = True

    def valid_move(self, board, start_square, end_square) -> bool:
        """
        Checks if the move inputted is valid for specific piece.
        Method is overwritten in each Piece Subclass
        :param board: (Board) 2d Array of Square Objects
        :param start_square: (Square) Starting Square
        :param end_square: (Square) Ending Square
        :return: True if move is valid, False if invalid
        """
        return True


class Square(object):
    piece: Piece
    x: int
    y: int
    attacked: bool = False

    def __init__(self, x: int, y: int):
        """
        Initializes the Square Object and sets the position and leaves piece empty
        :param x: Row
        :param y: Column
        """
        self.x = x
        self.y = y
        self.piece = None

    def occupy_square(self, piece: Piece) -> Piece:
        """
        Sets the Piece on this Square object

        :param piece: (Piece) the Piece to set on Square
        :return:
        """
        original_piece = self.piece
        if self.piece is not None:
            self.piece.set_captured(True)
        self.piece = piece
        return original_piece

    def release_square(self) -> Piece:
        """
        Sets piece on Square to None

        :return: Piece that used to be on the Square
        """
        released_piece = self.piece
        self.piece = None
        return released_piece

    def is_occupied(self) -> bool:
        """
        Checks to see if the Square has a piece on it

        :return: True if piece is on Square, False if Square is void
        """
        if self.piece is None:
            return False
        return True

    def set_piece(self, piece: Piece):
        """
        Sets the piece onto the Square
        :param piece:
        :return: None
        """
        self.piece = piece

    def get_piece(self) -> Piece:
        """
        Gets the Piece that is on the Square
        :return: Piece on Square
        """
        return self.piece


class Board(object):
    """
    Board Object
    """
    display_board = [
        ['. ', '. ', '. ', '. ', '. ', '. ', '. ', '. '],
        ['. ', '. ', '. ', '. ', '. ', '. ', '. ', '. '],
        ['. ', '. ', '. ', '. ', '. ', '. ', '. ', '. '],
        ['. ', '. ', '. ', '. ', '. ', '. ', '. ', '. '],
        ['. ', '. ', '. ', '. ', '. ', '. ', '. ', '. '],
        ['. ', '. ', '. ', '. ', '. ', '. ', '. ', '. '],
        ['. ', '. ', '. ', '. ', '. ', '. ', '. ', '. '],
        ['. ', '. ', '. ', '. ', '. ', '. ', '. ', '. ']
    ]

    def __init__(self):
        """
        Initializes the Board, Creates the array of squares and sets up the pieces
        """
        self.squares = [[Square(i, j) for j in range(8)] for i in range(8)]
        self.reset_board()

    def print_board(self):
        """
        Prints out the display board so the user can see the pieces
        :return: None
        """
        for i in range(len(self.display_board)):
            print(
                self.display_board[i][0],
                self.display_board[i][1],
                self.display_board[i][2],
                self.display_board[i][3],
                self.display_board[i][4],
                self.display_board[i][5],
                self.display_board[i][6],
                self.display_board[i][7]
            )

    def reset_board(self):
        """
        Places the correct pieces on the correct Squares

        :return: None
        """
        # Places Pawns B/W
        for i in [1, 6]:
            for j in range(len(self.display_board)):
                color = True
                if i == 1:
                    color = False
                self.display_board[i][j] = 'P '
                self.squares[i][j].occupy_square(Pawn(color, i, j))
        # Place Black Pieces
        # Places Rooks
        self.display_board[0][0] = 'R '
        self.squares[0][0].occupy_square(Rook(False, 0, 0))
        self.display_board[0][7] = 'R '
        self.squares[0][7].occupy_square(Rook(False, 0, 7))
        # Places Knights
        self.display_board[0][1] = 'N '
        self.squares[0][1].occupy_square(Knight(False, 0, 1))
        self.display_board[0][6] = 'N '
        self.squares[0][6].occupy_square(Knight(False, 0, 6))
        # Places Bishops
        self.display_board[0][2] = 'B '
        self.squares[0][2].occupy_square(Bishop(False, 0, 2))
        self.display_board[0][5] = 'B '
        self.squares[0][5].occupy_square(Bishop(False, 0, 5))
        # Places Queens
        self.display_board[0][3] = 'Q '
        self.squares[0][3].occupy_square(Queen(False, 0, 3))
        # Places Kings
        self.display_board[0][4] = 'K '
        self.squares[0][4].occupy_square(King(False, 0, 4))

        # Place White Pieces
        # Places Rooks
        self.display_board[7][0] = 'R '
        self.squares[7][0].occupy_square(Rook(True, 7, 0))
        self.display_board[7][7] = 'R '
        self.squares[7][7].occupy_square(Rook(True, 7, 7))
        # Places Knights
        self.display_board[7][1] = 'N '
        self.squares[7][1].occupy_square(Knight(True, 7, 1))
        self.display_board[7][6] = 'N '
        self.squares[7][6].occupy_square(Knight(True, 7, 6))
        # Places Bishops
        self.display_board[7][2] = 'B '
        self.squares[7][2].occupy_square(Bishop(True, 7, 2))
        self.display_board[7][5] = 'B '
        self.squares[7][5].occupy_square(Bishop(True, 7, 5))
        # Places Queens
        self.display_board[7][3] = 'Q '
        self.squares[7][3].occupy_square(Queen(True, 7, 3))
        # Places Kings
        self.display_board[7][4] = 'K '
        self.squares[7][4].occupy_square(King(True, 7, 4))

    def update_board(self):
        """
        Updates the Display board with the new position of all the Pieces

        :return: None
        """
        pieces = ['K ', 'Q ', 'R ', 'B ', 'K ', 'P ']
        for i in range(len(self.display_board)):
            for j in range(len(self.display_board)):
                if self.squares[i][j].is_occupied():
                    self.display_board[i][j] = self.squares[i][j].piece.piece_name
                else:
                    self.display_board[i][j] = '. '


class Move(object):
    """
    Move Object

    Moves will be input as coordinates where a - h are the Columns and 1 - 8 are the rows.
    a1 is on the bottom left of the player with the white pieces
    """

    current_move: List = []
    def get_move(self, raw_move: str) -> List:
        """
        Gets the move as a string with simple chess notation and seperates it
        :param raw_move: (String) String containing the users move
        :return: List of the individual characters
        """
        if len(raw_move) > 4:
            return []
        return [char for char in raw_move]

    def is_move_valid(self, move: List) -> bool:
        """
        Checks to see whether the move inputted by used is within the bounds of the board

        :param move: (List: str)A list of the characters of the user input string
        :return: True if move is valid, False if invalid
        """
        if not move:
            return False
        columns = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        rows = ['8', '7', '6', '5', '4', '3', '2', '1']
        if (move[0] in columns) is False:
            return False
        if (move[2] in columns) is False:
            return False
        if (move[1] in rows) is False:
            return False
        if (move[3] in rows) is False:
            return False
        return True

    def interpret_move(self, move: List) -> List:
        """
        Converts the move into a move able to be used to index squares

        :param move: (List: str)List of Characters from move
        :return: List of integers
        """
        columns = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        rows = ['8', '7', '6', '5', '4', '3', '2', '1']
        start_x = rows.index(move[1])
        start_y = columns.index(move[0])
        end_x = rows.index(move[3])
        end_y = columns.index(move[2])
        start_end_squares = [start_x, start_y, end_x, end_y]
        return start_end_squares

    def valid_piece_move(self, board: Board, move: List) -> bool:
        """
        Checks to see if the move is valid for the set piece and that their is a piece on the Square
        :param board: (Board) 2d List of Squares
        :param move: (List: int) List of the integers to be inputted
        :return: True if the move is valid, False if the mve is invalid
        """
        if board.squares[move[0]][move[1]].is_occupied() is False:
            return False
        piece = board.squares[move[0]][move[1]].get_piece()
        start_square = board.squares[move[0]][move[1]]
        end_square = board.squares[move[2]][move[3]]
        if piece.valid_move(board, start_square, end_square) is False:
            return False
        return True


class King(Piece):
    castled: bool = False

    def set_piece_name(self):
        self.piece_name = "K "

    def valid_move(self, board: Board, start_square: Square, end_square: Square):
        """
        Checks if the movement given is a valid King movement

        :param board: (Board)2d list of Square objects
        :param start_square: (Square)the starting Square object of the piece
        :param end_square: (Square)the ending Square object of the piece
        :return: True if move is valid, False if move is invalid
        """
        if end_square.is_occupied():
            if self.is_white == end_square.piece.is_white:
                return False
        x_dist = start_square.x - end_square.x
        y_dist = start_square.y - end_square.y
        abs_dist = math.sqrt(x_dist ** 2 + y_dist ** 2)
        if abs_dist > 1.5:
            return False
        return True


class Queen(Piece):
    def set_piece_name(self):
        self.piece_name = "Q "

    def valid_move(self, board: Board, start_square: Square, end_square: Square):
        """
        Checks if the movement given is a valid Queen movement

        :param board: (Board)2d list of Square objects
        :param start_square: (Square)the starting Square object of the piece
        :param end_square: (Square)the ending Square object of the piece
        :return: True if move is valid, False if move is invalid
        """
        # checks end Square to see if piece is there and if so if it is the same color
        if end_square.is_occupied():
            if self.is_white == end_square.piece.is_white:
                return False
        x_dist = start_square.x - end_square.x
        y_dist = start_square.y - end_square.y
        if (abs(x_dist) > 0 and abs(y_dist) > 0) and (abs(x_dist) is not abs(y_dist)):
            return False
        if self.is_obstructed(board, x_dist, y_dist):
            return False
        return True

    def is_obstructed(self, board: Board, x: int, y: int) -> bool:
        """
        Checks to see if there is a piece between start space and end space leading to an invalid move

        :param board: (Board)board: 2d list of Square objects
        :param x: (Int) Columns between start space and end square
        :param y: (Int) Rows between start and end square
        :return:
        """
        if y == 0:
            for i in range(1, abs(x)):
                j = int(i * (x / abs(x)))
                if board.squares[self.x - j][self.y].is_occupied():
                    return True
        if x == 0:
            for k in range(1, abs(y)):
                n = int(k * (y / abs(y)))
                if board.squares[self.x][self.y - n].is_occupied():
                    return True
        if abs(x) == abs(y):
            for u in range(1, abs(x)):
                m = u * int((x / abs(x)))
                p = u * int((y / abs(y)))
                if board.squares[self.x - m][self.y - p].is_occupied():
                    return True
        return False


class Rook(Piece):  # Completed
    def set_piece_name(self):
        self.piece_name = "R "

    # determine whether the move is a valid move for the piece
    def valid_move(self, board: Board, start_square: Square, end_square: Square):
        """
        Checks if the movement given is a valid Rook movement

        :param board: (Board)2d list of Square objects
        :param start_square: (Square)the starting Square object of the piece
        :param end_square: (Square)the ending Square object of the piece
        :return: True if move is valid, False if move is invalid
        """
        # checks end Square to see if piece is there and if so if it is the same color
        if end_square.is_occupied():
            if self.is_white == end_square.piece.is_white:
                return False
        x_dist = start_square.x - end_square.x
        y_dist = start_square.y - end_square.y
        # Prevent Diagonal Movement
        if abs(x_dist) > 0 and abs(y_dist) > 0:
            return False
        # checks Squares between it and destination
        if self.is_obstructed(board, x_dist, y_dist):
            return False
        return True

    def is_obstructed(self, board: Board, x: int, y: int) -> bool:
        """
        Checks to see if there is a piece between start space and end space leading to an invalid move

        :param board: (Board)board: 2d list of Square objects
        :param x: (Int) Columns between start space and end square
        :param y: (Int) Rows between start and end square
        :return:
        """
        if y == 0:
            for i in range(1, abs(x)):
                j = int(i * (x / abs(x)))
                if board.squares[self.x - j][self.y].is_occupied():
                    return True
        if x == 0:
            for k in range(1, abs(y)):
                n = int(k * (y / abs(y)))
                if board.squares[self.x][self.y - n].is_occupied():
                    return True
        return False

    pass


class Knight(Piece):  # Completed
    def set_piece_name(self):
        """
        Sets the pieces name

        :return: None
        """
        self.piece_name = "N "

    def valid_move(self,board: Board, start_square: Square, end_square: Square):
        """
        Checks if the movement given is a valid Rook movement

        :param start_square: (Square)the starting Square object of the piece
        :param end_square: (Square)the ending Square object of the piece
        :return: True if move is valid, False if move is invalid
        """
        if end_square.is_occupied():
            if self.is_white == end_square.piece.is_white:
                return False
        x_dist = start_square.x - end_square.x
        y_dist = start_square.y - end_square.y
        if (abs(x_dist) == 2 and abs(y_dist) != 1) or (abs(x_dist) == 1 and abs(y_dist) != 2):
            return False
        return True


class Bishop(Piece):  # Completed
    def set_piece_name(self):
        """
        Sets the pieces name

        :return: None
        """
        self.piece_name = "B "

    def valid_move(self, board: Board, start_square: Square, end_square: Square):
        """
        Checks if the movement given is a valid Rook movement

        :param board: (Board)2d list of Square objects
        :param start_square: (Square)the starting Square object of the piece
        :param end_square: (Square)the ending Square object of the piece
        :return: True if move is valid, False if move is invalid
        """
        if end_square.is_occupied():
            if self.is_white == end_square.piece.is_white:
                return False
        x_dist = start_square.x - end_square.x
        y_dist = start_square.y - end_square.y
        # Check to see if the movement is diagonal
        if abs(x_dist) is not abs(y_dist):
            return False
        if self.is_obstructed(board, x_dist, y_dist):
            return False
        return True

    def is_obstructed(self, board: Board, x: int, y: int) -> bool:
        """
        Checks to see if there is a piece between start space and end space leading to an invalid move

        :param board: (Board)board: 2d list of Square objects
        :param x: (Int) Columns between start space and end square
        :param y: (Int) Rows between start and end square
        :return:
        """
        for i in range(1, abs(x)):
            j = i * int((x / abs(x)))
            k = i * int((y / abs(y)))
            if board.squares[self.x - j][self.y - k].is_occupied():
                return True
        return False

    pass


class Pawn(Piece):
    """
    Pawn Piece Object:
    subclass of Piece Object
    """
    first_move: bool = True

    def set_piece_name(self):
        self.piece_name = "P "

    def valid_move(self, board: Board, start_square: Square, end_square: Square) -> bool:
        """
        Asks if the movement given is a valid pawn movement

        :param board: (Board)2d list of Square objects
        :param start_square: (Square)the starting Square object of the piece
        :param end_square: (Square)the ending Square object of the piece
        :return: True if move is valid, False if move is invalid
        """
        if end_square.is_occupied():
            if self.is_white == end_square.piece.is_white:
                return False
        x_dist = start_square.x - end_square.x
        y_dist = start_square.y - end_square.y
        abs_dist = math.sqrt(x_dist ** 2 + y_dist ** 2)
        # Prevents piece from moving more than 1 space at a time
        if abs_dist > 1.5:
            return False
        if y_dist == 1 and x_dist ==0:
            return False
        # Prevents White pieces from moving backwards
        elif self.is_white and x_dist < 0:
            return False
        # Prevents Black pieces from moving backwards
        elif self.is_white is False and x_dist > 0:
            return False
        elif self.is_obstructed(board) and abs_dist == 1:
            return False
        elif self.can_capture(board, end_square) is False and abs_dist > 1:
            return False
        return True

    def can_capture(self, board: Board, target_square: Square) -> bool:
        """
        Determines if the pawn has the possibility to capture

        :param board: (Board)2D array Squares containing all the active pieces
        :param target_square: (Square) square being attacked
        :return: True if a piece of the opposite color is on a Square object in front of and adjacent to the pawn
        """
        if self.y == target_square.y:
            return False
        if target_square.is_occupied():
            if target_square.piece.is_white != self.is_white:
                return True
        return False

    def is_obstructed(self, board: Board) -> bool:
        """
        Determines whether the path in front of the pawn is blocked

        :param board:(Board) 2D list of Square objects
        :return: Return True if pawn is blocked false if unobstructed
        """
        if self.is_white and board.squares[self.x - 1][self.y].is_occupied():
            return True
        if self.is_white is False and board.squares[self.x + 1][self.y].is_occupied():
            return True
        return False


class ChessGame(object):
    board = Board()
    current_turn: int
    white_side = Player(True)
    black_side = Player(False)
    players = [white_side, black_side]
    move = Move()
    white_won: bool = False
    black_won: bool = False
    captured_pieces = []

    def __init__(self):
        self.current_turn = 0

    def get_move(self, player_idx: int) -> bool:
        valid_move: bool = False
        if self.current_turn % 2 != self.players[player_idx].turn:
            return False
        player_move = input(f"Enter move for player{player_idx + 1}:")
        raw_move = self.move.get_move(player_move)
        if self.move.is_move_valid(raw_move):
            self.move.current_move = self.move.interpret_move(raw_move)
            if self.move.valid_piece_move(self.board, self.move.current_move):
                valid_move = self.board.squares[self.move.current_move[0]][self.move.current_move[1]].piece.is_white == \
                             self.players[player_idx].is_white
        while valid_move is False:
            player_move = input(f"Invalid Move Please Re-enter for player{player_idx + 1}:")
            raw_move = self.move.get_move(player_move)
            if self.move.is_move_valid(raw_move):
                self.move.current_move = self.move.interpret_move(raw_move)
                if self.move.valid_piece_move(self.board, self.move.current_move):
                    valid_move = self.board.squares[self.move.current_move[0]][
                                     self.move.current_move[1]].piece.is_white == self.players[player_idx].is_white
        return True

    def get_move(self, player_idx: int, player_move: str) -> bool:
        valid_move: bool = False
        if self.current_turn % 2 != self.players[player_idx].turn:
            return False
        raw_move = self.move.get_move(player_move)
        if self.move.is_move_valid(raw_move):
            self.move.current_move = self.move.interpret_move(raw_move)
            if self.move.valid_piece_move(self.board, self.move.current_move):
                valid_move = self.board.squares[self.move.current_move[0]][self.move.current_move[1]].piece.is_white == \
                             self.players[player_idx].is_white
        return valid_move

    def execute_move(self, player_idx: int):
        if self.get_move(player_idx):
            start_x = self.move.current_move[0]
            start_y = self.move.current_move[1]
            end_x = self.move.current_move[2]
            end_y = self.move.current_move[3]

            temp_piece = self.board.squares[start_x][start_y].release_square()
            if self.board.squares[end_x][end_y].is_occupied():
                self.board.squares[end_x][end_y].piece.set_captured()
                captured_piece = self.board.squares[end_x][end_y].get_piece()
                self.captured_pieces.append(captured_piece)
                if captured_piece.piece_name == "K ":
                    if captured_piece.is_white:
                        self.black_won = True
                    else:
                        self.white_won = True

            self.board.squares[end_x][end_y].set_piece(temp_piece)
            self.board.squares[end_x][end_y].piece.set_coords(end_x, end_y)
            self.current_turn += 1
        else:
            print(f"Incorrect player trying to make move. Current player turn:{player_idx}")

    def game_won(self) -> bool:
        if self.white_won:
            print("White Won")
            return False
        if self.black_won:
            print("Black Won")
            return False
        return True
    def who_won(self) -> str:
        if self.white_won:
            return "White Won"
        if self.black_won:
            return "Black Won"
        return ""

    def run(self):
        self.board.print_board()
        game_continue = True
        while game_continue:
            self.execute_move(self.current_turn % 2)
            self.board.update_board()
            self.board.print_board()
            game_continue = self.game_won()


def main():
    chess = ChessGame()
    chess.run()
    return True


if __name__ == '__main__':
    main()
