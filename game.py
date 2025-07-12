import tkinter as tk
import random

# Create main window
window = tk.Tk()
window.title("Snake Game")

# Canvas size
canvas_width = 400
canvas_height = 400

# Create main frame
main_frame = tk.Frame(window)
main_frame.pack()

# Create canvas
canvas = tk.Canvas(main_frame, width=canvas_width, height=canvas_height, bg="black")
canvas.pack()

# Score label (below canvas)
score_var = tk.StringVar()
score_var.set("Score: 0")
score_label = tk.Label(main_frame, textvariable=score_var, font=("Arial", 14))
score_label.pack()

# Snake initial settings
snake_size = 20  # Each segment size
snake = [
    (200, 200),
    (180, 200),
    (160, 200)
]

# Draw snake
snake_rects = []
snake_length = len(snake)
for i, (x, y) in enumerate(snake):
    if i == 0:
        color = "blue"
    else:
        green_value = int(255 - (i / (snake_length - 1)) * 120) if snake_length > 1 else 255
        color = f"#00{green_value:02x}00"
    rect = canvas.create_rectangle(x, y, x + snake_size, y + snake_size, fill=color)
    snake_rects.append(rect)

# Snake movement direction (dx, dy)
direction = (20, 0)  # Start moving right

# Initial food
food = (random.randint(0, canvas_width - snake_size), random.randint(0, canvas_height - snake_size))
food_rect = canvas.create_rectangle(food[0], food[1], food[0]+snake_size, food[1]+snake_size, fill="red")

# Initial score
score = 0

# Handle keyboard events to change direction
def change_direction(event):
    global direction
    key = event.keysym
    if key == "Up" and direction != (0, 20):
        direction = (0, -20)
    elif key == "Down" and direction != (0, -20):
        direction = (0, 20)
    elif key == "Left" and direction != (20, 0):
        direction = (-20, 0)
    elif key == "Right" and direction != (-20, 0):
        direction = (20, 0)

# Bind keyboard events
window.bind("<Key>", change_direction)
window.focus_set()  # Focus window

def reset_game(event=None):
    global snake, snake_rects, food, food_rect, score, direction
    canvas.delete("all")
    # Reset snake
    snake = [
        (200, 200),
        (180, 200),
        (160, 200)
    ]
    snake_rects = []
    snake_length = len(snake)
    for i, (x, y) in enumerate(snake):
        if i == 0:
            color = "blue"
        else:
            green_value = int(255 - (i / (snake_length - 1)) * 120) if snake_length > 1 else 255
            color = f"#00{green_value:02x}00"
        rect = canvas.create_rectangle(x, y, x + snake_size, y + snake_size, fill=color)
        snake_rects.append(rect)
    # Reset score
    score = 0
    score_var.set("Score: 0")
    # Reset food
    food = random_food()
    food_rect = canvas.create_rectangle(food[0], food[1], food[0]+snake_size, food[1]+snake_size, fill="red")
    # Reset direction
    direction = (20, 0)
    # Bind keyboard
    window.bind("<Key>", change_direction)
    window.focus_set()
    # Start moving
    move_snake()

def game_over():
    global snake, snake_rects, food, food_rect, score, direction
    canvas.delete("all")
    canvas.create_text(canvas_width/2, canvas_height/2, text="Game Over!", fill="white", font=("Arial", 40))
    canvas.create_text(canvas_width/2, canvas_height/2 + 50, text=f"Your Score: {score}", fill="white", font=("Arial", 30))
    canvas.create_text(canvas_width/2, canvas_height/2 + 100, text="Press R to restart", fill="white", font=("Arial", 20))
    direction = (0, 0) # Stop moving
    window.bind("r", reset_game)  # Bind R to restart
    window.focus_set() # Focus window

def random_food():
    while True:
        fx = random.randrange(0, canvas_width, snake_size)
        fy = random.randrange(0, canvas_height, snake_size)
        if (fx, fy) not in snake:
            return (fx, fy)

def move_snake():
    global snake, snake_rects, food, food_rect, score
    if use_ai:
        ai_choose_direction()
    # Calculate new head
    head_x, head_y = snake[0]
    dx, dy = direction
    new_head_x = head_x + dx
    new_head_y = head_y + dy

    # Game over if hit wall
    if (new_head_x < 0 or new_head_x >= canvas_width or
        new_head_y < 0 or new_head_y >= canvas_height):
        game_over()
        return

    new_head = (new_head_x, new_head_y)

    # Game over if hit itself
    if new_head in snake:
        game_over()
        return

    # Eat food
    if new_head == food:
        snake = [new_head] + snake
        rect = canvas.create_rectangle(new_head[0], new_head[1], new_head[0]+snake_size, new_head[1]+snake_size, fill="blue")
        # Previous head becomes green (gradient)
        if len(snake_rects) > 0:
            snake_length = len(snake)
            for i in range(len(snake_rects)):
                green_value = int(255 - ((i+1) / (snake_length - 1)) * 120) if snake_length > 1 else 255
                color = f"#00{green_value:02x}00"
                canvas.itemconfig(snake_rects[i], fill=color)
        snake_rects = [rect] + snake_rects
        # New food
        food = random_food()
        canvas.coords(food_rect, food[0], food[1], food[0]+snake_size, food[1]+snake_size)
        # Update score
        score += 1
        score_var.set(f"Score: {score}")
    else:
        # Normal move
        snake = [new_head] + snake[:-1]
        for i, (x, y) in enumerate(snake):
            canvas.coords(snake_rects[i], x, y, x + snake_size, y + snake_size)
        # Update color: head blue, body green gradient
        if len(snake_rects) > 0:
            canvas.itemconfig(snake_rects[0], fill="blue")
            snake_length = len(snake)
            for i in range(1, len(snake_rects)):
                green_value = int(255 - (i / (snake_length - 1)) * 120) if snake_length > 1 else 255
                color = f"#00{green_value:02x}00"
                canvas.itemconfig(snake_rects[i], fill=color)
        # If snake gets shorter (didn't eat food), delete last rect
        if len(snake_rects) > len(snake):
            canvas.delete(snake_rects[-1])
            snake_rects.pop()

    window.after(100, move_snake)

# Simple AI (optional, set use_ai = True to enable)
use_ai = False  # Set to True for auto-play

def ai_choose_direction():
    global direction, snake, food
    head_x, head_y = snake[0]
    food_x, food_y = food
    # Simple greedy AI: move towards food
    if head_x < food_x and direction != (-20, 0):
        direction = (20, 0)
    elif head_x > food_x and direction != (20, 0):
        direction = (-20, 0)
    elif head_y < food_y and direction != (0, -20):
        direction = (0, 20)
    elif head_y > food_y and direction != (0, 20):
        direction = (0, -20)

# Start moving
move_snake()

# Main loop
window.mainloop()
