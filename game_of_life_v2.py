import copy
import numpy as np
from numpy.random import default_rng
import matplotlib.pyplot as plt
import matplotlib.animation as ani
import matplotlib;


#Has to be used on my system as the animation does not otherwise work.
matplotlib.use("TkAgg")


#This function  is from the course Classical Simulation methods in physics, exercise example etching.py
#Used to draw the board at each generation.
def draw(frame, history):
    plt.clf()
    plt.pcolormesh(history[frame], cmap='Greys')

#This function  is from the course Classical Simulation methods in physics, exercise example etching.py
#Animate the game of life by drawing consecutive frames and save the animation.
#Additionally, the function saves the animation to mp4.
def animate(history):
    nframes = len(history)
    fig = plt.figure()
    motion = ani.FuncAnimation(fig, draw, nframes, interval = 1, fargs=(history,))

    writervideo = ani.FFMpegWriter(fps=5)
    #The program really should automatically generate a filename with relevant information. Oh well.
    motion.save("simulation.mp4", writer=writervideo)

    plt.show()




#Create an empty board, full of dead cells.
def create_board(size: int = 100):
    board = np.zeros((size, size))

    return board


# Make each cell on the board alive, depending on the probability given. The probability must be
# between 0 and 1 :). I'm not going to check if the values are legitimate.
def populate_board(board, probability):
    # Get dimensions of board.
    size = board.shape

    # Go through each cell and make it alive according to the probability.
    for i in range(0, size[0]):

        for j in range(0, size[1]):

            # Roll a number 0 <= x < 1
            random_roll = np.random.rand()
            # If the probability is high, the roll is lower than  the probability more often.
            if random_roll <= probability:
                board[i, j] = 1



#The board is connected at the sides, meaning the leftmost element is connected to rightmost element and so forth.
#The neighbourhood considered is the Moore-neighbourhood.
def get_live_neighbour_count_Moore(board, x, y):
    size = board.shape

    #x_below and x_above mean the indices that are lower and higher respectively. Visually, x_below is above the element.
    x_below = x - 1
    x_above = x + 1

    y_left = y - 1
    y_right = y + 1

    #If index too far above, look at the bottom side.
    if x_below < 0:
        x_below = size[0] - 1

    #If index too far below, look at the top side.
    if x_above > size[0] - 1:
        x_above = 0


    #If index too far left, look at the right side.
    if y_left < 0:
        y_left = size[1] - 1

    #If index too far right, look at the left side.
    if y_right > size[1] - 1:
        y_right = 0

    neighbours = 0

    #Check above
    neighbours += board[x_above, y_left]
    neighbours += board[x_above, y]
    neighbours += board[x_above, y_right]

    #Check adjacent
    neighbours += board[x, y_left]
    neighbours += board[x, y_right]

    #Check below
    neighbours += board[x_below, y_left]
    neighbours += board[x_below, y]
    neighbours += board[x_below, y_right]

    return neighbours


#Counts the number of live cells on the board.
def get_live_cells(board):

    size = board.shape

    live_cells = 0

    for i in range(size[0]):
        for j in range(size[1]):
            if board[i,j] == 1:
                live_cells += 1

    return live_cells



#A well studied seed that dies after a few generations.
def die_hard(board):

    size = board.shape

    #Get the middle of the board.
    x = size[0] // 2
    y = size[1] // 2

    board[x, y] = 1

    board[x + 2, y] = 1

    board[x + 2, y - 1] = 1
    board[x + 2, y + 1] = 1

    board[x + 1, y - 5] = 1

    board[x + 1, y - 6] = 1

    board[x + 2, y - 5] = 1



#A methuselah for generating a well studied initial seed.
def r_pentomino(board):

    size = board.shape


    center_x = size[0] // 2
    center_y = size[1] // 2

    board[center_x, center_y] = 1

    board[center_x - 1, center_y] = 1
    board[center_x + 1, center_y] = 1

    board[center_x, center_y - 1] = 1

    board[center_x - 1, center_y + 1] = 1



#A methuselah for showing a well studied initial seed.
def acorn(board):
    size = board.shape

    center_x = size[0] // 2
    center_y = size[1] // 2

    board[center_x, center_y] = 1

    board[center_x -1 , center_y - 2] = 1

    board[center_x + 1, center_y + 1] = 1
    board[center_x + 1, center_y + 2] = 1
    board[center_x + 1, center_y + 3] = 1

    board[center_x + 1, center_y -2] = 1
    board[center_x +1, center_y -3] = 1


def thunderbird(board):
    size = board.shape

    x = size[0] // 2
    y = size[1] // 2

    board[x,y] = 1
    board[x, y+ 1] = 1
    board[x, y -1] = 1

    board[x+2, y] = 1
    board[x+3, y] = 1
    board[x+4,y] = 1

def queen_bee(board):

    size = board.shape

    x = size[0] // 2
    y = size[1] // 2

    board[x,y] = 1

    board[x-1,y-1] = 1
    board[x+1,y-1] = 1

    board[x-2,y-2] = 1
    board[x+2,y-2] = 1

    board[x-1,y-3] = 1
    board[x+1,y-3] = 1

    board[x+3,y-4] = 1
    board[x - 3,y- 4] = 1

    board[x-2,y-4] = 1
    board[x + 2, y-4] = 1

    board[x, y-3] = 1



def queen_bee_with_gliders(board):

    size = board.shape

    x = size[0] // 2
    y = size[1] // 2

    #Setup for bee
    board[x,y] = 1

    board[x-1,y-1] = 1
    board[x+1,y-1] = 1

    board[x-2,y-2] = 1
    board[x+2,y-2] = 1

    board[x-1,y-3] = 1
    board[x+1,y-3] = 1

    board[x+3,y-4] = 1
    board[x - 3,y- 4] = 1

    board[x-2,y-4] = 1
    board[x + 2, y-4] = 1

    board[x, y-3] = 1


    #Gliders

    #First glider
    board[x-7,y-3] = 1
    board[x-5,y-3] = 1
    board[x-5,y-2] = 1
    board[x-6,y-2] = 1
    board[x-6,y-1] = 1


    #Second glider

    board[x+1,y+4] = 1
    board[x+1,y+5] = 1
    board[x+3,y+5] = 1
    board[x+2,y+4] = 1
    board[x+2,y+3] = 1





#Update the board according to the rules of Game of Life.
def update_board_moore(board):
    #Get board dimensions
    size = board.shape


    #Create a copy of the board to manipulate.
    updated_board = copy.deepcopy(board)

    #Go through each element on the board.
    for i in range(0, size[0]):
        for j in range(0, size[1]):

            #Get the amount of live neighbours for the cell.
            alive_neighbours = get_live_neighbour_count_Moore(board, i, j)

            #If a live cells has less than two live neighbours, it dies.
            if board[i, j] == 1 and alive_neighbours < 2:
                updated_board[i, j] = 0


            #If the cell is alive and has 2-3 live neighbours, it lives.
            elif board[i, j] == 1 and 2 <= alive_neighbours <= 3:
                updated_board[i, j] = 1


            #If the cell is alive and more than 3 live neighbours, it dies.
            elif board[i, j] == 1 and alive_neighbours > 3:
                updated_board[i, j] = 0


            #If the cell is dead and has exactly 3 live neighbours, it becomes alive.
            elif board[i, j] == 0 and alive_neighbours == 3:
                updated_board[i, j] = 1

    return updated_board


#Otherwise the same as the deterministic version, except each change has a probability to be ignored.
#The probability is given with the threshold parameter.

def update_board_moore_probabilistic(board, threshold):

    size = board.shape

    updated_board = copy.deepcopy(board)

    for i in range(0, size[0]):
        for j in range(0, size[1]):

            random_roll = np.random.rand()

            alive_neighbours = get_live_neighbour_count_Moore(board, i, j)

            #Check if the action for the cell is be done.
            if random_roll > threshold:


                #This whole logic branch should be done by calling the update_board_moore()-method.
                if board[i, j] == 1 and alive_neighbours < 2:

                    updated_board[i, j] = 0


                elif board[i, j] == 1 and 2 <= alive_neighbours <= 3:


                    updated_board[i, j] = 1


                elif board[i, j] == 1 and alive_neighbours > 3:


                    updated_board[i, j] = 0


                elif board[i, j] == 0 and alive_neighbours == 3:


                    updated_board[i, j] = 1

    return updated_board




def main(size: int, probability: float, generations: int, deterministic: bool, threshold: float ):


    # Create a board full of dead cells.
    board = create_board(size)

    #Create list that holds the generation number.
    generation = np.arange(0, generations)

    # States to draw.
    history = [board]



    #Create an array that holds the amount of live cells per generation.
    alive_cells = np.array([])

# ==========================================================================================================
    #IF YOU WANT TO USE PREDEFINED SEEDS INSTEAD GENERATING A RANDOM ONE, COMMENT OUT populate_board()  # |
    #AND UNCOMMENT ONE OF THE METHUSELAHS                                                               # |
# =========================================================================================================


    #Generate a new initial state for the board.
    populate_board(board, probability)

    # METHUSHELAHS
    #r_pentomino(board)
    #acorn(board)
    #thunderbird(board)
    #die_hard(board)
    #queen_bee(board)
    #queen_bee_with_gliders(board)

    #Calculate the number of live cells on the board.
    live_cells_on_board = get_live_cells(board)

    #Add the amount of live cells
    alive_cells = np.append(alive_cells, live_cells_on_board)

    #Save the first 0th generation to animate.
    history.append(copy.deepcopy(board))


    #Checks if using the deterministic or probabilistic updater.
    if deterministic:
        updated_board = update_board_moore(board)

    else:
        updated_board = update_board_moore_probabilistic(board, threshold)


    for i in range(1,generations):

        #Add a frame to animate
        history.append(copy.deepcopy(updated_board))

        # Checks if using the deterministic or probabilistic updater.
        if deterministic:
            updated_board = update_board_moore(updated_board)
        else:
            updated_board = update_board_moore_probabilistic(updated_board, threshold)


        #Add to array current generations live cell count.
        live_cells_on_board = get_live_cells(updated_board)
        alive_cells = np.append(alive_cells, live_cells_on_board)




    #Plot the simulation.
    plt.xlabel("Generation")
    plt.ylabel("Live cells")
    plt.plot(generation, alive_cells)

    #Animate the simulation.
    animate(history)



if __name__ == "__main__":
    # edit the main function call to adjust simulation behaviour
    # 1st parameter changes grid size.
    # 2nd parameter changes initial probability of cell being alive when the board is initialized.
    # 3rd parameter changes the amount of generations the simulation runs for.
    # 4th parameter chooses whether the deterministic or probabilistic simulation is used. True for deterministic.
    # 5th parameter chooses the probabilty at which a rule is ignored if using the probabilistic update.

    main(100, 0.5, 500, True, 0.5)


