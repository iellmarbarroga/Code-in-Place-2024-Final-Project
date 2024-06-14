from tkinter import*
import time
import random


colors_option = ["skyblue", "coral", "palegreen", "lightgoldenrodyellow"]
balls = None
start_time = None
time_duration = 5

# canvas
WIDTH = 400
HEIGHT = 375
top_border_color = "skyblue"
bottom_border_color = "coral"
left_border_color = "palegreen"
right_border_color = "lightgoldenrodyellow"
border_thickness = 10

window = Tk()
window.geometry("800x475")
window.resizable(False, False)


canvas = Canvas(window, width=WIDTH, height=HEIGHT, bg="whitesmoke", bd=0, highlightthickness=0)

class Ball:
    def __init__(self, canvas, start_x, start_y, color, xVelocity, yVelocity, ball_size):
        self.canvas = canvas
        # attributes intended to be random
        self.start_x = start_x
        self.start_y = start_y
        self.xVelocity = xVelocity
        self.yVelocity = yVelocity
        # we will initialize the color to be black at first
        self.color = color
        self.ball_size = ball_size
        self.circ = canvas.create_oval(start_x, start_y, start_x + ball_size, start_y + ball_size, fill=color)

    def change_color(self):
        self.canvas.itemconfig(self.circ, fill=self.color)

    def move_ball(self):
        self.start_x += self.xVelocity
        self.start_y += self.yVelocity

        # this is a border check condition which changes the color when the ball hits a specific border
        # it also makes the ball bounce when they hit the wall
        self.location = (self.start_x, self.start_y)
        if self.location[0] >= (WIDTH - self.ball_size - border_thickness):  # right border
            self.xVelocity = -self.xVelocity
            self.color = right_border_color
            self.change_color()

        if self.location[0] < border_thickness:  # left border
            self.xVelocity = -self.xVelocity
            self.color = left_border_color
            self.change_color()

        if self.location[1] >= (HEIGHT - self.ball_size - border_thickness):  # bottom border
            self.yVelocity = -self.yVelocity
            self.color = bottom_border_color
            self.change_color()

        if self.location[1] < border_thickness:  # top border
            self.yVelocity = -self.yVelocity
            self.color = top_border_color
            self.change_color()

        self.canvas.move(self.circ, self.xVelocity, self.yVelocity)

def display_result(frame_result, results_dict, selected_option):
    # this function is triggered when the simulation ends.
    frame_result.place(x=500, y=150)  # calls the frame_result after the simulation

    label_result = Label(frame_result,
                         text=f"The resulting counts are the following:",
                         font=("Helvetica", 12))
    label_result.grid()
    max_count = max(results_dict.values())
    colors_with_max_count = [key for key, count in results_dict.items() if count == max_count]
    for color, count in results_dict.items():
        lb = Label(frame_result, text=f"{color}: {count}", )
        # makes the winning colors bold font
        if color in colors_with_max_count:
            lb.config(font=("Helvetica", 12, "bold"))
        else:
            lb.config(font=("Helvetica", 12))
        lb.grid()

    label_win_lose = Label(frame_result, font=("Helvetica", 12))
    label_win_lose.grid(row=5)

    if selected_option in colors_with_max_count:
        label_win_lose.config(text=f"\n\n You guessed right!")
    else:
        label_win_lose.config(text=f"\n\n You guessed wrong!")

def count_balls(ball_colors):
    dict = {}
    for color in ball_colors:
        if color not in dict.keys():
            dict[color] = 1
        else:
            dict[color] += 1
    return dict

def create_canvas():
    # this function recreates the canvas whenever the user initializes the num balls and size
    canvas.place(x=50, y=50)
    # Draw the top border
    canvas.create_line(0, 0, WIDTH, 0, fill=top_border_color, width=border_thickness)
    # Draw the bottom border
    canvas.create_line(0, HEIGHT, WIDTH, HEIGHT, fill=bottom_border_color, width=border_thickness)
    # Draw the left border
    canvas.create_line(0, 0, 0, HEIGHT, fill=left_border_color, width=border_thickness)
    # Draw the right border
    canvas.create_line(WIDTH, 0, WIDTH, HEIGHT, fill=right_border_color, width=border_thickness)

def main():
    create_canvas()
    # displays the elapsed time label
    label_time = Label(window, text="Elapsed Time: 0s", font=("Helvetica", 14))
    label_time.place(x=180, y=10)

    # the frame to initialize the balls size and number
    frame_set = Frame(window)
    frame_set.place(x=500, y=100)

    def set_init():
        frame_set.destroy()
        frame_ui.place(x=500, y=100)

    def update_config_balls(value):  # the value is the scale number
        global balls    # this is a global variable because the changes in this function would be used again
        canvas.delete('all') # deletes the canvas
        create_canvas() # restart the canvas to initialize size and num balls
        no_of_balls = int(scale_num.get())
        ball_size = int(scale_size.get())
        # calls many instances of Ball class
        balls = []
        for _ in range(no_of_balls):
            start_x = random.randint(border_thickness, WIDTH - ball_size - border_thickness)
            start_y = random.randint(border_thickness, HEIGHT - ball_size - border_thickness)
            xVelocity = random.choice([19, 8, 17, 5]) * random.choice([-1, 1])
            yVelocity = random.choice([9, 19, 8, 12]) * random.choice([-1, 1])

            ball = Ball(canvas, start_x, start_y, "white", xVelocity, yVelocity, ball_size)
            balls.append(ball)

        # this button is placed here so that it will appear when the scale is calibrated
        button_init = Button(frame_set, text="initialize config", command=set_init)
        button_init.grid(row=4, padx=20, pady=20)

    # this block of code is for initializing the num of balls and size
    scale_num = Scale(frame_set, from_=10, to=100, orient='horizontal', length=180, command=update_config_balls)
    scale_num.grid(row=0, pady=5)
    label_num_balls = Label(frame_set, text="Select number of balls", font=("Helvetica", 12))
    label_num_balls.grid(row=1)
    scale_size = Scale(frame_set, from_=10, to=50, orient='horizontal', length=180, command=update_config_balls)
    scale_size.grid(row=2, pady=5)
    label_size_balls = Label(frame_set, text="Select size of balls", font=("Helvetica", 12))
    label_size_balls.grid(row=3)



    # the frame will be the user interface
    frame_ui = Frame(window)

    # the frame will display the result
    frame_result = Frame(window)

    def start_timer():
        # we need to have this so that when we click start simulation, the timer is set
        global start_time
        start_time = time.time()
        selected_option = var.get()
        label_color = Label(window,
                            text=f"You picked {selected_option}.",
                            font=("Helvetica", 14))
        label_color.place(x=500, y=100)
        animate()

    def animate():
        # this function shows the every frame of move_ball() and then updates the canvas after
        global balls, start_time
        current_time = time.time()
        elapsed_time = current_time - start_time
        if elapsed_time < time_duration:  # Run for 60 seconds
            for ball in balls:
                ball.move_ball()
            # updates the time after 1 s
            label_time.config(text=f"Elapsed Time: {int(elapsed_time)}s")
            canvas.after(50, animate)
        else:
            # make a list of colors of the balls after the elapsed time
            ball_colors = []
            for ball in balls:
                ball_colors.append(ball.color)

            # this block of code displays the final count, if you guessed right.
            results_dict = count_balls(ball_colors)
            display_result(frame_result, results_dict, var.get())  # displays the result after the simulation

        frame_ui.destroy()

    def select_option():
        # the button to continue would appear
        button_animate = Button(frame_ui, text="start the simulation",  width=20, command=start_timer)
        button_animate.grid(row=5, pady=30)

    label_instruction = Label(frame_ui, text=f"Guess the color with \nthe most number of balls.\n", font=("Helvetica", 12))
    label_instruction.grid(row=0)

    # Create a variable to store the selected option
    var = StringVar()
    for idx, option in enumerate(colors_option):
        rb = Radiobutton(frame_ui, text=option, variable=var, value=option, indicatoron=0, width=20, height=2,
                        command=select_option, bg=option, font=("Helvetica", 12),
                        activebackground='lightsteelblue', selectcolor=option)
        rb.grid(row=idx % 4+1)

    window.mainloop()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()


