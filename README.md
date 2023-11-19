# Snakes and Ladders Game

## Overview

This project is an implementation of the classic Snakes and Ladders game in Python, adhering to Object-Oriented Programming principles. The game allows users to configure the grid size, the number of players, and the positions of snakes and ladders. It supports saving and loading game states, and recording game history.

## Features

- **Configurability:**
  - The size of the playing grid is configurable (nxn where n is the size of either dimension).
  - The number of snakes and ladders, along with their start and end points, is configurable.
  - The number of players is configurable (2, 3, or 4).

- **Save and Load Game State:**
  - Users can save the game state at any time and load it later.

- **Exception Handling:**
  - Proper exception handling is implemented to handle user inputs and potential errors.

- **OOPs Principles:**
  - Object-Oriented Programming principles are followed for a structured and modular codebase.

- **Encapsulation with Protected Variables:**
  - Protected variables (prefixed with a single underscore) are used within the classes to encapsulate internal state.

- **Game Moves Recording:**
  - All game moves are recorded in a text file.

- **Game History:**
  - Past game history is dumped in a file, and appropriate visuals can be created.

## Setup

1. **Install Python (Used version 3)**
1. **Clone the Repository:**
   ```bash
   git clone https://github.com/gourabb8273/python-snake-ladder-game.git
   cd python-snake-ladder-game
   python3 snake_ladder_game.py  (use python or python3 based on the system configuration)

## Files and Directories

- **`snakes_ladder_game.py`:** Main Python script containing the game implementation.

- **`game_states.json`:** File to store the current game state. This JSON file includes information about the current state of the game, such as the grid size, number of players, player positions, snakes, and ladders.

- **`game_records.json`:** File to store past game records. This JSON file keeps a record of each game played, including timestamps, player names, dice rolls, snakes, ladders, and the winning player.

- **`moves_history.txt`:** File to store the history of all game moves. This text file logs each move made during the game, including the player's name, dice roll, current and final positions, and any encounters with snakes or ladders.

