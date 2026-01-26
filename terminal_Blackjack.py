import requests
from colorama import Fore, Back, Style

#Text interface --start
print(Fore.RED + Back.LIGHTGREEN_EX + "BlackjackV1" + Style.RESET_ALL)

#functions
def shuffleDeck():
    shuffleURL = 'https://deckofcardsapi.com/api/deck/new/shuffle/?deck_count=1'
    shuffleResponse = requests.get(shuffleURL)
    shuffleData = shuffleResponse.json()
    deckId = shuffleData['deck_id']
    remainingCards = shuffleData['remaining']
    return{
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

def displayHand(arr):
    for card in arr:
        print(card[3], "of", card[1])

def checkWinner():
    global dealerHand
    global playerHand
    global playerStake
    global playerChips
    if HandSum(playerHand) < HandSum(dealerHand) <= 21:
        print("You lost!", f"dealer's {HandSum(dealerHand)} beats your {HandSum(playerHand)}")
    elif HandSum(dealerHand) < HandSum(playerHand) <= 21:
        print("You won!",f"Your {HandSum(playerHand)} beat the dealer's {HandSum(dealerHand)}")
        playerChips += playerStake
    elif HandSum(dealerHand)>21:
        print("Dealer busts, You won!")
        playerChips += playerStake
    elif HandSum(playerHand)==HandSum(dealerHand) and HandSum(playerHand)<=21:
        print("Push!")
        playerChips += playerStake //2

def dealerLogic():
    while HandSum(dealerHand)<17:
        print("")
        print("Dealer is drawing...")
        drawCard(dealerHand)
        print("dealer's hand:")
        displayHand(dealerHand)
    print("")
    checkWinner()

#setup
playerHand = []
dealerHand = []
playerStake = 0

playerChips = 1000

deck = shuffleDeck()
deck_id = deck['deck_id']
remaining_cards = deck['remaining']
currentDeckURL = f"https://deckofcardsapi.com/api/deck/{deck_id}/draw/?count=1"

#game loop
while playerChips > 0:
    print("")
    bet = int(input("Insert bet amount(current chips: "+Fore.GREEN + f"{playerChips}" + Style.RESET_ALL+"):"))
    if bet <= 0 or bet > playerChips:
        print("Invalid bet")
        continue
    stake(bet)
    print("")
    drawCard(playerHand)
    drawCard(playerHand)
    drawCard(dealerHand)
    print("your hand:")
    displayHand(playerHand)
    print("")
    print("dealer's hand:")
    displayHand(dealerHand)
    print("")
    #innitial card draw
    if isBlackjack(playerHand):
        print("Blackjack!  You won!")
        playerChips += playerStake * 1.5
        playerHand.clear()
        dealerHand.clear()
        continue

    while HandSum(playerHand)<=21:
        if HandSum(playerHand)==21:
            dealerLogic()
            break
        prompt = input("Hit? Y/N: ")
        if prompt == "Y":
            print("")
            print("your hand:")
            drawCard(playerHand)
            displayHand(playerHand)
            print("")

        elif prompt == "N":
            print("")
            dealerLogic()
            break

    else:
        print("You busted!")

    if remaining_cards <= 6:
        print("shuffling deck ...")
        deck = shuffleDeck()
        deck_id = deck['deck_id']
        remaining_cards = deck['remaining']
        currentDeckURL = f"https://deckofcardsapi.com/api/deck/{deck_id}/draw/?count=1"
        print("")

    playerHand.clear()
    dealerHand.clear()