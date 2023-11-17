import random
import json
import matplotlib.pyplot as plt
import numpy as np

def create_grid(n):
    grid = np.zeros((n, n))
    print(grid)
    return grid

def visualize_grid(x,y):
     print(x,y)
     plt.plot(x,y, 'o')
    #  fig, ax = plt.subplots()
    #  ax.imshow(grid, cmap='gray')
    # #  ax.grid(True)  # Enable grid lines
    # #  plt.show()
    #  print(snake_positions)
    #  for s in snake_positions:
    #    draw_snake(ax, s, snake_positions[s], grid.shape[0])
    # #  ax.grid(True)  # Enable grid lines
     plt.show()

def draw_snake(ax, start, end, grid_size):
    ax.plot([start % grid_size, end % grid_size], [grid_size - 1 - start // grid_size, grid_size - 1 - end // grid_size], color='red', linewidth=2)

# Define the number of snakes and ladders and their positions
# num_snakes = int(input("Enter the number of snakes: "))
# num_ladders = int(input("Enter the number of ladders: "))

# Initialize snake and ladder positions
snake_positions = {}
ladder_positions = {}

# for _ in range(num_snakes):
#     start, end = map(int, input("Enter the snake's start and end positions (space-separated): ").split())
#     snake_positions[start] = end

# for _ in range(num_ladders):
#     start, end = map(int, input("Enter the ladder's start and end positions (space-separated): ").split())
#     ladder_positions[start] = end

def roll_dice():
    return random.randint(1, 6)

print(snake_positions)
print(ladder_positions)
n = int(input("Enter the grid size (n x n): "))
# p = int(input("Enter No of player"))
# grid = create_grid(n)
xpoints = np.arange(int(n))
print(xpoints)
ypoints = np.arange(int(n))
visualize_grid(xpoints, ypoints)
