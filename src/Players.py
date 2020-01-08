from Pickable.Pickable import Pickable
from time import time


class Players(Pickable):
    def __init__(self, *players, **kwargs):
        self.players = list(players)

    def append(self, player):
        self.players.append(player)

    def insert(self, i, player):
        self.players.insert(i, player)

    def pop(self, index):
        return self.players.pop(index)

    def remove(self, player):
        self.players.remove(player)

    def index(self, player):
        return self.players.index(player)

    def __getitem__(self, index):
        return self.players[index]

    def __len__(self):
        return len(self.players)

    def __iter__(self):
        for p in self.players:
            yield p

    def strength(self):
        return sum(p.rating for p in self)

    def chance(self, opponent):
        """Evaluate chance against `opponent`"""
        return 1.0 / (
            1.0 + 10.0 ** (float(opponent.strength() - self.strength()) / 400.0)
        )

    def delta(self, winner, opponent):
        """Evaluate `self` delta player rating"""
        try:
            return 40.0 * ((1.0 if winner else 0.0) - self.chance(opponent)) / len(self)
        except:
            return 0

    def update_rating(self, delta, win):
        for p in self:
            p.update_rating(delta, win)

    def find_id(self, id):
        res = [p for p in self if p.id == id]
        if len(res) > 0:
            return res[0]
        else:
            return None
