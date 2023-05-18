from tkinter import *
import random


GAME_WIDTH = 1000
GAME_HEIGHT = 700
SPEED = 60
SPACE_SIZE = 40
BODY_PARTS = 3
SNAKE_COLOR = "#00FF00"
FOOD_COLOR = "#FF0000"
BACKGROUND_COLOR = "#000000"


class Snake:
    def __init__(self):
        ''' intialize snake '''

        # initialize snakes
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []
        
        # list of coordinates of each body part of the snake
        for i in range(0, BODY_PARTS):
            self.coordinates.append([0,0])

        # generate said body parts
        for x,y in self.coordinates:
            square = canvas.create_rectangle(x, y, x+SPACE_SIZE, y+SPACE_SIZE, fill=SNAKE_COLOR, tag="snake")
            self.squares.append(square)


class Food:
    def __init__(self):
        ''' initialize food '''

        # randomize coordinates upon generation
        x = random.randint(0, int((GAME_WIDTH/SPACE_SIZE))-1) * SPACE_SIZE
        y = random.randint(0, int((GAME_HEIGHT/SPACE_SIZE))-1) * SPACE_SIZE

        # append these coordinates
        self.coordinates = [x,y]

        # generate food
        canvas.create_oval(x,y, x+SPACE_SIZE, y+SPACE_SIZE, fill=FOOD_COLOR, tag="food")

def next_turn(snake, food):
    ''' update snake's position when in motion '''
    x,y = snake.coordinates[0]

    # update new move
    if direction == "up":
        y-=SPACE_SIZE

    elif direction == "down":
        y+=SPACE_SIZE

    elif direction == "left":
        x-=SPACE_SIZE

    elif direction == "right":
        x+=SPACE_SIZE

    snake.coordinates.insert(0, (x,y))          # update new set of coordinates

    square = canvas.create_rectangle(x, y , x+SPACE_SIZE, y+SPACE_SIZE, fill=SNAKE_COLOR)         #   create new graphic for snake's position

    snake.squares.insert(0, square)         #   append the new position to snake's list of positions

    # snake position overlapping with food position
    if x ==food.coordinates[0] and y == food.coordinates[1]:     
        global score
        
        score+=1        # increment score

        label.config(text="Score: {}".format(score))

        canvas.delete("food")       # delete old food obj

        food = Food()           # generate new food object

    else:                           # delete body part other wise

        del snake.coordinates[-1]           # delete the last position of snake
        
        canvas.delete(snake.squares[-1])    # delete the graphic

        del snake.squares[-1]       # delete the square that the snake was in

    if check_collisions(snake):     # do we have a collision?
        game_over()         # end game
    
    else:
        window.after(SPEED, next_turn, snake, food)        # update next turn


def change_direction(new_direction):
    ''' change directions according to keybinds '''
    global direction

    if new_direction == "left":
        if direction != "right":
            direction = new_direction

    elif new_direction == "right":
        if direction != "left":
            direction = new_direction

    elif new_direction == "up":
        if direction != "down":
            direction = new_direction

    elif new_direction == "down":
        if direction != "up":
            direction = new_direction
            
def check_collisions(snake):
    ''' check if we had collided with anything  '''
    x,y = snake.coordinates[0]

    # border collision
    if x<0 or x>= GAME_WIDTH:
        return True
    
    elif y<0 or y>=GAME_HEIGHT:
        return True
    
    for body_part in snake.coordinates[1:]:
        
        # snake overlapping with itself
        if x== body_part[0] and y == body_part[1]:
            return True
        
    return False


def game_over():
    ''' terminate game  '''
    global score
    
    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/2, font=('times new roman', 70), text = "GAME OVER", fill="red", tag ="gameover")
    canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/2+(2*SPACE_SIZE), font=('times new roman', 60), text = f"Final Score: {score}", fill="#FFDEAD", tag ="finalscore")



def gen_game():
    ''' generate game   '''
    canvas.delete(ALL)
    
    # creation of game figures
    snake = Snake()
    food = Food()

    # set snake in motion
    next_turn(snake, food)
    

if __name__ == "__main__":
    
    # window creation
    window = Tk()
    window.title("Snake game")
    window.resizable(True, True)

    score = 0
    direction = 'down'

    label = Label(window, text="Score: {}".format(score), font=('times new roman', 40))
    label.pack()

    canvas = Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
    canvas.pack()

    window.update()

    window_width = window.winfo_width()
    window_height = window.winfo_height()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x= int((screen_width/2) - (window_width/2))
    y= int((screen_height/2) - (window_height/2))

    window.geometry(f"{window_width}x{window_height}+{x}+{y}")

    # bind keys to direciton
    window.bind('<Left>', lambda event: change_direction('left'))
    window.bind('<Right>', lambda event: change_direction('right'))
    window.bind('<Up>', lambda event: change_direction('up'))
    window.bind('<Down>', lambda event: change_direction('down'))
    window.bind('<Tab>', lambda event: gen_game())

    # first screen
    canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/2, font=('times new roman', 70), text = "Welcome!", fill="#FFDEAD", tag ="welcome")
    canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/2 + (2*SPACE_SIZE), font=('times new roman', 70), text = "Press Tab to start", fill="#FFDEAD", tag ="play")
    
    
    window.mainloop()
