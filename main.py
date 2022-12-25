from tkinter import *
import pandas as pd
import random

BACKGROUND_COLOR = "#B1DDC6"

# ------------------- French and English text display -------------------- #

try:
    words_to_learn = pd.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    data = pd.read_csv("data/french_words.csv")
    data_dict = data.to_dict(orient="records")
else:
    data_dict = words_to_learn.to_dict(orient="records")

current_card = {}


def french_card():
    global current_card, delay
    window.after_cancel(delay)
    current_card = random.choice(data_dict)
    canvas.itemconfig(card_image, image=card_front)
    canvas.itemconfig(title, text="French", fill="black")
    canvas.itemconfig(word, text=current_card["French"], fill="black")

    delay = window.after(3000, english_card)


def english_card():
    canvas.itemconfig(card_image, image=card_back)
    canvas.itemconfig(title, text="English", fill="white")
    canvas.itemconfig(word, text=current_card["English"], fill="white")


def known_card():
    data_dict.remove(current_card)
    new_data = pd.DataFrame(data_dict)
    new_data.to_csv("data/words_to_learn.csv", index=False)
    french_card()

# --------------------- User Interface ------------------------ #


window = Tk()
window.title("Flashcard Program")
window.config(pady=30, padx=30, bg=BACKGROUND_COLOR)

delay = window.after(3000, english_card)

canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)

card_front = PhotoImage(file="images/card_front.png")
card_back = PhotoImage(file="images/card_back.png")
right = PhotoImage(file="images/right.png")
wrong = PhotoImage(file="images/wrong.png")

card_image = canvas.create_image(400, 263, image=card_front)
title = canvas.create_text(400, 150, text="", font=("Arial", 35, "italic"))
word = canvas.create_text(400, 263, text="", font=("Arial", 50, "bold"))
canvas.grid(row=1, column=1, columnspan=2)

right_button = Button(image=right, bg=BACKGROUND_COLOR, border=0, highlightthickness=0, command=known_card)
right_button.grid(row=2, column=2)

wrong_button = Button(image=wrong, bg=BACKGROUND_COLOR, border=0, highlightthickness=0, command=french_card)
wrong_button.grid(row=2, column=1)

french_card()

window.mainloop()
