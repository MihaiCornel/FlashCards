from tkinter import *
import pandas
import random

pick = {}
data_dict = {}


def next_slide():
    global pick, flip_timer
    window.after_cancel(flip_timer)
    pick = random.choice(data_dict)
    canvas.itemconfig(card_title, text="English")
    canvas.itemconfig(card_word, text=pick["English"])
    canvas.itemconfig(canvas_image, image=bg_image)
    canvas.itemconfig(card_title, text="English", fill="black")
    canvas.itemconfig(card_word, text=pick["English"], fill="black")
    flip_timer = window.after(3000, func=flip_card)


def flip_card():
    canvas.itemconfig(card_title, text="Romanian", fill="white")
    canvas.itemconfig(card_word, text=pick["Romanian"], fill="white")
    canvas.itemconfig(canvas_image, image=back_image)


def is_known():
    data_dict.remove(pick)
    next_slide()
    new_data = pandas.DataFrame(data_dict)
    new_data.to_csv("data/words_to_learn.csv", index=False)


BACKGROUND_COLOR = "#B1DDC6"
# Create window:
window = Tk()
window.title("Flashy")
window.config(pady=50, padx=50, background=BACKGROUND_COLOR)

flip_timer = window.after(3000, func=flip_card)

# aces to file
try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    og_data = pandas.read_csv("data/ro-en.csv")
    data_dict = og_data.to_dict(orient="records")
else:
    data_dict = data.to_dict("records")

# Create image:
canvas = Canvas(width=800, height=526, background=BACKGROUND_COLOR)
bg_image = PhotoImage(file="imagini/card_front.png")
back_image = PhotoImage(file="imagini/card_back.png")
canvas_image = canvas.create_image(400, 263, image=bg_image)
canvas.config(bg = BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(row=0, column=0, columnspan=2)
card_title = canvas.create_text(400, 150, font=("Ariel",40,"italic"), text="English")
card_word = canvas.create_text(400, 263, font=("Ariel",60,"bold"),text="data")

# Create buttons:
x_image = PhotoImage(file="imagini/wrong.png")
wrong_button = Button(image=x_image, highlightthickness=0, command=next_slide)
wrong_button.grid(row=1, column=0)

g_image = PhotoImage(file="imagini/right.png")
g_button = Button(image=g_image, highlightthickness=0, command=is_known)
g_button.grid(row=1, column=1)

next_slide()

window.mainloop()
