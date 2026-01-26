#code used to download all 52 card images from the api
#not needed anymore after download
import requests
import os

url = "https://deckofcardsapi.com/static/img/"
values = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "J", "Q", "K", "A"]
suits = ["H", "D", "C", "S"]
folder = "cards"
os.makedirs(folder, exist_ok=True)
for value in values:
    for suit in suits:
        image_url = url + value + suit + ".png"
        filename = f"{value}{suit}.png"
        save_path = os.path.join(folder, filename)

        response = requests.get(image_url)
        if response.status_code == 200:
            with open(save_path, "wb") as f:
                f.write(response.content)
            print(f"Saved {filename}")
        else:
            print(f"Failed to download {filename}")
