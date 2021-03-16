from unittest import TestCase, mock
from chess_objects import Board, Move, Piece, Square, King, Queen, Rook, Bishop, Knight, Pawn
from chess import ChessGame


class TestChess(TestCase):
    def setUp(self) -> None:
        self.board = Board()
        self.move = Move()
        self.game = ChessGame()

    def test__King(self):
        self.setUp()
        king = self.board.squares[7][4].get_piece()
        self.assertEqual(self.board.squares[7][4].piece.is_white, True)
        self.assertEqual(king.valid_move(self.board, self.board.squares[7][4], self.board.squares[7][3]), False)
        self.board.squares[6][4].piece = None
        self.assertEqual(self.board.squares[6][4].is_occupied(), False)
        self.assertEqual(king.valid_move(self.board, self.board.squares[7][4], self.board.squares[6][4]), True)

    def test__Queen(self):
        self.setUp()
        queen = self.board.squares[7][3].get_piece()
        self.assertEqual(self.board.squares[7][3].piece.is_white, True)
        self.assertEqual(queen.valid_move(self.board, self.board.squares[7][3], self.board.squares[7][4]), False)
        self.board.squares[6][4].piece = None
        self.assertEqual(self.board.squares[6][4].is_occupied(), False)
        self.assertEqual(queen.valid_move(self.board, self.board.squares[7][3], self.board.squares[3][7]), True)

    def test__Rook(self):
        self.setUp()
        self.board.squares[4][4].piece = Rook(True, 4, 4)
        self.assertEqual(self.board.squares[4][4].piece.valid_move(self.board, self.board.squares[4][4], self.board.squares[3][4]), True)

    def test__Bishop(self):
        self.setUp()
        self.board.squares[4][4].piece = Bishop(True, 4, 4)
        self.assertEqual(self.board.squares[4][4].piece.valid_move(self.board, self.board.squares[4][4], self.board.squares[2][6]), True)
        self.assertEqual(self.board.squares[4][4].piece.valid_move(self.board, self.board.squares[4][4], self.board.squares[2][2]), True)

    def test__Knight(self):
        self.setUp()
        self.board.squares[4][4].piece = Knight(True, 4, 4)
        self.assertEqual(self.board.squares[4][4].piece.valid_move(self.board, self.board.squares[4][4], self.board.squares[3][6]), True)

    def test__Pawn(self):
        self.setUp()
        self.board.squares[4][4].piece = Pawn(True, 4, 4)
        self.board.squares[3][3].piece = Pawn(False, 3, 3)
        self.assertEqual(self.board.squares[4][4].piece.valid_move(self.board, self.board.squares[4][4], self.board.squares[3][4]), True)
        self.assertEqual(self.board.squares[4][4].piece.valid_move(self.board, self.board.squares[4][4], self.board.squares[3][3]), True)
        self.assertEqual(self.board.squares[4][4].piece.valid_move(self.board, self.board.squares[4][4], self.board.squares[3][5]), False)
        self.assertEqual(self.board.squares[4][4].piece.valid_move(self.board, self.board.squares[4][4], self.board.squares[4][3]), False)

    def test_interpret_move(self):
        self.setUp()
        self.assertEqual(self.move.interpret_move(['e', '2', 'e', '3']), [6, 4, 5, 4])
        self.assertEqual(self.move.valid_piece_move(self.board, [6, 4, 5, 4]), True)
