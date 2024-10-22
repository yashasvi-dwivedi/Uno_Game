import random

class Player:
    def __init__(self, name, is_ai=False):
        self.name = name
        self.hand = []
        self.is_ai = is_ai

    def draw_card(self, card):
        self.hand.append(card)

    def play_card(self, card):
        self.hand.remove(card)
        return card

    def choose_card(self, top_card):
        # Heuristic: prioritize matching color, then value, then special cards
        color_match = [card for card in self.hand if card[0] == top_card[0]]
        value_match = [card for card in self.hand if card[1] == top_card[1]]
        special_cards = [card for card in self.hand if card[1] in ['Skip', 'Reverse', 'Draw Two', 'Wild', 'Wild Draw Four']]

        if color_match:
            return color_match[0]
        elif value_match:
            return value_match[0]
        elif special_cards:
            return special_cards[0]
        return None

    def choose_card_human(self, top_card):
        print(f"Top card: {top_card}")
        print("Your hand:")
        for idx, card in enumerate(self.hand):
            print(f"{idx}: {card}")
        
        while True:
            try:
                choice = int(input("Enter the index of the card you want to play (or -1 to draw a card): "))
                if choice == -1:
                    return None
                if 0 <= choice < len(self.hand):
                    card = self.hand[choice]
                    if card[0] == top_card[0] or card[1] == top_card[1] or card[0] == 'Wild':
                        return card
                    else:
                        print("Invalid card. It doesn't match the top card.")
                else:
                    print("Invalid index. Try again.")
            except ValueError:
                print("Invalid input. Enter a number.")

class UnoGame:
    COLORS = ['Red', 'Yellow', 'Green', 'Blue']
    VALUES = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'Skip', 'Reverse', 'Draw Two']
    SPECIAL_CARDS = ['Wild', 'Wild Draw Four']

    def __init__(self):
        self.players = []
        self.draw_pile = []
        self.discard_pile = []
        self.current_player = 0
        self.direction = 1
        self.current_color = None

    def setup_game(self, player_names):
        self.create_deck()
        random.shuffle(self.draw_pile)
        self.deal_cards(player_names)
        first_card = self.draw_pile.pop()
        self.discard_pile.append(first_card)
        self.current_color = first_card[0]

    def create_deck(self):
        for color in self.COLORS:
            for value in self.VALUES:
                self.draw_pile.append((color, value))
                if value != '0':  # Two of each card except 0
                    self.draw_pile.append((color, value))
        for _ in range(4):  # Four of each special card
            self.draw_pile.append(('Wild', 'Wild'))
            self.draw_pile.append(('Wild', 'Wild Draw Four'))

    def deal_cards(self, player_names):
        for name in player_names:
            player = Player(name, is_ai=(name.startswith("AI")))
            self.players.append(player)
            for _ in range(7):
                player.draw_card(self.draw_pile.pop())

    def draw_card(self, player, count=1):
        for _ in range(count):
            if self.draw_pile:
                player.draw_card(self.draw_pile.pop())
            else:
                self.draw_pile = self.discard_pile[:-1]
                random.shuffle(self.draw_pile)
                self.discard_pile = [self.discard_pile[-1]]
                player.draw_card(self.draw_pile.pop())

    def choose_color(self):
        print("Choose a color: 0: Red, 1: Yellow, 2: Green, 3: Blue")
        while True:
            try:
                choice = int(input("Enter the number of the color you want: "))
                if 0 <= choice < 4:
                    return self.COLORS[choice]
                else:
                    print("Invalid choice. Try again.")
            except ValueError:
                print("Invalid input. Enter a number.")

    def play_turn(self):
        player = self.players[self.current_player]
        top_card = self.discard_pile[-1]
        if player.is_ai:
            card = player.choose_card(top_card)
        else:
            card = player.choose_card_human(top_card)

        if card:
            self.discard_pile.append(player.play_card(card))
            print(f"{player.name} played {card}")
            if card[1] == 'Skip':
                self.switch_turn(skip=True)
            elif card[1] == 'Draw Two':
                self.switch_turn(draw_two=True)
            elif card[1] == 'Reverse':
                self.direction *= -1
                self.switch_turn()
            elif card[1] == 'Wild':
                self.current_color = self.choose_color()
                print(f"{player.name} chose {self.current_color}")
                self.switch_turn()
            elif card[1] == 'Wild Draw Four':
                self.current_color = self.choose_color()
                print(f"{player.name} chose {self.current_color}")
                self.switch_turn(draw_four=True)
            else:
                self.current_color = card[0]
                self.switch_turn()
        else:
            self.draw_card(player)
            print(f"{player.name} drew a card")
            self.switch_turn()

        if not player.hand:
            print(f"{player.name} wins!")
            return True

        return False

    def switch_turn(self, skip=False, draw_two=False, draw_four=False):
        if draw_four:
            next_player = (self.current_player + self.direction) % len(self.players)
            self.draw_card(self.players[next_player], count=4)
            self.current_player = (self.current_player + 2 * self.direction) % len(self.players)
        elif draw_two:
            next_player = (self.current_player + self.direction) % len(self.players)
            self.draw_card(self.players[next_player], count=2)
            self.current_player = (self.current_player + 2 * self.direction) % len(self.players)
        elif skip:
            self.current_player = (self.current_player + 2 * self.direction) % len(self.players)
        else:
            self.current_player = (self.current_player + self.direction) % len(self.players)

    def start_game(self):
        while True:
            if self.play_turn():
                break


game = UnoGame()
game.setup_game(["Player1", "AI1", "AI2", "AI3"])
game.start_game()