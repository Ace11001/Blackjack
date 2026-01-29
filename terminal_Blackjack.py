import requests
from colorama import Fore, Back, Style
import os
import time
import sys
import platform
# functions
def introText(hasDESC):
    # Text interface --start
    print(
        Fore.LIGHTGREEN_EX + Style.DIM + "Blackjack " + Fore.BLACK + Back.WHITE+" ♠ " + Fore.RED + "♥ " + Fore.BLACK + "♣ " + Fore.RED + "♦ " + Style.RESET_ALL)
    if hasDESC:
        print(
            Fore.LIGHTGREEN_EX + "Updated version ~ improved command line ~ if unsure how to play type:> help" + Style.RESET_ALL)

def update_title():
    global playerChips
    title = f"Blackjack//Current chips: {playerChips}"
    if platform.system() == "Windows":
        os.system(f"title {title}")
    else:
        sys.stdout.write(f"\033]0;{title}\007")
        sys.stdout.flush()

def play_round():
    global playerHand, dealerHand, playerChips, deck_id, deck, remaining_cards, currentDeckURL, autoplay
    playerHand.clear()
    dealerHand.clear()
    clear_screen(autoclear)
    introText(False)

    bet = int(input("Insert bet amount(current chips: " + Fore.GREEN + f"{playerChips}" + Style.RESET_ALL + "):"))
    if bet == 0:
        return
    if bet < 0 or bet > playerChips:
        print("Invalid bet")
        return
    stake(bet)
    update_title()
    print("")

    # drawing cards, dealer only draws one to simulate having one face down
    drawCard(playerHand)
    drawCard(playerHand)
    drawCard(dealerHand)

    # display drawn hands
    print("your hand:")
    displayHand(playerHand, togSUM)
    print("")
    print("dealer's hand:")
    displayHand(dealerHand, togSUM)
    print("")

    # initial Blackjack check
    if isBlackjack(playerHand):
        print("Blackjack!  You won!")
        playerChips += int(playerStake * 1.5)
        update_title()
        playerHand.clear()
        dealerHand.clear()
        return

    while HandSum(playerHand) <= 21:
        if HandSum(playerHand) == 21:
            dealerLogic()
            break
        prompt = input("Hit? Y/N: ")  # should maybe add valid answers for y/n, 0/1, true/false
        if prompt == "Y":
            print("")
            print("your hand:")
            drawCard(playerHand)
            displayHand(playerHand, togSUM)
            print("")

        elif prompt == "N":
            print("")
            dealerLogic()
            break

    else:
        print("You busted!")
    # reshuffles whole deck, before an empty deck can cause an issue
    if remaining_cards <= 6:
        print("shuffling deck ...")
        deck = shuffleDeck()
        deck_id = deck['deck_id']
        remaining_cards = deck['remaining']
        currentDeckURL = f"https://deckofcardsapi.com/api/deck/{deck_id}/draw/?count=1"
        print("")

    if autoplay:
        print(f"next round starting in 3")
        time.sleep(1.1)
        print(f"next round starting in 2")
        time.sleep(1.1)
        print(f"next round starting in 1")
        time.sleep(1.1)
        play_round()

def shuffleDeck():
    shuffleURL = 'https://deckofcardsapi.com/api/deck/new/shuffle/?deck_count=1'
    shuffleResponse = requests.get(shuffleURL)
    shuffleData = shuffleResponse.json()
    deckId = shuffleData['deck_id']
    remainingCards = shuffleData['remaining']
    return {
        'deck_id': deckId,
        'remaining': remainingCards
    }

def drawCard(arr):
    drawCardResponse = requests.get(currentDeckURL)
    drawCardData = drawCardResponse.json()
    face = drawCardData['cards'][0]['value']
    suit = drawCardData['cards'][0]['suit']
    global remaining_cards
    remaining_cards = drawCardData['remaining']
    AceBool = False
    if face in ("QUEEN", "KING", "JACK"):
        value = 10
    elif face == "ACE":
        value = 11
        AceBool = True
    else:
        value = int(face)
    arr.append([value, suit, AceBool, face])

def HandSum(arr):
    total = sum(card[0] for card in arr)
    ace_count = sum(1 for card in arr if card[2])

    while total > 21 and ace_count > 0:
        total -= 10
        ace_count -= 1

    return total

def hasAce(arr):
    return any(card[2] for card in arr)

def isBlackjack(arr):
    if HandSum(arr) == 21 and hasAce(arr) == True and len(arr) == 2:
        return True
    else:
        return False

def bust(arr):
    if HandSum(arr) > 21:
        return True
    else:
        return False

def stake(num):
    global playerChips, playerStake
    playerChips -= num
    playerStake = num * 2

def displayHand(arr, Bool):
    for card in arr:
        print(card[3], "of", card[1])
    if Bool:
        print("  Hand Value:" + Fore.YELLOW + str(HandSum(arr)) + Style.RESET_ALL)

def checkWinner():
    global dealerHand
    global playerHand
    global playerStake
    global playerChips
    if HandSum(playerHand) < HandSum(dealerHand) <= 21:
        print("You lost!", f"dealer's {HandSum(dealerHand)} beats your {HandSum(playerHand)}")
    elif HandSum(dealerHand) < HandSum(playerHand) <= 21:
        print("You won!", f"Your {HandSum(playerHand)} beat the dealer's {HandSum(dealerHand)}")
        playerChips += playerStake
        update_title()
    elif HandSum(dealerHand) > 21:
        print("Dealer busts, You won!")
        playerChips += playerStake
        update_title()
    elif HandSum(playerHand) == HandSum(dealerHand) and HandSum(playerHand) <= 21:
        print("Push!")
        playerChips += playerStake // 2
        update_title()

def dealerLogic():
    while HandSum(dealerHand) < 17:
        print("")
        print("Dealer is drawing...")
        drawCard(dealerHand)
        print("dealer's hand:")
        displayHand(dealerHand, togSUM)
    print("")
    checkWinner()

def clear_screen(Bool):
    if Bool:
        os.system('cls' if os.name == 'nt' else 'clear')

# command line functions
def help1():
    print("  help cmd    :list of valid commands")
    print("  help rls    :displays the Blackjack rules")
def helpCMD():
    print(Fore.CYAN + "Commands:" + Style.RESET_ALL)
    print("  play    :starts a round")
    print("  quit    :quits the game")
    print("  clear   :clears the terminal")
    print("  tog     :opens game config")
def helpRLS():
    print(Fore.RED + "Rules:" + Style.RESET_ALL)
    print("  Dealer must draw until soft 17")
    print("  Blackjack pays" + Fore.YELLOW + " 3:2" + Style.RESET_ALL)

def toggleCMD():
    print("  tog sum    :if ON: Displaying player/dealer's hands also display the sum of the hand value")
    print("  tog auto   :if ON: Automatically starts a new round 3 seconds after finishing a round")
    print("                     To leave autoplay enter 0 when prompted to enter bet amount")
    print("  tog clear  :if ON: Automatically clears the terminal after starting a new round")
def toggleSUM():
    global togSUM
    togSUM = not togSUM
    print(f"Hand sum is {'ON' if togSUM else 'OFF'}")
def toggleAUTO():
    global autoplay
    autoplay = not autoplay
    print(f"autoplay is {'ON' if autoplay else 'OFF'}")
def toggleClear():
    global autoclear
    autoclear = not autoclear
    print(f"autoclear is {'ON' if autoclear else 'OFF'}")

# debug command line functions
def hiddenCMD():
    print(Fore.RED+"  cheats chips    :add chips"+Style.RESET_ALL)
    print(Fore.RED+"  reset           :Resets chips and reshuffles Deck"+Style.RESET_ALL)
    print(Fore.RED+"  api debug       :Prints variables related to the api"+Style.RESET_ALL)
    print(Fore.RED+"  player debug    :Prints variables related to the player"+Style.RESET_ALL)
    print(Fore.RED+"  dealer debug    :Prints variables related to the dealer"+Style.RESET_ALL)
def cheatCHIPS():
    global playerChips
    playerChips += int(input("  Enter chip amount:"))
def resetCMD():
    global playerChips,deck,deck_id,remaining_cards,currentDeckURL
    playerChips = 1000
    shuffleDeck()
    deck = shuffleDeck()
    deck_id = deck['deck_id']
    remaining_cards = deck['remaining']
    currentDeckURL = f"https://deckofcardsapi.com/api/deck/{deck_id}/draw/?count=1"

def apiDBG():
    global deck_id, remaining_cards, currentDeckURL
    print(f"  Deck ID:{deck_id}")
    print(f"  Remaining cards:{remaining_cards}")
    print(f"  Current deck URL:{currentDeckURL}")
def plyDBG():
    global playerChips, playerStake, playerHand, autoplay, togSUM
    print(f"  Player Chips:{playerChips}")
    print(f"  Player Stake:{playerStake}")
    print(f"  Player Hand:")
    for x in playerHand:
        print("    "+str(x))
    print(f"  Autoplay:{autoplay}")
    print(f"  AutoSum:{togSUM}")
def dlrDBG():
    global dealerHand
    print("  Dealer draws until soft 17")
    print("  Dealer Hand:")
    for x in dealerHand:
        print("    "+str(x))

# setup
togSUM = False
autoplay = False
autoclear = False

playerHand = []
dealerHand = []
playerStake = 0
playerChips = 1000

deck = shuffleDeck()
deck_id = deck['deck_id']
remaining_cards = deck['remaining']
currentDeckURL = f"https://deckofcardsapi.com/api/deck/{deck_id}/draw/?count=1"

commands = {
    # basic
    "help": help1,
    "play": play_round,
    "quit": exit,
    "clear": lambda: clear_screen(True),
    "tog": toggleCMD,
    "hidden": hiddenCMD,
    # less so
    "help cmd": helpCMD,
    "help rls": helpRLS,
    "tog sum": toggleSUM,
    "tog auto": toggleAUTO,
    "tog clear": toggleClear,
    #hidden
    "cheats chips": cheatCHIPS,
    "reset":resetCMD,
    "api debug": apiDBG,
    "player debug": plyDBG,
    "dealer debug": dlrDBG,
}
# Game Loop
introText(True)
while True:
    cmd = input("> ").strip().lower()
    if cmd in commands:
        commands[cmd]()
    else:
        print("Unknown command")