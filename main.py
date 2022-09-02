import random
from tkinter import *
import pandas as pd

# Local imports
from art_and_craft import *

# Global Constants
LANGUAGE_1 = 'French'
LANGUAGE_2 = 'English'
ORIGIN = 'data/french_words.csv'
PROGRESS = f'data/{LANGUAGE_1}_words_to_learn.csv'
# Variables
flip_timer = 0
word = {}

# ---------------------------- FLASH CARD DATA ------------------------------- #
try:
    data = pd.read_csv(PROGRESS).to_dict(orient='records')
except FileNotFoundError:
    data = pd.read_csv(ORIGIN).to_dict(orient='records')
except pd.errors.EmptyDataError:
    data = pd.read_csv(ORIGIN).to_dict(orient='records')


def known_words():
    data.remove(word)
    pd.DataFrame(data).to_csv(PROGRESS, index=False)
    next_card()


def next_card():
    global flip_timer, word
    if flip_timer != 0:
        root.after_cancel(flip_timer)
    word = random.choice(data)
    canvas.itemconfig(display, image=card_front)
    canvas.itemconfig(card_title, text=LANGUAGE_1, fill='black')
    canvas.itemconfig(card_word, text=word[LANGUAGE_1], fill='black')
    flip_timer = root.after(3000, flip_card, word)


def flip_card(current_flash):
    canvas.itemconfig(display, image=card_back)
    canvas.itemconfig(card_title, text=LANGUAGE_2, fill='white')
    canvas.itemconfig(card_word, text=current_flash[LANGUAGE_2], fill='white')


# ---------------------------- UI SETUP ------------------------------- #
root = Tk()
root.title('Flash Cards')
root.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
# Canvas
canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
card_front = PhotoImage(file=CARD_FRONT)
card_back = PhotoImage(file=CARD_BACK)
display = canvas.create_image(400, 263, image=card_front)
# Labels
card_title = canvas.create_text(400, 150, text='Title', font=(FONT_NAME, 40, 'italic'))
card_word = canvas.create_text(400, 300, text='Word', font=(FONT_NAME, 60, 'bold'))
# Buttons
right_image = PhotoImage(file=RIGHT)
wrong_image = PhotoImage(file=WRONG)

known = Button(image=right_image, command=known_words)
unknown = Button(image=wrong_image, command=next_card)

# Geometry
canvas.grid(row=0, column=0, columnspan=2)
known.grid(row=1, column=0)
unknown.grid(row=1, column=1)

next_card()
root.mainloop()
