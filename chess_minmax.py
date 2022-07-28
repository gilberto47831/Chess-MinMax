#!/usr/bin/env python3

#author:Gilberto Ramirez

import string
import random
import os
import sys
import time
import math
from IPython.display import clear_output

def ChessBoardSetup():
    # initialize and return a chess board - create a 2D 8x8 array that has the value for each cell
    # . for empty board cell
    # p/P for pawn
    # r/R for rook
    # t/T for knight
    # b/B for bishop
    # q/Q for queen
    # k/K for king
    black_pawns = ['p' for i in range(8)]
    white_pawns = [piece.upper() for piece in black_pawns]
    black = ['r', 't', 'b', 'q', 'k', 'b', 't', 'r']
    white = [piece.upper() for piece in black]

    board = []
    board.append(black)
    board.append(black_pawns)
    board.append(['.', '.', '.', '.', '.', '.', '.', '.'])
    board.append(['.', '.', '.', '.', '.', '.', '.', '.'])
    board.append(['.', '.', '.', '.', '.', '.', '.', '.'])
    board.append(['.', '.', '.', '.', '.', '.', '.', '.'])
    board.append(white_pawns)
    board.append(white)

    return board

def DrawBoard(board):
    # r t b q k b t r
    # p p p p p p p p 
    # . . . . . . . .
    # . . . . . . . .
    # . . . . . . . .
    # . . . . . . . .
    # P P P P P P P P
    # R T B Q K B T R

    for row in board:
      for col in row:
        print(col, end=' ')
      print()

def MovePiece(from_piece, to_piece, board):
    
    piece = board[from_piece[0]][from_piece[1]]

    board[from_piece[0]][from_piece[1]] = '.'

    board[to_piece[0]][to_piece[1]] = piece

    return board

# return True if the input move (from-square and to-square) is legal, else False
def IsMoveLegal(from_square, to_square, board, player):
    # input is from-square and to-square
    # use the input and the board to get the from-piece and to-piece

    from_piece = board[from_square[0]][from_square[1]]
    to_piece = board[to_square[0]][to_square[1]]

    #check that we aren't attacking our own piece
    if to_piece != '.':
      
      if from_piece.isupper() and to_piece.isupper():
        return False

      elif from_piece.islower() and to_piece.islower():
        return False
    #make sure player is moving their own piece
    if player == 'white' and from_piece.islower():
      return False

    elif player == 'black' and from_piece.isupper():
      return False

    # if from-square is the same as to-square
        # return False
    if from_square == to_square:
        return False
    
    # if the from-piece is a "pawn"
    if from_piece == 'p' or from_piece == 'P':
        ## case - pawn wants to move one step forward (or backward if white)

        row_diff = to_square[0] - from_square[0]
        col_diff = to_square[1] - from_square[1]
        # if to-square is empty and is in the same column as the from-square
            # return True
        if (player == 'white' and row_diff == -1 and col_diff == 0) or (player == 'black' and row_diff == 1 and col_diff == 0):
          if to_piece == '.':
            return True
        

        ## case - pawn can move two spaces forward (or backward if white) ONLY if pawn on starting row
        # else if to-square is empty and from-square-row = 2 (or 7 if white) and to-square-row = from-square-row + 2 (or -2 if white)
            # if IsClearPath() - a clear path exists between from-square and to-square
                # return True

        elif (player == 'white' and row_diff == -2 and from_square[0] == 6) or (player == 'black' and row_diff == 2 and from_square[0] == 1):
          if to_piece == '.' and col_diff == 0:
            if IsClearPath(from_square, to_square, board):
              return True

        ## case - pawn attacks the enemy piece if diagonal
        # else if there is piece diagonally forward (or backward if white) and that piece belongs to the enemy team
            # return True
        elif player == 'black' and row_diff == 1 and to_piece != '.' and abs(col_diff) == 1:
          return True

        elif player == 'white' and row_diff == -1 and to_piece != '.' and abs(col_diff) == 1:
          return True
          

    # else if the from-piece is a "rook"
    elif from_piece == 'r' or from_piece == 'R':
        row_diff = to_square[0] - from_square[0]
        col_diff = to_square[1] - from_square[1]

        # if to-square is either in the same row or column as the from-square
        if row_diff == 0 or col_diff == 0:
            # if to-square is either empty or contains a piece that belongs to the enemy team
            if to_piece == '.' or IsEnemy(to_piece, player, board):
                # if IsClearPath() - a clear path exists between from-square and to-square
                if IsClearPath(from_square, to_square, board):
                    return True
                    # return True

    # else if the from-piece is a "bishop"
    elif from_piece == 'b' or from_piece == 'B':

        # if to-square is diagonal wrt from-square
        x = to_square[0] - from_square[0]
        y = to_square[1] - from_square[1]

        if abs(x) == abs(y): 

            # if to-square is either empty or contains a piece that belongs to the enemy team
            if to_piece == '.' or IsEnemy(to_piece, player, board):

                # if IsClearPath() - a clear path exists between from-square and to-square
                if IsClearPath(from_square, to_square, board):
                    return True
                    # return True

    # else if the from-piece is a "queen"
    elif from_piece == 'q' or from_piece == 'Q':
        row_diff = to_square[0] - from_square[0]
        col_diff = to_square[1] - from_square[1]

        # if to-square is either in the same row or column as the from-square
            # if to-square is either empty or contains a piece that belongs to the enemy team
                # if IsClearPath() - a clear path exists between from-square and to-square
                    # return True

        if col_diff == 0 or row_diff == 0:
            # if to-square is either empty or contains a piece that belongs to the enemy team
            if to_piece == '.' or IsEnemy(to_piece, player, board):
                # if IsClearPath() - a clear path exists between from-square and to-square
                if IsClearPath(from_square, to_square, board):
                    return True


        # if to-square is diagonal wrt from-square
            # if to-square is either empty or contains a piece that belongs to the enemy team
                # if IsClearPath() - a clear path exists between from-square and to-square
                    # return True

        x = to_square[0] - from_square[0]
        y = to_square[1] - from_square[1]

        if abs(x) == abs(y): 

            # if to-square is either empty or contains a piece that belongs to the enemy team
            if to_piece == '.' or IsEnemy(to_piece, player, board):

                # if IsClearPath() - a clear path exists between from-square and to-square
                if IsClearPath(from_square, to_square, board):
                    return True


    # else if the from-piece is a "knight"
    elif from_piece == 't' or from_piece == 'T':

        # calculate the col-diff = to-square-col - from-square-col
        col_diff = to_square[1] - from_square[1]
        # calculate the row-diff = to-square-row - from-square-row
        row_diff = to_square[0] - from_square[0]

        # if to-square is either empty or contains a piece that belongs to the enemy team
        if to_piece == '.' or IsEnemy(to_piece, player, board):
            # return True for any of the following cases:
                # col-diff = 1 & row_dif = -2
                # col-diff = 2 & row_dif = -1
                # col-diff = 2 & row_dif = 1
                # col-diff = 1 & row_dif = 2
                # col-diff = -1 & row_dif = -2
                # col-diff = -2 & row_dif = -1
                # col-diff = -2 & row_dif = 1
                # col-diff = -1 & row_dif = 2
                if col_diff == 1 and row_diff == -2:
                  return True
                if col_diff == 2 and row_diff == -1:
                  return True
                if col_diff == 2 and row_diff == 1:
                  return True
                if col_diff == 1 and row_diff == 2:
                  return True                  
                if col_diff == -1 and row_diff == -2:
                  return True               
                if col_diff == -2 and row_diff == -1:
                  return True
                if col_diff == -2 and row_diff == 1:
                  return True
                if col_diff == -1 and row_diff == 2:
                  return True
    # else if the from-piece is a "king"
    elif from_piece == 'k' or from_piece == 'K':

        col_diff = abs(to_square[1] - from_square[1])
        row_diff = abs(to_square[0] - from_square[0])

        # calculate the col-diff = to-square-col - from-square-col
        # calculate the row-diff = to-square-row - from-square-row
        # if to-square is either empty or contains a piece that belongs to the enemy team
        if to_piece == '.' or IsEnemy(to_piece, player, board):

            # return True for any of the following cases:
            if col_diff == 1 and row_diff == 0:
              return True
            if col_diff == 0 and row_diff == 1:
              return True
            if col_diff == 1 and row_diff == 1:
              return True

                # abs(col-diff) = 1 & abs(row_dif) = 0
                # abs(col-diff) = 2 & abs(row_dif) = 1
                # abs(col-diff) = 1 & abs(row_dif) = 1

    # return False - if none of the other True's are hit above
    else:
      return False


# gets a list of legal moves for a given piece
# input = from-square
# output = list of to-square locations where the piece can move to
def GetListOfLegalMoves(from_square, board, player):
    # input is the current player and the given piece as the from-square
    # initialize the list of legal moves, i.e., to-square locations to []
    legal_moves = []
    # go through all squares on the board
    for i in range(8):
      for j in range(8):
        to_square = (i, j)
        ret = IsMoveLegal(from_square, to_square, board, player)
        if ret:
          ret = DoesMovePutPlayerInCheck(from_square, to_square, board, player)
          if not ret:
            legal_moves.append(to_square)

    return legal_moves


# gets a list of all pieces for the current player that have legal moves
def GetPiecesWithLegalMoves(board, player):
    # initialize the list of pieces with legal moves to []
    pieces = []
    # go through all squares on the board
    for i in range(8):
      for j in range(8):
        if board[i][j] == '.':
          continue
        from_square = (i, j)
        piece = board[i][j]
        if IsFriendly(piece, player, board):
    # for the selected 
    
        # if the square contains a piece that belongs to the current player's team
          legal = GetListOfLegalMoves(from_square, board, player)
            # call GetListOfLegalMoves() to get a list of all legal moves for the selected piece / square 
            # if there are any legel moves
          if legal:
            pieces.append(from_square)
                # append this piece to the list of pieces with legal moves
    # return the final list of pieces with legal moves
    return pieces

# returns True if the current player is in checkmate, else False
def IsCheckmate(player, board):
    # call GetPiecesWithLegalMoves() to get all legal moves for the current player
    moves = GetPiecesWithLegalMoves(board, player)
    # if there is no piece with any valid move
        # return False
    if moves:
      return False
    else:
      return True
    # else
        # return True

def IsEnemy(piece, player, board):
  if piece != '.':

    if player == 'black' and piece.isupper():
      return True
    elif player =='white' and piece.islower():
      return True

def IsFriendly(piece, player, board):
  if piece != '.':
    if player == 'black' and piece.islower():
      return True
    elif player =='white' and piece.isupper():
      return True

# returns True if the given player is in Check state
def IsInCheck(player, board):
    # find given player's King's location = king-square
    if player == 'white':
      enemy = 'black'
    else: 
      enemy = 'white'

    for i in range(8):
      for j in range(8):
        piece = board[i][j]
        if piece == 'k' or piece == 'K':
          if IsFriendly(piece, player, board):
            king_square = (i, j)
            break
    
    for i in range(8):
      for j in range(8):
        from_piece = (i, j)
        piece = board[i][j]

        if piece != '.' and IsEnemy(piece, player, board):

          if IsMoveLegal(from_piece, king_square, board, enemy):
            return True

    return False

# helper function to figure out if a move is legal for straight-line moves (rooks, bishops, queens, pawns)
# returns True if the path is clear for a move (from-square and to-square), non-inclusive
def IsClearPath(from_square, to_square, board):
    # given the move (from-square and to-square)
    piece = board[from_square[0]][from_square[1]]
    dist = int(math.sqrt( (to_square[0] - from_square[0])**2 + (to_square[1] - from_square[1])**2 ))
    # if the from and to squares are only one square apart and to-square is empty
        # return True

    ve_vert = to_square[0] - from_square[0]
    ve_horiz = to_square[1] - from_square[1]
    x = to_square[0] - from_square[0]
    y = to_square[1] - from_square[1]

    if dist == 1: #and board[to_square[0]][to_square[1]] == '.':
      return True

    else: 
        # if to-square is in the +ve vertical direction from from-square
            # new-from-square = next square in the +ve vertical direction
          if from_square[1] == to_square[1] and ve_vert < 0:
            new_from_square = (from_square[0] - 1, from_square[1])
        # else if to-square is in the -ve vertical direction from from-square
            # new-from-square = next square in the -ve vertical direction
          elif from_square[1] == to_square[1] and ve_vert > 0:
            new_from_square = (from_square[0] + 1, from_square[1])

        # else if to-square is in the +ve horizontal direction from from-square
            # new-from-square = next square in the +ve horizontal direction
          elif from_square[0] == to_square[0] and ve_horiz > 0:
            new_from_square = (from_square[0], from_square[1] + 1)
        # else if to-square is in the -ve horizontal direction from from-square
            # new-from-square = next square in the -ve horizontal direction
          elif from_square[0] == to_square[0] and ve_horiz < 0:
            new_from_square = (from_square[0], from_square[1] - 1)

        # else if to-square is in the SE diagonal direction from from-square
            # new-from-square = next square in the SE diagonal direction
          elif abs(ve_vert) == abs(ve_horiz) and ve_vert > 0 and ve_horiz > 0:
            new_from_square = (from_square[0] + 1, from_square[1] + 1)

        # else if to-square is in the SW diagonal direction from from-square
            # new-from-square = next square in the SW diagonal direction
          elif abs(ve_vert) == abs(ve_horiz) and ve_vert > 0 and ve_horiz < 0:
            new_from_square = (from_square[0] + 1, from_square[1] - 1)

        # else if to-square is in the NE diagonal direction from from-square
            # new-from-square = next square in the NE diagonal direction
          elif abs(ve_vert) == abs(ve_horiz) and ve_vert < 0 and ve_horiz > 0:
            new_from_square = (from_square[0] - 1, from_square[1] + 1)

        # else if to-square is in the NW diagonal direction from from-square
            # new-from-square = next square in the NW diagonal direction
          elif abs(ve_vert) == abs(ve_horiz) and ve_vert < 0 and ve_horiz < 0:
            new_from_square = (from_square[0] - 1, from_square[1] - 1)


    # if new-from-square is not empty
        # return False
    # else
        # return the result from the recursive call of IsClearPath() with the new-from-square and to-square
    if board[new_from_square[0]][new_from_square[1]] != '.':
      return False
    else:
      return IsClearPath(new_from_square, to_square, board)



# makes a hypothetical move (from-square and to-square)
# returns True if it puts current player into check
def DoesMovePutPlayerInCheck(from_square, to_square, board, player):
  
    # given the move (from-square and to-square), find the 'from-piece' and 'to-piece'
    from_piece = board[from_square[0]][from_square[1]]
    to_piece = board[to_square[0]][to_square[1]]
    
    board = MovePiece(from_square, to_square, board)

    ret = IsInCheck(player, board)

    board[from_square[0]][from_square[1]] = from_piece
    board[to_square[0]][to_square[1]] = to_piece

    return ret


    # make the move temporarily by changing the 'board'
    # Call the IsInCheck() function to see if the 'player' is in check - save the returned value
    # Undo the temporary move
    # return the value saved - True if it puts current player into check, False otherwise

def GetAllMoves(board, player):
  moves = []
  #obtain all moves for given player in form: (from_square, to_square)
  for from_square in GetPiecesWithLegalMoves(board, player):
    for to_square in GetListOfLegalMoves(from_square, board, player):
      moves.append((from_square, to_square))
  
  return moves

def GetRandomMove(board, player):
    # pick a random piece and a random legal move for that piece
    pieces = GetPiecesWithLegalMoves(board, player)
    from_square = random.choice(pieces)

    legal_moves = GetListOfLegalMoves(from_square, board, player)
    to_square = random.choice(legal_moves)

    return from_square, to_square


def evl(board, player):
    # this function will calculate the score on the board, if a move is performed
    # give score for each of piece and calculate the score for the chess board
  pieces = {
      'P': 1, 
      'R': 5, 
      'T': 3,
      'B': 3,
      'Q': 9,
      'K': 40,
      'p': 1, 
      'r': 5, 
      't': 3,
      'b': 3,
      'q': 9,
      'k': 40
  }
  value = 0
  for i in range(8):
    for j in range(8):
      piece = board[i][j]
      if piece in pieces:
        if IsFriendly(piece, player, board):
          value += pieces[piece]
        elif IsEnemy(piece, player, board):
          value -= pieces[piece]

  return value


def GetMinMaxMove(board, player):
    # return the best move for the current player using the MinMax strategy
    # to get the allocated points, searching should be 2-ply (one Max and one Min)
  
  max_val = -9999999
  best_move = None
  global prunes

  #FOR PRUNING UNEEDED NODES
  max_alpha = -math.inf
  max_beta = math.inf
  ### MAXIMIZE ###
  for i in GetAllMoves(board, player):
    #get move
    max_from_square = i[0]
    max_to_square = i[1]
    #save state
    max_from_piece = board[max_from_square[0]][max_from_square[1]]
    max_to_piece = board[max_to_square[0]][max_to_square[1]]
    
    #make move
    board = MovePiece(max_from_square, max_to_square, board)
    
    min_val = 99999999

    min_alpha = -math.inf
    min_beta = math.inf

    ### MINIMIZE ###
    #go through enemie's moves
    for j in GetAllMoves(board, 'black'):

      #get move
      min_from_square = j[0]
      min_to_square = j[1]
      #save state
      min_from_piece = board[min_from_square[0]][min_from_square[1]]
      min_to_piece = board[min_to_square[0]][min_to_square[1]]
      #make move
      board = MovePiece(min_from_square, min_to_square, board)

      #eval board
      val = evl(board, player)

      if val < min_beta:
        min_beta = val

      #MIN CASE
      if val < min_val:
        min_val = val

      #undo move
      board[min_from_square[0]][min_from_square[1]] = min_from_piece
      board[min_to_square[0]][min_to_square[1]] = min_to_piece
      
      ##if max is greater, WE CAN BE SURE WE'LL NEVER SELECT 
      #ANYTHONG FROM THIS NODE
      if max_alpha > min_beta:
        prunes += 1
        break


    if min_beta > max_alpha:
      max_alpha = min_beta
    #undo move
    board[max_from_square[0]][max_from_square[1]] = max_from_piece
    board[max_to_square[0]][max_to_square[1]] = max_to_piece

    #moves.append((min_val, i))
    #MAX CASE
    if min_val > max_val:
      max_val = min_val
      best_move = i

  #moves[0] = (0, ((2, 2), (3, 3)))
  #moves.sort(key=lambda tup: tup[0], reverse=True)   
  #return moves[0][1]
  return best_move


# initialize and setup the board
# player assignment and counter initializations
board = ChessBoardSetup()
turns = 0
N = 100

prunes = 0
#our player
player = 'white'

# main game loop - while a player is not in checkmate or stalemate (<N turns)
# below is the rough looping strategy
while not IsCheckmate(player, board) and turns < N:
    clear_output()
    DrawBoard(board)
    print()

    if player == 'white':
      from_square, to_square = GetMinMaxMove(board, player)
      player = 'black'
    else:
      from_square, to_square = GetRandomMove(board, player)
      player = 'white'

    board = MovePiece(from_square, to_square, board)

    DrawBoard(board)
    #time.sleep(.5)
    turns += 1

# check and print - Stalemate or Checkmate
if IsCheckmate(player, board):
  print(f'CHECKMATE IN {turns} TURNS!') 

else: 
  print("STALEMATE!")

print(f'PRUNED {prunes} NODES TOTAL!')
