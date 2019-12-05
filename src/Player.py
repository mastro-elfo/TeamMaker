
from Uid.Uid import Uid
from time import time

class Player(Uid):
    def __init__(self,
                nickname,
                number,
                rating,
                name,
                surname,
                *args, **kwargs):
        self.nickname = nickname
        self.number = number
        self.rating = rating
        self.last_update = time()
        self.name = name
        self.surname = surname
        self.win = 0
        self.lost = 0
        super(Player, self).__init__(*args, **kwargs)

    def __iter__(self):
        yield self.id
        yield self.nickname
        yield self.number
        yield self.rating
        yield self.last_update
        yield self.name
        yield self.surname

    def update(self, nickname = None, number = None, rating = None, name = None, surname = None):
        if nickname is not None:
            self.nickname = nickname
        if number is not None:
            self.number = number
        if rating is not None:
            self.rating = rating
        if name is not None:
            self.name = name
        if surname is not None:
            self.surname = surname
        self.last_update = time()

    def update_rating(self, delta, win):
        self.rating += delta
        if win:
            # TODO: remove when all players have win/lost
            try:
                self.win += 1
            except:
                self.win = 1
        else:
            try:
                self.lost += 1
            except:
                self.lost = 1
        self.last_update = time()
