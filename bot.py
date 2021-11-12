from textwrap import wrap
import random
import chess
import copy

def CheckForResult(originalBoard, deep, root = False, side = "White", makeCopy = True):
	if makeCopy: board = copy.deepcopy(originalBoard)
	else: board = originalBoard

	if deep <= 0:
		#Check statistics
		total = 0
		if board.outcome() != None:
			res = board.outcome().result()

			if res == "1-0": return 700
			elif res == "0-1": return -700

		pieceMap = board.piece_map()
		for piece in pieceMap:
			if pieceMap[piece] == chess.Piece.from_symbol('P'): total += 1
			elif pieceMap[piece] == chess.Piece.from_symbol('p'): total -= 1

			elif pieceMap[piece] == chess.Piece.from_symbol('N'): total += 3
			elif pieceMap[piece] == chess.Piece.from_symbol('B'): total += 3

			elif pieceMap[piece] == chess.Piece.from_symbol('n'): total -= 3
			elif pieceMap[piece] == chess.Piece.from_symbol('b'): total -= 3

			elif pieceMap[piece] == chess.Piece.from_symbol('R'): total += 5
			elif pieceMap[piece] == chess.Piece.from_symbol('r'): total -= 5

			elif pieceMap[piece] == chess.Piece.from_symbol('Q'): total += 9
			elif pieceMap[piece] == chess.Piece.from_symbol('q'): total -= 9

		return total

	possibleSituations = {}
	for possibleMove in board.legal_moves:
		newBoard = copy.deepcopy(board)
		newBoard.push((possibleMove))
		possibleSituations[possibleMove] = CheckForResult(newBoard, deep-1, side=side, makeCopy=False)

	bestMove = None
	bestResult = -1000 if side == "White" else 1000

	#Needs to filter the best move from possibillities
	if root:
		# Needs to give best move.
		for possibleMove in possibleSituations:
			if side == "White" and possibleSituations[possibleMove] > bestResult:
				bestResult = possibleSituations[possibleMove]
				bestMove = possibleMove
			elif side == "Black" and possibleSituations[possibleMove] < bestResult:
				bestResult = possibleSituations[possibleMove]
				bestMove = possibleMove
			elif possibleSituations[possibleMove] == bestResult:
				if random.getrandbits(1):
					bestResult = possibleSituations[possibleMove]
					bestMove = possibleMove
				... # Same outcome
		return bestMove, bestResult
	else:
		worstResult = -1000 if side == "Black" else 1000
		# Find the worst situation of enemies answers
		for possibleMove in possibleSituations:
			if side == "Black" and possibleSituations[possibleMove] > worstResult:
				worstResult = possibleSituations[possibleMove]
			elif side == "White" and possibleSituations[possibleMove] < worstResult:
				worstResult = possibleSituations[possibleMove]
			else:
				... # Same outcome
		return worstResult

import chess.pgn

board = chess.Board()

if input("Type of game (b - bots, r - real): ").upper() == 'B':
	game = chess.pgn.Game()
	game.headers["Event"] = "Bot test"
	game.headers["White"] = "White bot power 3"
	game.headers["Black"] = "Black bot power 3"
	game.setup(board)
	node = game

	print("Starting...")

	def Split(s):
		res = ""
		leftUntilSpace = 2
		for character in s:
			if not leftUntilSpace: res += " "
			res += character
			leftUntilSpace -= 1
		return res

	while board.outcome() == None:
		try:
			move = CheckForResult(board, 4, True, "White")
			print(str(move[0]) + ",", \
				"good material" if not move[1] \
				else ("White is winning by " + str(abs(move[1]))) if move[1] > 0 \
				else ("Black is winning by " + str(abs(move[1]))))
			print(" Possible moves found:", len(list(board.legal_moves)))
			board.push_san(str(move[0]))
			node = node.add_variation(move[0])

			move = CheckForResult(board, 3, True, "Black")
			print(str(move[0]) + ",", \
				"good material" if not move[1] \
				else ("White is winning by " + str(abs(move[1]))) if move[1] > 0 \
				else ("Black is winning by " + str(abs(move[1]))))
			print(" Possible moves found:", len(list(board.legal_moves)))
			board.push_san(str(move[0]))
			# recording += board.fen() 
			node = node.add_variation(move[0])

			print(board)

		except Exception as e:
			print(e)
			break
	else:
		...
else:
	while board.outcome() == None:
		possibleMoves = len(list(board.legal_moves))
		if possibleMoves >= 19: move = CheckForResult(board, 3, True, "White")
		else: move = CheckForResult(board, 4, True, "White")
		print(str(move[0]))# + ",", \
			# "good material" if not move[1] \
			# else ("White is winning by " + str(abs(move[1]))) if move[1] > 0 \
			# else ("Black is winning by " + str(abs(move[1]))))
		# print(" Possible moves found:", len(list(board.legal_moves)))
		board.push_san(str(move[0]))

		move = input("> ")
		while len(move) != 4:
			print("Error: illegal move")
			move = input("> ")

		board.push_san(move)

print(board.outcome())
print(board.result())
print("\n\n\n", game)