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
        for card in self.hand:
            if card[0] == top_card[0] or card[1] == top_card[1]:
                return card
        return None

class UnoGame:
    COLORS = ['Red', 'Yellow', 'Green', 'Blue']
    VALUES = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'Skip', 'Reverse', 'Draw Two']

    def __init__(self):
        self.players = []
        self.draw_pile = []
        self.discard_pile = []
        self.current_player = 0
        self.direction = 1

    def setup_game(self, player_names):
        self.create_deck()
        random.shuffle(self.draw_pile)
        self.deal_cards(player_names)
        self.discard_pile.append(self.draw_pile.pop())

    def create_deck(self):
        for color in self.COLORS:
            for value in self.VALUES:
                self.draw_pile.append((color, value))
                if value != '0':  # Two of each card except 0
                    self.draw_pile.append((color, value))

    def deal_cards(self, player_names):
        for name in player_names:
            player = Player(name, is_ai=(name.startswith("AI")))
            self.players.append(player)
            for _ in range(7):
                player.draw_card(self.draw_pile.pop())

    def draw_card(self, player):
        if self.draw_pile:
            player.draw_card(self.draw_pile.pop())
        else:
            self.draw_pile = self.discard_pile[:-1]
            random.shuffle(self.draw_pile)
            self.discard_pile = [self.discard_pile[-1]]
            player.draw_card(self.draw_pile.pop())

    def play_turn(self):
        player = self.players[self.current_player]
        top_card = self.discard_pile[-1]
        if player.is_ai:
            card = player.choose_card(top_card)
        else:
            # For simplicity, assume human player always plays the first valid card
            card = player.choose_card(top_card)

        if card:
            self.discard_pile.append(player.play_card(card))
            print(f"{player.name} played {card}")
            if card[1] == 'Skip':
                self.switch_turn(skip=True)
            else:
                self.switch_turn()
        else:
            self.draw_card(player)
            print(f"{player.name} drew a card")
            self.switch_turn()

        if not player.hand:
            print(f"{player.name} wins!")
            return True

        return False

    def switch_turn(self, skip=False):
        if skip:
            self.current_player = (self.current_player + 2 * self.direction) % len(self.players)
        else:
            self.current_player = (self.current_player + self.direction) % len(self.players)

    def start_game(self):
        while True:
            if self.play_turn():
                break

# Example usage
game = UnoGame()
game.setup_game(["Player1", "AI1", "AI2"])
game.start_game()