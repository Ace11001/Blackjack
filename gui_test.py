import tkinter as tk
from PIL import Image, ImageTk
import os

#nomenclature for cards:
#1st:   A,2,3,4,5,6,7,8,9,0,J,Q,K
#2nd:   C,D,H,S
#Ace of spades: "AS";10 of hearts: "0H";...
CARD_FOLDER = "cards"

playerHandDisplay = ["AS","0H"]
dealerHandDisplay = ["9C","BACK"]

playerChips = 1000
current_stake = 0

#interface
root = tk.Tk()
root.title("Blackjack V2")
root.resizable(False, False)
root.geometry("800x600")#<placeholder>
root.configure(bg="darkgreen")

#grid setup
info_frame = tk.Frame(root, bg="darkgreen")
info_frame.grid(row=0, column=0, pady=10)

dealer_frame = tk.Frame(root, bg="darkgreen")
dealer_frame.grid(row=1, column=0, pady=10)

player_frame = tk.Frame(root, bg="darkgreen")
player_frame.grid(row=2, column=0, pady=10)

button_frame = tk.Frame(root, bg="darkgreen")
button_frame.grid(row=3, column=0, pady=10)

bet_frame = tk.Frame(root, bg="darkgreen")
bet_frame.grid(row=4, column=0, pady=10)

result_frame = tk.Frame(root, bg="darkgreen")
result_frame.grid(row=5, column=0, pady=10)


#labels
label_fg_color = "yellow"

total_chips_label = tk.Label(info_frame, text=f"Total Chips: ${playerChips}", font=("Arial", 14), bg="darkgreen", fg=label_fg_color)
total_chips_label.grid(row=0, column=0, padx=10)

stake_label = tk.Label(info_frame, text=f"Stake: ${current_stake}", font=("Arial", 14), bg="darkgreen", fg=label_fg_color)
stake_label.grid(row=0, column=1, padx=10)

result_label = tk.Label(result_frame, text="", font=("Arial", 16), fg="gold", bg="darkgreen")
result_label.pack()

def display_hand(frame, hand):
    for widget in frame.winfo_children():
        widget.destroy()
    images = []
    for col, card in enumerate(hand):
        path = os.path.join(CARD_FOLDER,f"{card}.png")
        image = Image.open(path).resize((100, 145))
        photo = ImageTk.PhotoImage(image)
        images.append(photo)

        label = tk.Label(frame, image=photo, bg="darkgreen")
        label.image = photo
        label.grid(row = 0,column = col,padx=5)

def hit():
    result_label.config(text="Hit!")
    display_hand(player_frame, playerHandDisplay)
def stand():
    result_label.config(text="Stand")
def setBet(amount):
    global current_stake
    current_stake = amount
    stake_label.config(text=f"Current Stake: {current_stake}")
    result_label.config(text="")

button_bg_color = "#FFD700"
button_fg_color = "black"
button_width = 10

hit_button = tk.Button(button_frame, text="Hit", width=button_width, bg=button_bg_color, fg=button_fg_color, command=hit)
hit_button.grid(row=0, column=0, padx=10)
stand_button =tk.Button(button_frame, text="Stand", width=button_width,bg=button_bg_color, fg=button_fg_color, command=stand)
stand_button.grid(row=0, column=1, padx=10)

#betting
tk.Label(bet_frame, bg="darkgreen", fg=label_fg_color).grid(row=0, column=0, padx=5)
bet_amounts = [5, 10, 50, 100, 500]
for i, amt in enumerate(bet_amounts):
    btn = tk.Button(bet_frame, text=f"${amt}", width=8, bg=button_bg_color, fg=button_fg_color, command=lambda a=amt: setBet(a))
    btn.grid(row=0, column=i+1, padx=5)

display_hand(dealer_frame, dealerHandDisplay)
display_hand(player_frame, playerHandDisplay)

root.mainloop()