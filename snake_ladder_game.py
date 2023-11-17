import random
import json
import os
from datetime import datetime
import sys

moves_history_file = "moves_history.txt"
game_content = "game_states.json"
game_record = "game_records.json"


# Invalid number of player exception
class InvalidNumberOfPlayers(Exception):
    def __init__(self, message):
        super().__init__(message)


# Invalid snake position exception
class InvalidSnakePositionError(Exception):
    def __init__(self, message):
        super().__init__(message)


# Invalid ladder position exception
class InvalidLadderPositionError(Exception):
    def __init__(self, message):
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
        self._grid_size = 0
        self._num_players = 0
        self._players = []
        self._snakes = {}
        self._ladders = {}
        self._board = []
        self._player_positions = {}
        self._game_loaded = False
        self._dice_rolls = 0

    # Method for showing game menu
    def game_menu(self):
        if os.path.exists(game_content):
            try:
                with open(game_content, "r") as file:
                    game_state = json.load(file)
                # Check if the content has the required keys
                if all(
                    key in game_state
                    for key in [
                        "grid_size",
                        "num_players",
                        "players",
                        "snakes",
                        "ladders",
                        "player_positions",
                    ]
                ):
                    gameload = input(
                        "!! ======== Welcome to Snakes and Ladders ======== !! \n"
                        "Do you want to: \n"
                        "1. Resume a saved game (Press 1 and enter)\n"
                        "2. Start a new game (Press 2 and enter)\n"
                        "3. Quit the game (Press 3 and enter)\n"
                        "Enter your choice: "
                    )
                    if gameload == "1":
                        print("Loading the saved game...")
                        self.load_game_state()
                        self._game_loaded = True
                        print("Game successfully loaded. Let's continue!")
                        self.play_game()
                        return
                    elif gameload == "2":
                        print("====================================")
                        print("Starting a new game. Good luck!")
                        self.configure_game()
                        self.play_game()
                    elif gameload == "3":
                        print("You have chosen to quit the game. Goodbye!")
                        sys.exit()
                    else:
                        print("Please choose a valid option (1 or 2).")
                        self.game_menu()
                else:
                    print(
                        "Game was not saved properly. Starting a new game. Good luck!"
                    )
                    self.configure_game()
                    self.play_game()
            except json.JSONDecodeError:
                gameload = input(
                    "!! ======== Welcome to Snakes and Ladders ======== !! \n"
                    "No saved game found. Do you want to \n"
                    "1. Start a new game (Press 1 and enter)\n"
                    "2. Quit the game (Press 2 to Quit) "
                )
                if gameload == "1":
                    print("Starting a new game. Good luck!")
                    self.configure_game()
                    self.play_game()
                else:
                    print("You have chosen to quit the game. Goodbye!")
                    sys.exit()
        else:
            gameload = input(
                "!! ======== Welcome to Snakes and Ladders ======== !! \n"
                "No saved game found. Do you want to \n"
                "1. Start a new game (Press 1 and enter)\n"
                "2. Quit the game (Press 2 to Quit) "
            )
            if gameload == "1":
                print("Starting a new game. Good luck!")
                self.configure_game()
            else:
                print("You have chosen to quit the game. Goodbye!")
                sys.exit()

    # Method for Configuring game settings by taking input from the user
    def configure_game(self):
        try:
            # Initialize game board & player
            self._grid_size = int(input("Enter the size of the playing grid (n x n): "))
            if self._grid_size <= 0:
                raise ValueError("Please enter a positive integer.")
            self._num_players = int(input("Enter the number of players (2, 3, or 4): "))
            if self._num_players < 2:
                raise InvalidNumberOfPlayers("At least 2 players are needed.")
            # Initialize players
            self._players = [Player(f"Player {i+1}") for i in range(self._num_players)]

            # Initialize snakes
            num_snakes = int(input("Enter the number of snakes: "))
            for ns in range(num_snakes):
                start = int(
                    input(f"Enter the starting position of the {ns + 1} snake: ")
                )
                end = int(input(f"Enter the ending position of the {ns + 1} snake: "))
                if not start > end:
                    raise InvalidSnakePositionError(
                        "Start should be more than end position"
                    )
                elif (
                    start > self._grid_size * self._grid_size
                    or end > self._grid_size * self._grid_size
                ):
                    raise InvalidLadderPositionError(
                        f"Position can't exceed grid's size {self._grid_size * self._grid_size}"
                    )
                self._snakes[start] = end

            # Initialize ladders
            num_ladders = int(input("Enter the number of ladders: "))
            for nl in range(num_ladders):
                start = int(
                    input(f"Enter the starting position of the {nl + 1} ladder: ")
                )
                end = int(input(f"Enter the ending position of the {nl + 1} ladder: "))
                if not (start < end):
                    raise InvalidLadderPositionError(
                        "Start should be less than end position"
                    )
                elif (
                    start > self._grid_size * self._grid_size
                    or end > self._grid_size * self._grid_size
                ):
                    raise InvalidLadderPositionError(
                        f"Position can't exceed grid's size {self._grid_size * self._grid_size}"
                    )
                self._ladders[start] = end

            # Initialize the game board
            self._board = []
            for i in range(self._grid_size):
                row = [0] * self._grid_size
                self._board.append(row)
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
        except ValueError:
            print("Invalid input. Please enter a positive integer.")
            print("Starting the game again")
            self.game_menu()
        except KeyboardInterrupt:
            print("\nProgram interrupted! Stopping the game...")
            sys.exit()
        except:
            print(f"An unexpected exception occurred: Please enter valid input")
            print("Starting the game again!")
            self.game_menu()

    # Method for playing the game
    def play_game(self):
        print("Game Started!")
        if self._game_loaded:
            self.show_game_state()
        while True:
            for player in self._players:
                key = input(
                    f"\n{player.name}'s turn now!\n"
                    "1. Press Enter to roll the dice...\n"
                    "2. Press '2' to save and quit the game: \n"
                    "3. Press '3' to quit the game: \n"
                    "Enter your choice: "
                )

                if key == "2":
                    print("Saving game...")
                    self.save_game_state()
                    print("Game saved. Exiting.")
                    return
                elif key == "3":
                    print("You have chosen to quit the game. Goodbye!")
                    sys.exit()
                dice_roll = random.randint(1, 6)
                self._dice_rolls += 1
                print("==========================")
                print(f"{player.name} rolled a {dice_roll}.")

                # Move the player
                current_position = self.move_player(player, dice_roll)
                print(f"{player.name} is now at position {current_position}.")
                print("==========================")
                # Check for snakes and ladders
                current_position = self.check_snakes_and_ladders(
                    player, current_position, dice_roll
                )
                # Check for win condition
                if current_position == self._grid_size * self._grid_size:
                    print(f"{player.name} has won!")
                    self.record_game(player.name)
                    print("Game has been recored successfully")
                    with open(game_content, "w") as file:
                        file.truncate()
                    return
                else:
                    print(
                        f"To win, you need to land on position {self._grid_size * self._grid_size}. Keep going!"
                    )

    # Method to record a move in the text file
    def record_move(self, player, dice_roll, current_position, final_position, move_type):
        try:
            timestamp = datetime.now().isoformat()
            move_details = f"{timestamp}: {player.name} rolled a {dice_roll}, Moved from {current_position} to {final_position}, Move type : {move_type}\n"
            with open(moves_history_file, "a") as file:
                file.write(move_details)
        except Exception as e:
            print(f"An error occurred while recording the move: {e}")
        
    # Method to show game state after resuming
    def show_game_state(self):
        print("===========================")
        print("Here is the state of your saved game")
        print(f"Game Grid Size: {self._grid_size}, Total Players: {len(self._players)}")
        print("---- Current Postions---- ")
        for player in self._players:
            if player.name in self._player_positions:
                print(
                    f"{player.name} is now at position {self._player_positions[player.name]}."
                )
            else:
                print(f"{player.name} has not moved yet.")
        print("---- Snakes -----")
        for snake in self._snakes:
            print(f"Snake at {snake} leads to {self._snakes[snake]}")
        print("---- Ladders---- ")
        for ladder in self._ladders:
            print(f"Ladder at {ladder} leads to {self._ladders[ladder]}")

    # Method to move the player on the board based on dice roll
    def move_player(self, player, steps):
        if self._player_positions and player.name in self._player_positions:
            newstate = self._player_positions[player.name] + steps
            # If step is more than grid's size then it will be discarded
            if newstate > self._grid_size * self._grid_size:
                print(
                    f"Oops! Your move {newstate} exceeds the grid size {self._grid_size * self._grid_size}. You need to land exactly on the final position. Try again."
                )
                return self._player_positions[player.name]
            self.record_move(player, steps, self._player_positions[player.name], newstate, "Normal Dice")
            self._player_positions[player.name] = newstate
            return self._player_positions[player.name]
        else:
            # If step is more than grid's size then it will be discarded
            if steps > self._grid_size * self._grid_size:
                print(
                    f"Oops! Your move {steps} exceeds the grid size {self._grid_size * self._grid_size}. You need to land exactly on the final position. Try again."
                )
                return self._player_positions[player.name]
            self._player_positions[player.name] = steps
            return self._player_positions[player.name]

    # Method to check if the player landed on a snake or ladder
    def check_snakes_and_ladders(self, player, position, steps):
        if position in self._snakes:
            print(f"Oops! Snake found at {position}")
            self.record_move(player, steps, self._player_positions[player.name], self._snakes[position], "Snake")
            self._player_positions[player.name] = self._snakes[position]
            print(f"{player.name} is now at position {self._snakes[position]}.")
            return self._snakes[position]

        elif position in self._ladders:
            print(f"Wow! Ladder found at {position}")
            self.record_move(player, steps, self._player_positions[player.name], self._ladders[position], "Ladder")
            self._player_positions[player.name] = self._ladders[position]
            print(f"{player.name} is now at position {self._ladders[position]}.")
            return self._ladders[position]
        return position

    # Method for saving game state
    def save_game_state(self, filename=game_content):
        game_state = {
            "grid_size": self._grid_size,
            "num_players": self._num_players,
            "players": [player.name for player in self._players],
            "snakes": self._snakes,
            "ladders": self._ladders,
            "player_positions": self._player_positions,
            "dice_rolls": self._dice_rolls,
        }

        with open(game_content, "w") as file:
            json.dump(game_state, file)

    # Method for loading saved game state
    def load_game_state(self, filename=game_content):
        try:
            with open(filename, "r") as file:
                game_state = json.load(file)

            self._grid_size = game_state["grid_size"]
            self._num_players = game_state["num_players"]
            self._players = [Player(name) for name in game_state["players"]]
            self._snakes = game_state["snakes"]
            self._ladders = game_state["ladders"]
            self._player_positions = game_state["player_positions"]
            self._dice_rolls = game_state["dice_rolls"]
        except FileNotFoundError:
            print(f"Error: The file {filename} does not exist.")
        except json.JSONDecodeError:
            print(f"Error: Failed to decode JSON in {filename}.")

    # Method for recording every game
    def record_game(self, winning_player):
        record = {
            "timestamp": datetime.now().isoformat(),
            "players": [{"name": player.name} for player in self._players],
            "dice_rolls": self._dice_rolls,
            "snakes": self._snakes,
            "ladders": self._ladders,
            "winning_player": winning_player,
        }
        try:
            with open(game_record, "r") as file:
                records = json.load(file)
        except (json.JSONDecodeError, FileNotFoundError):
            records = []

        # Append the new record
        records.append(record)
        # Save the updated records
        with open("game_records.json", "w") as file:
            json.dump(records, file, indent=2)


game = SnakesAndLaddersGame()
game.game_menu()
