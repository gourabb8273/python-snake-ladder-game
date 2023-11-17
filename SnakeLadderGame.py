import matplotlib.pyplot as plt
import seaborn as sns
import random
import json
import os
from datetime import datetime
import sys

game_content = "game_state.json"

# Invalid number of player exception 
class InvalidNumberOfPlayers(Exception):
     def __init__(self,message):  
        super().__init__(message)

# Invalid snake position exception 
class InvalidSnakePositionError(Exception):
    def __init__(self,message):
        super().__init__(message)

# Invalid ladder position exception 
class InvalidLadderPositionError(Exception):
    def __init__(self,message):
        super().__init__(message)

# Player initialization 
class Player:
    def __init__(self, name):
        self.name = name

 # Snake initialization
class Snake:
    def __init__(self, start, end):
        self.start = start
        self.end = end

# Ladder initialization
class Ladder:
    def __init__(self, start, end):
        self.start = start
        self.end = end

# Snake and Ladder game initialization
class SnakesAndLaddersGame:
    def __init__(self):
        self.grid_size = 0
        self.num_players = 0
        self.players = []
        self.snakes = {}
        self.ladders = {}
        self.board = []
        self.player_positions = {}
        self.game_loaded = False
        self.dice_rolls = 0 

    # Showing game menu
    def game_menu(self):
        if os.path.exists(game_content):
            try:
                with open(game_content, 'r') as file:
                  game_state = json.load(file)
                # Check if the content has the required keys
                if all(key in game_state for key in ['grid_size', 'num_players', 'players', 'snakes', 'ladders', 'player_positions']):
                    gameload = input("!! ======== Welcome to Snakes and Ladders ======== !! \n"
                                    "Do you want to: \n"
                                    "1. Resume a saved game (Press 1 and enter)\n"
                                    "2. Start a new game (Press 2 and enter)\n"
                                    "3. Quit the game (Press 3 and enter)\n"
                                    "Enter your choice: ")
                    if(gameload == '1'):
                        print("Loading the saved game...")
                        self.load_game_state()
                        self.game_loaded = True
                        print("Game successfully loaded. Let's continue!")
                        self.play_game()
                        return
                    elif(gameload == '2'):
                        print("====================================")
                        print("Starting a new game. Good luck!")
                        self.configure_game()
                        self.play_game()
                    elif(gameload == '3'):
                        print("You have chosen to quit the game. Goodbye!")
                        sys.exit()
                    else:
                        print("Please choose a valid option (1 or 2).")
                        self.game_menu()
                else:
                    print("Game was not saved properly. Starting a new game. Good luck!")
                    self.configure_game()
                    self.play_game()
            except json.JSONDecodeError:
             gameload = input("!! ======== Welcome to Snakes and Ladders ======== !! \n"
                                    "No saved game found. Do you want to \n"
                                    "1. Start a new game (Press 1 and enter)\n"
                                    "2. Quit the game (Press 2 to Quit) ")
             if(gameload== '1'):
                    print("Starting a new game. Good luck!")
                    self.configure_game()
                    self.play_game()
             else:
                 print("You have chosen to quit the game. Goodbye!")
                 sys.exit()
        else:
             gameload = input("!! ======== Welcome to Snakes and Ladders ======== !! \n"
                                    "No saved game found. Do you want to \n"
                                    "1. Start a new game (Press 1 and enter)\n"
                                    "2. Quit the game (Press 2 to Quit) ")
             if(gameload== '1'):
                    print("Starting a new game. Good luck!")
                    self.configure_game()
             else:
                 print("You have chosen to quit the game. Goodbye!")
                 sys.exit()

    # Configuring game settings by taking input from the user
    def configure_game(self):
        try:
            # Initialize game board & player
            self.grid_size = int(input("Enter the size of the playing grid (n x n): "))
            self.num_players = int(input("Enter the number of players (2, 3, or 4): "))
            if self.num_players < 2:
                raise InvalidNumberOfPlayers("At least 2 players are needed.")

            # Initialize players
            self.players = [Player(f"Player {i+1}") for i in range(self.num_players)]

            # Initialize snakes
            num_snakes = int(input("Enter the number of snakes: "))
            for ns in range(num_snakes):
                start = int(input(f"Enter the starting position of the {ns + 1} snake: "))
                end = int(input(f"Enter the ending position of the {ns + 1} snake: "))
                if(not start>end):
                    raise InvalidSnakePositionError("Start should be more than end position")
                self.snakes[start] = end

            # Initialize ladders
            num_ladders = int(input("Enter the number of ladders: "))
            for nl in range(num_ladders):
                start = int(input(f"Enter the starting position of the {nl + 1} ladder: "))
                end = int(input(f"Enter the ending position of the {nl + 1} ladder: "))
                if not (start<end):
                    raise InvalidLadderPositionError("Start should be less than end position")
                self.ladders[start] = end

            # Initialize the game board
            self.board = []
            for i in range(self.grid_size):
                row = [0] * self.grid_size
                self.board.append(row)
        except InvalidNumberOfPlayers as e:
            print(f"You have entered an invalid number of players: {e}")
            print("Starting the game again")
            self.game_menu()
        except InvalidSnakePositionError as e:
            print(f"You have entered an invalid snake position: {e}")
            print("Starting the game again")
            self.game_menu()
        except InvalidLadderPositionError as e:
            print(f"You have entered an invalid ladder position: {e}")
            print("Starting the game again")
            self.game_menu()
        except:
            print(f"An unexpected exception occurred: Please enter valid input")
            print("Starting the game again!")
            self.game_menu()
        

    def play_game(self):
            print("Game Started!")
            if(self.game_loaded):
                self.show_game_state()
            while True:
                for player in self.players:
                    key = input(f"\n{player.name}'s turn now!\n"
                                 "1. Press Enter to roll the dice...\n"
                                 "2. Press '2' to save and quit the game: \n"
                                 "3. Press '3' to quit the game: \n"
                                 "Enter your choice: ")

                    if key == '2':
                        print("Saving game...")
                        self.save_game_state()
                        print("Game saved. Exiting.")
                        return
                    elif key == '3':
                        print("You have chosen to quit the game. Goodbye!")
                        sys.exit()
                    dice_roll = random.randint(1, 6)
                    self.dice_rolls +=1
                    print("==========================")
                    print(f"{player.name} rolled a {dice_roll}.")

                    # Move the player
                    current_position = self.move_player(player, dice_roll)
                    print(f"{player.name} is now at position {current_position}.")
                    print("==========================")
                    # Check for snakes and ladders
                    current_position = self.check_snakes_and_ladders(player, current_position)
                    # Check for win condition
                    if current_position == self.grid_size * self.grid_size:
                        print(f"{player.name} has won!")
                        self.record_game(player.name)
                        print("Game has been recored successfully")
                        with open(game_content, 'w') as file:
                             file.truncate()
                        return
                    else:
                        print(f"To win, you need to land on position {self.grid_size * self.grid_size}. Keep going!")
    # Show game state after resuming                
    def show_game_state(self):
            print("===========================")
            print("Here is the state of your saved game")
            print(f"Game Grid Size: {self.grid_size}, Total Players: {len(self.players)}")
            print("---- Current Postions---- ")
            for player in self.players:
                if player.name in self.player_positions:
                     print(f"{player.name} is now at position {self.player_positions[player.name]}.")
                else:
                     print(f"{player.name} has not moved yet.")
            print("---- Snakes -----")
            for snake in self.snakes:
                print(f"Snake at {snake} leads to {self.snakes[snake]}")
            print("---- Ladders---- ")
            for ladder in self.ladders:
                 print(f"Ladder at {ladder} leads to {self.ladders[ladder]}")   
    
   # Move the player on the board based on dice roll
    def move_player(self, player, steps):
            if self.player_positions and player.name in self.player_positions:
                newstate = self.player_positions[player.name] + steps
                # If step is more than grid's size then it will be discarded
                if newstate > self.grid_size * self.grid_size:
                    print(f"Oops! Your move {newstate} exceeds the grid size {self.grid_size * self.grid_size}. You need to land exactly on the final position. Try again.")
                    return self.player_positions[player.name]
                self.player_positions[player.name] = newstate
                return self.player_positions[player.name]
            else:
                # If step is more than grid's size then it will be discarded
                if steps > self.grid_size * self.grid_size:
                    print(f"Oops! Your move {steps} exceeds the grid size {self.grid_size * self.grid_size}. You need to land exactly on the final position. Try again.")
                    return self.player_positions[player.name]
                self.player_positions[player.name] = steps
                return self.player_positions[player.name]

    # Check if the player landed on a snake or ladder
    def check_snakes_and_ladders(self, player, position):
           if position in self.snakes:
            print(f"Oops! Snake found at {position}")
            self.player_positions[player.name] = self.snakes[position]
            print(f"{player.name} is now at position {self.snakes[position]}.")
            return self.snakes[position]

           elif position in self.ladders:
            print(f"Wow! Ladder found at {position}")
            self.player_positions[player.name] = self.ladders[position]
            print(f"{player.name} is now at position {self.ladders[position]}.")
            return self.ladders[position]
           return position
    
    # Saving game state
    def save_game_state(self, filename=game_content):
        game_state = {
            'grid_size': self.grid_size,
            'num_players': self.num_players,
            'players': [player.name for player in self.players],
            'snakes': self.snakes,
            'ladders': self.ladders,
            'player_positions': self.player_positions,
            'dice_rolls': self.dice_rolls 
        }

        with open(game_content, 'w') as file:
            json.dump(game_state, file)

    # Loading saved game state
    def load_game_state(self, filename=game_content):
        with open(filename, 'r') as file:
            game_state = json.load(file)

        self.grid_size = game_state['grid_size']
        self.num_players = game_state['num_players']
        self.players = [Player(name) for name in game_state['players']]
        self.snakes = game_state['snakes']
        self.ladders = game_state['ladders']
        self.player_positions = game_state['player_positions']
        self.dice_rolls =game_state['dice_rolls']

    # Recording all game
    def record_game(self, winning_player):
        record = {
            "timestamp": datetime.now().isoformat(),
            "players": [
                {"name": player.name} for player in self.players
            ],
            "dice_rolls": self.dice_rolls,
            "snakes": self.snakes,
            "ladders": self.ladders,
            "winning_player": winning_player
        }
        try:
            with open('game_records.json', 'r') as file:
                records = json.load(file)
        except (json.JSONDecodeError, FileNotFoundError):
            records = []

        # Append the new record
        records.append(record)
        # Save the updated records
        with open('game_records.json', 'w') as file:
            json.dump(records, file, indent=2)

game = SnakesAndLaddersGame()
game.game_menu()
