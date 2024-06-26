import random
import csv
import copy
import time
from copy import deepcopy

# Object used to create new boards


class Board:
    def __init__(self, size):
        self.size = size
        self.board = []

    # Used to fill the "board" property with a list with a length equal to the "size" property
    def create_board(self):
        for y_pos in range(self.size):
            for x_pos in range(self.size):
                #  Create a Tile instance
                #  Gives it the coordinates (depending on x_pos and y_pos)
                #  Add it to the board property
                if x_pos != 0 and x_pos != 7 and y_pos != 0 and y_pos != 7:
                    self.board.append(Tile(x_pos, y_pos, "🟩", "🟩"))
                else:
                    self.board.append(Tile(x_pos, y_pos, "X", "🟩"))
        self.place_initial_pawns()

    #  This will print the game board, depending on the data_type
    #  Data types are "Coordinates", "Type" and "Content"
    def draw_board(self, data_type):
        display_board = []
        line_breaker = 0
        print([0, ' 0', ' 1', ' 2', ' 3', ' 4', ' 5', ' 6', ' 7'])
        for board_index in self.board:
            if (board_index.x_pos == 0):
                display_board.append(board_index.y_pos)
            if data_type == "Coordinates":
                display_board.append([board_index.x_pos, board_index.y_pos])
            elif data_type == "Type":
                display_board.append(board_index.type)
            else:
                display_board.append(board_index.content)
            line_breaker += 1
            if line_breaker > 7:
                print(display_board)
                line_breaker = 0
                display_board = []
        print("\n")

    # Place the 4 initial pawns at the center of the board (2 white and 2 black)
    def place_initial_pawns(self):
        #  We pick the 4 central tiles
        #  And place 2 black pawns and 2 white pawns
        self.board[27].content = "⚪"
        self.board[28].content = "⚫"
        self.board[35].content = "⚫"
        self.board[36].content = "⚪"
        
    # Check if the position in inside the board
    # Return true or false depending if it is inside or not
    def is_on_board(self, x_pos, y_pos):
        if x_pos < 0 or x_pos > 7 or y_pos < 0 or y_pos > 7:
            return False
        else:
            return True

    # Check if the tile is an empty tile ("🟩")
    # Return true or false depending if it is empty or not
    def is_tile_empty(self, x_pos, y_pos):
        if self.board[(x_pos) + y_pos * 8].content == "🟩":
            return True
        else:
            return False

    # Takes a position (x_pos, y_pos) and a color
    # Try to simulate the move
    # Returns either false if the move is not valid
    # Or returns which pawns will change color if true
    # The returned list will contain [numbers_of_pawns_to_change, [direction_x, direction_y]]
    def is_legal_move(self, x_pos, y_pos, color):

        # North / Nort-East / East / South-East / South / South-West / West / North-West
        directions = [
            [0, -1],
            [1, -1],
            [1, 0],
            [1, 1],
            [0, 1],
            [-1, 1],
            [-1, 0],
            [-1, -1],
        ]

        # Opposite of the color of the placed pawn
        if color == "⚪":
            awaited_color = "⚫"
        else:
            awaited_color = "⚪"

        current_x_pos = x_pos
        current_y_pos = y_pos
        is_legal = False
        # [number_of_tile_to_flip, direction]
        # Si on a un pion noir placé en 2,3, on veut:
        # [[1, [1, 0]]
        tiles_to_flip = []

        if (not self.is_tile_empty(current_x_pos, current_y_pos) or not self.is_on_board(current_x_pos, current_y_pos)):
            return False

        # Check for every direction
        for current_dir in directions:
            number_of_tiles_to_flip = 1
            # Get your original coordinates + the direction modifier
            current_x_pos = x_pos + current_dir[0]
            current_y_pos = y_pos + current_dir[1]
            # Check if the new position is on the board and empty
            if self.is_on_board(current_x_pos, current_y_pos):
                #  Get the tile informations
                current_index = self.board[current_x_pos + current_y_pos * 8]
                # If the tile contains a pawn of the opposite color, continue on the line
                while current_index.content == awaited_color:
                    current_x_pos += current_dir[0]
                    current_y_pos += current_dir[1]
                    if self.is_on_board(current_x_pos, current_y_pos):
                        current_index = self.board[current_x_pos +
                                                   current_y_pos * 8]
                        # If the line ends with a pawn of your color, then the move is legal
                        if current_index.content == color:
                            is_legal = True
                            tiles_to_flip.append(
                                [number_of_tiles_to_flip, current_dir])
                            break
                    else:
                        break
                    number_of_tiles_to_flip += 1

        if is_legal:
            return tiles_to_flip
        else:
            return False

    # Takes a position (x_pos, y_pos), an array with a number of tiles to flip and a direction, and a color
    # The array should be obtained with the "is_legal_move" function
    # Doesn't return anything, but will change the color of the tiles selected by "tiles_to_flip"
    def flip_tiles(self, x_pos, y_pos, tiles_to_flip, color):
        # x_pos and y_pos = new pawn position
        # tiles_to_flip = list containing the number of pawn to flip and a direction
        # ex: [
        # [1, [1, 0]],
        # ] means we're changing 1 pawn to the right
        # color = the new color of the pawns to flip
        for current_dir in tiles_to_flip:
            current_x_pos = x_pos + current_dir[1][0]
            current_y_pos = y_pos + current_dir[1][1]
            for nb_tile in range(current_dir[0]):
                current_index = self.board[current_x_pos + current_y_pos * 8]
                current_index.content = color
                current_x_pos += current_dir[1][0]
                current_y_pos += current_dir[1][1]

# Used to create each tile of your board
# Contains a position (x, y), a type to check if it's a boder tile or not, and a content to check if there is a pawn inside the tile


class Tile:
    #   Type is used to check if its an "🟩" empty tile or a "X" border tile
    #   Content is used to check if a pawn is placed o (Empty), B (Black), W (White)
    def __init__(self, x_pos, y_pos, type, content):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.type = type
        self.content = content

# Used to create new ruleset
# Contains the score, the active player, the game_over check and functions allowing to interact with the game


class Game:
    def __init__(self):
        self.score_black = 2
        self.score_white = 2
        self.active_player = "⚫"
        self.is_game_over = False
        self.winner = "Noone"

    # Place a pawn on the board (checks if the move is legal before placing it)
    # It takes a position (x, y), a Board object instance and a color
    # The function will automatically check if the move is valid or not
    def place_pawn(self, x_pos, y_pos, board_instance, color):
        if not board_instance.is_on_board(x_pos, y_pos):
            print("Coordinates outside the board")
        else:
            if board_instance.board[(x_pos) + y_pos * 8].content == "🟩":
                tiles_to_flip = board_instance.is_legal_move(
                    x_pos, y_pos, color)
                if not tiles_to_flip:
                    print("Invalid move")
                else:
                    board_instance.board[(x_pos) + y_pos * 8].content = color
                    board_instance.flip_tiles(
                        x_pos, y_pos, tiles_to_flip, color)
                    print(f"Pion placé en {x_pos}, {y_pos}")
                    self.update_score(board_instance)
                    self.change_active_player()
                    self.check_for_valid_moves(board_instance)
                    board_instance.draw_board("Content")
            else:
                print("There is already a pawn here")

    # Change the active player color from black to white or white to black
    def change_active_player(self):
        # Prend self.active_player et change la couleur du joueur actif
        if self.active_player == "⚫":
            self.active_player = "⚪"
            print("C'est au tour du joueur blanc")
        else:
            self.active_player = "⚫"
            print("C'est au tour du joueur noir")

    # Update the players score after a successful move
    def update_score(self, board_instance):
        # Count all the black & white pawns, and update the scores
        w_score = 0
        b_score = 0
        for tile_index in board_instance.board:
            if tile_index.content == "⚪":
                w_score += 1
            elif tile_index.content == "⚫":
                b_score += 1
        self.score_black = b_score
        self.score_white = w_score

    # Check for a valid move, and end the game if there is none for the current player
    def check_for_valid_moves(self, board_instance):
        is_game_over = True
        for tile_index in board_instance.board:
            move_to_check = board_instance.is_legal_move(
                tile_index.x_pos, tile_index.y_pos, self.active_player)
            if move_to_check != False:
                is_game_over = False

        if is_game_over:
            self.check_for_winner()
            self.is_game_over = True

    # Compare the score, and print the winner's color
    def check_for_winner(self):
        print("Partie terminée !")
        print("Le joueur noir a: " + str(self.score_black) + " points")
        print("Le joueur white a: " + str(self.score_white) + " points")
        if (self.score_black > self.score_white):
            print("Le joueur noir a gagné !")
            self.winner = "⚫"
        elif (self.score_white > self.score_black):
            print("Le joueur blanc a gagné !")
            self.winner = "⚪"
        else:
            print("Égalité !")

class Xx_Bender_Destroyer_30_xX :
    def __init__(self):
        self.name = "Xx_Bender_Destroyer_3.0_xX"
        

    def check_valid_moves(self, base_board, base_game):
        
        cpt_tile = 0
        number_of_flip = 0
        biggest_number_of_flip = -21
        lowest_number_of_flip = 10
        valid_moves = []
        best_coordinates = []
        best_coordinates_on_border = []
        check_valid = []
        new_board = Board(8)
        new_board.create_board()
        current_part = 1
        best_move = []


        bonus_matrix_20_moins = [100, -10, 5, 2, 2, 5, -10, 100,
                                -10, -20, 2, 2, 2, 2, -20, -10,
                                5, 2, 20, 15, 15, 20, 2, 5,
                                2, 2, 15, 0, 0, 15, 2, 2,
                                2, 2, 15, 0, 0, 15, 2, 2,
                                5, 2, 20, 15, 15, 20, 2, 5,
                                -10, -20, 2, 2, 2, 2, -20, -10,
                                100, -10, 5, 2, 2, 5, -10, 100]
        
      
        bonus_matrix_20_plus = [100, -20, 5, 2, 2, 5, -20, 100,
                                -20, -30, 2, 2, 2, 2, -30, -20,
                                5, 2, 2, 1, 1, 2, 2, 5,
                                2, 2, 1, 0, 0, 1, 2, 2,
                                2, 2, 1, 0, 0, 1, 2, 2,
                                5, 2, 2, 1, 1, 2, 2, 5,
                                -20, -30, 2, 2, 2, 2, -30, -20,
                                100, -20, 5, 2, 2, 5, -20, 100]

  
        if current_part <= 16:
            bonus_matrix = bonus_matrix_20_moins
            
        else:
            bonus_matrix = bonus_matrix_20_plus
            
        for tile in range(len(new_board.board)):
            new_board.board[tile].weight = bonus_matrix[tile]
                
        current_part += 1
        
        
        

        
        for tile_index in base_board.board:
            move_to_check = base_board.is_legal_move(tile_index.x_pos, tile_index.y_pos, base_game.active_player)
            if move_to_check:
                valid_moves.append(move_to_check)
                
                if (tile_index.x_pos, tile_index.y_pos) in [(0, 0), (0, 7), (7, 0), (7, 7)]:
                    return (tile_index.x_pos, tile_index.y_pos)
                
                
            
                if (tile_index.x_pos, tile_index.y_pos) in [(2, 0), (3, 0), (4, 0), (5, 0), (0, 2), (0, 3),
                                                            (0, 4), (0, 5), (7, 2), (7, 3), (7, 4), (7, 5), (2, 7),
                                                            (3, 7), (4, 7), (5, 7)]:
                    return(tile_index.x_pos, tile_index.y_pos)
                
                
                number_of_flip = 0
                
                for move_to_check_index in range(len(move_to_check)):
                    
                    number_of_flip = number_of_flip + move_to_check[move_to_check_index][0]

                number_of_flip += new_board.board[cpt_tile].weight
                
                if current_part <= 6:
                    if number_of_flip < 2 and number_of_flip > 0:
                        return (tile_index.x_pos, tile_index.y_pos)
                        
                    
                if number_of_flip > biggest_number_of_flip:
                    biggest_number_of_flip = number_of_flip
                    best_coordinates = [[tile_index.x_pos, tile_index.y_pos, biggest_number_of_flip]]
                elif number_of_flip == biggest_number_of_flip:
                    best_coordinates.append([tile_index.x_pos, tile_index.y_pos, biggest_number_of_flip])

            
                
            cpt_tile += 1 

        best_coordinates = random.choices(best_coordinates)
        best_coordinates = best_coordinates[0]
        return best_coordinates
    
    
    
    def minmax(self, depth, board, game, maximizing_player):
        if depth == 0 or game.is_game_over:
            return self.evaluate_board(board, game), None

        valid_moves = self.get_valid_moves(board, game)
        best_move = None

        if maximizing_player:
            max_eval = float('-inf')

            for move in valid_moves:
                temp_board = copy.deepcopy(board)
                temp_game = copy.deepcopy(game)

                temp_game.place_pawn(move[0], move[1], temp_board, game.active_player)
                eval, _ = self.minmax(depth - 1, temp_board, temp_game, False)

                if eval > max_eval:
                    max_eval = eval
                    best_move = move

            return max_eval, best_move

        else:
            min_eval = float('inf')

            for move in valid_moves:
                temp_board = copy.deepcopy(board)
                temp_game = copy.deepcopy(game)

                temp_game.place_pawn(move[0], move[1], temp_board, game.active_player)
                eval, _ = self.minmax(depth - 1, temp_board, temp_game, True)

                if eval < min_eval:
                    min_eval = eval
                    best_move = move

            return min_eval, best_move

        
        
        
    def get_valid_moves(self, board100, game100):
        valid_moves = []
        for tile_index in board100.board:
                move_to_check = board100.is_legal_move(tile_index.x_pos, tile_index.y_pos, game100.active_player)
                if move_to_check:
                    valid_moves.append([tile_index.x_pos, tile_index.y_pos])
        return valid_moves
    
    
    def evaluate_board(self, board1000, game1000):
        return game1000.score_black - game1000.score_white
        
        
 

class concurent:
   
    def __init__(self):
        self.name = "concurent"


    def check_valid_moves_test(self, board, game,depth):
        matrice_list = [
            100, -25,  50,  50,  50,  50, -25, 100,
            -25, -50, -15, -15, -15, -15, -50, -25,
             50, -15,  10,  10,  10,  10, -15,  50,
             50, -15,  10, 'X', 'X',  10, -15,  50,
             50, -15,  10, 'X', 'X',  10, -15,  50,
             50, -15,  10,  10,  10,  10, -15,  50,
            -25, -50, -15, -15, -15, -15, -50, -25,
            100, -25,  50,  50,  50,  50, -25,  100
        ]
        newboard = deepcopy(board)
        matrice_list = self.initialize_matrix(newboard,matrice_list, game.active_player)
        max_points = -10000
        playable_moves = []
        final_max_point = 0
        points_per_move = []
        final_playable_moves = []
        turn = game.score_black + game.score_white - 4
        for index in range(len(board.board)):
            square_info = board.is_legal_move(board.board[index].x_pos, board.board[index].y_pos, game.active_player)
            if square_info != False:
                points_per_case = 0
                #ajout du poids en fonction de la case
                weight = newboard.board[index].content
                #On calcule le nombre de points en fonctions de la position et de la direction
                #square_direction /points_per_case /
                for square_direction in range(len(square_info)):
                    if(turn < 20):
                        points_per_case -= square_info[square_direction][0]
                    else:
                        points_per_case += square_info[square_direction][0]


                points_per_case += weight
                #On récupère le coup qui rapporte le maximum de points
                if max_points == points_per_case:
                    playable_moves.append([board.board[index].x_pos, board.board[index].y_pos,max_points])
                elif max_points < points_per_case:
                    max_points  = points_per_case
                    playable_moves = [[board.board[index].x_pos, board.board[index].y_pos,max_points]]
       
       
        if depth > 0:
            depth -=1
            playable_moves = self.best_moves(playable_moves, board, game, depth)
            # 2 list for the points / final moves
            # Get the points value and store them
            for move in playable_moves:
                points_per_move.append(move[2])
            # Check for the maximum value
            final_max_point = max(points_per_move)
            # Only fill the final list with the highest score moves
            for move in playable_moves:
                if(move[2] == final_max_point):
                    final_playable_moves.append(move)
            return random.choice(final_playable_moves)
        return random.choice(playable_moves)
   
    def best_moves(self,playable_moves, board, game, depth):
        for index in playable_moves:
            # Init copy board / game
            new_board = deepcopy(board)
            new_game = deepcopy(game)
            # Place pawn, recursive call for check_valid_moves
            #print(index)
            new_game.place_pawn(index[0], index[1], new_board, new_game.active_player)
            if new_game.is_game_over == False:
                opponent_points = self.check_valid_moves_test(new_board, new_game, depth)
            # Tile score update
                index.append(index[2]-opponent_points[2])
                index.pop(2)
        return playable_moves


    # function allow to initialize a bord with a matrix
    def initialize_matrix(self,table,matrice_list,color):
        if color == table.board[0].content :
            matrice_list[1] = 75
            matrice_list[8] = 75
        if color == table.board[7].content :
            matrice_list[6] = 75
            matrice_list[15] = 75
        if color == table.board[56].content :
            matrice_list[48] = 75
            matrice_list[57] = 75
        if color == table.board[63].content :
            matrice_list[55] = 75
            matrice_list[62] = 75
       
        if color == table.board[1].content:
            step = 1
            while matrice_list[step] != 100 and matrice_list[step+1]<len(matrice_list):
                if matrice_list[step] == 75 and color == table.board[step].content:
                    matrice_list[step+1] = 75
                step +=1
       
        if color == table.board[57].content:
            step = 57
            while matrice_list[step] != 100 and matrice_list[step+1]<len(matrice_list):
                if matrice_list[step] == 75 and color == table.board[step].content:
                    matrice_list[step+1] = 75
                step +=1
       
        #Pas de 8
               
        if color == table.board[8].content:
            step = 8
            while matrice_list[step+8] != 100 and matrice_list[step+1]<len(matrice_list):
                if matrice_list[step] == 75 and color == table.board[step].content:
                    matrice_list[step+8] = 75
                step +=8
       
        if color == table.board[15].content:
            step = 15
            while matrice_list[step+8] != 100 and matrice_list[step+1]<len(matrice_list):
                if matrice_list[step] == 75 and color == table.board[step].content:
                    matrice_list[step+8] = 75
                step +=8


        #Pas de -1
               
        if color == table.board[6].content:
            step = 6
            while matrice_list[step] != 100 and matrice_list[step+1]>0:
                if matrice_list[step] == 75 and color == table.board[step].content:
                    if step-1 >0:
                        matrice_list[step-1] = 75
                step -=1


        #Pas de -8
               
        if color == table.board[48].content:
            step = 48
            while matrice_list[step] != 100 and matrice_list[step+1]>0:
                if matrice_list[step] == 75 and color == table.board[step].content:
                    if step-8 >0:
                        matrice_list[step-8] = 75
                step -=8
       
        if color == table.board[55].content:
            step = 55
            while matrice_list[step] != 100 and matrice_list[step+1]>0:
                if matrice_list[step] == 75 and color == table.board[step].content:
                    if step-8 >0:
                        matrice_list[step-8] = 75
                step -=8


       
        for index in range(len(table.board)):                
            if table.board[index].content != 'X':
                table.board[index].content = matrice_list[index]
        return matrice_list


def play_games(number_of_games):
    white_victories = 0
    black_victories = 0
    white_win_icons = ""
    black_win_icons = ""
    
    for current_game in range(number_of_games):

        timeout = time.time() + 0.6

        # Create a new board & a new game instances
        othello_board = Board(8)
        othello_game = Game()

        # Fill the board with tiles
        othello_board.create_board()

        # Draw the board
        othello_board.draw_board("Content")

        # Create 2 bots
        benderBot = Xx_Bender_Destroyer_30_xX()
        babaa = concurent()

        # Loop until the game is over


        while not othello_game.is_game_over:

            if(time.time() > timeout):
                othello_game.check_for_winner()
                othello_game.is_game_over = True
                print("Player " + othello_game.active_player + " caused a Timeout")
                break

            # First player / bot logic goes here
            if (othello_game.active_player == "⚫"):
                move_coordinates = babaa.check_valid_moves_test(othello_board, othello_game, 1)
                othello_game.place_pawn(move_coordinates[0], move_coordinates[1], othello_board, othello_game.active_player)

            # Second player / bot logic goes here
            else:
                move_coordinates = benderBot.check_valid_moves(othello_board, othello_game)
                othello_game.place_pawn(move_coordinates[0], move_coordinates[1], othello_board, othello_game.active_player)
    
        if(othello_game.winner == "⚫"):
            black_win_icons += "⚫"
            black_victories += 1
        elif(othello_game.winner == "⚪"):
            white_win_icons += "⚪"
            white_victories += 1
        
        print(black_win_icons)
        print(white_win_icons)
        
    
    print("End of the games, showing scores: ")
    print("Black player won " + str(black_victories) + " times")
    print("White player won " + str(white_victories) + " times")
        

play_games(100)
