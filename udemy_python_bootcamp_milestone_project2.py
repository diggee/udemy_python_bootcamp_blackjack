from random import shuffle
from IPython.display import clear_output


class Bank():

    def __init__(self, bet, balance):
        self.bet = bet
        self.balance = balance

    def transaction_win(self):
        self.balance += self.bet * 2
        return self.balance

    def transaction_loss(self):
        self.balance -= self.bet
        return self.balance


def introduction():
    print('*' * 40)
    print('\nWelcome to Blackjack!')
    print('This is a simplified version of the actual game')
    print('Each card club is represented by its initial i.e. (H)earts,(S)pade,(D)iamond and (C)lub')
    print('Player can only Hit or Stay. Double down, insurance, card splits are not a feature of the game')
    print('Rest of the rules remain the same. Good luck and have fun!\n')
    print('*' * 40)
    print('\n\n')
    balance = int(input('What is the maximum total balance you can bet?'))
    bet = int(input('What amount would you like to bet?'))
    return balance, bet


class Deck():

    def __init__(self, card_no):
        self.card_no = card_no

    def card_display(self):
        if self.card_no in range(1, 14):
            card_house = 'H'
        elif self.card_no in range(14, 27):
            card_house = 'S'
        elif self.card_no in range(27, 40):
            card_house = 'D'
        else:
            card_house = 'C'
        temp = self.card_no % 13
        if temp == 0:
            temp = 13
        return str(temp) + card_house

    def card_score(self):
        temp = self.card_no % 13
        if temp in range(1, 11):
            card_score = 1
        elif temp in range(11, 13):
            card_score = 10
        else:
            card_score = 10
        return card_score


def start_game(player_hand, dealer_hand):
    cards = list(range(1, 53))
    shuffle(cards)
    print('Card deck shuffled!')
    print('Dealing cards\n\n')
    player_card = [cards.pop(), cards.pop()]
    dealer_card = [cards.pop(), cards.pop()]
    player_score = []
    dealer_score = []

    for (i, j) in zip(player_card, dealer_card):
        temp1 = Deck(i)
        temp2 = Deck(j)
        player_hand.append(temp1.card_display())
        player_score.append(temp1.card_score())
        dealer_hand.append(temp2.card_display())
        dealer_score.append(temp2.card_score())

    return player_hand, dealer_hand, cards, player_score, dealer_score


def hand_score(player_score, dealer_score):
    return sum(player_score), sum(dealer_score)


def display_hand(player_hand, dealer_hand, choice):

    if choice == 1:
        print('Dealer hand:', end=' ')
        for i in dealer_hand[:-1]:
            print(i, end=' ')
        print('*')
    else:
        print('Dealer hand: ' + ' '.join(dealer_hand))
    print('\n' * 5)
    print('Player hand: ' + ' '.join(player_hand))


def player_choice():
    while True:
        try:
            choice = int(input('Do you want to Hit(1) or Stay(2)?'))
        except ValueError:
            print('Error! Non numeral input/invalid numeral input. Try again')
        else:
            if choice not in [1, 2]:
                print('Invalid numeral input. Please try again')
                continue
            else:
                return choice
                break


def win_check(player_total, dealer_total, bet, balance, choice):
    temp = Bank(bet, balance)
    if player_total == 21:
        print('Congrats! You won!')
        balance = temp.transaction_win()
        return True, balance
    elif dealer_total == 21 and choice == 2:
        print('Sorry, you lost your bet')
        balance = temp.transaction_loss()
        return True, balance
    elif player_total > 21:
        print('Bust! Sorry, you lost your bet')
        balance = temp.transaction_loss()
        return True, balance
    elif dealer_total < 21 and dealer_total > player_total and choice == 2:
        print('Sorry, you lost your bet')
        balance = temp.transaction_loss()
        return True, balance
    elif dealer_total > 21 and choice == 2:
        print('Congrats! You won!')
        balance = temp.transaction_win()
        return True, balance
    else:
        return False, balance


def play_again(balance):
    wish = input('Do you wish to play again? (Y)es or (N)o?')
    bet = 0
    if 'y' in wish.lower():
        answer = True
        print('Available balance: {}'.format(balance))
        while True:
            try:
                bet = int(input('how much would you like to bet?'))
            except ValueError:
                print('please give a numeric input')
            else:
                if balance - bet < 0:
                    print('Cannot bet more than available balance. Try again')
                    continue
                else:
                    break
    elif 'n' in wish.lower():
        answer = False
        print('Thanks for playing. Your final balance is {}'.format(balance))
    else:
        clear_output()
        print('Give proper input please')
        play_again(balance)
    return answer, bet


play_answer = True
balance, bet = introduction()

while balance > 0 and play_answer is True:

    choice = 1
    winner_check = False
    player_hand, dealer_hand, cards, player_score, dealer_score = start_game([], [
    ])
    player_total, dealer_total = hand_score(player_score, dealer_score)
    display_hand(player_hand, dealer_hand, choice)
    choice = player_choice()
    while (choice == 1 or choice == 2) and winner_check is False:

        card_drawn = cards.pop()
        temp = Deck(card_drawn)
        if choice == 1:
            player_total += temp.card_score()
            player_hand.append(temp.card_display())
            player_score.append(temp.card_score())
        else:
            dealer_total += temp.card_score()
            dealer_hand.append(temp.card_display())
            dealer_score.append(temp.card_score())

        clear_output()
        display_hand(player_hand, dealer_hand, choice)
        winner_check, balance = win_check(
            player_total, dealer_total, bet, balance, choice)
        if winner_check:
            break
        elif choice == 1:
            choice = player_choice()
        else:
            pass

    if balance == 0:
        print('You are too poor to bet more. Better luck next time.')
        break
    else:
        pass

    play_answer, bet = play_again(balance)
    del winner_check, player_hand, dealer_hand, cards, player_score, dealer_score, player_total, dealer_total, temp
