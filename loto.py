from random import randint, choices, shuffle


def strike(text: str):
    return ''.join([u'\u0336{}'.format(c) for c in text])


def rjust(text: str, width: int):
    additional_len = sum(c == '\u0336' for c in text)
    return text.rjust(width + additional_len)


def unique_numbers(count: int, low: int, high: int):
    res = []
    while len(res) < count:
        new = randint(low, high)
        if new not in res:
            res.append(new)
    return res


class Keg:
    placeholder = ' '

    def __init__(self, value: int | None):
        self.value = value
        self.is_crossed = False

    def cross_out(self):
        self.is_crossed = True

    def __eq__(self, other):
        return self.value == other.value

    def __str__(self):
        if self.value is None:
            return Keg.placeholder
        if self.is_crossed:
            return strike(str(self.value))
        else:
            return str(self.value)


class Card:
    def __init__(self, num_kegs: int = 90, rows: int = 3, cols: int = 9, nums_per_row: int = 5):
        assert nums_per_row < cols
        self.num_kegs = num_kegs
        self.rows = rows
        self.cols = cols
        self.nums_per_row = nums_per_row
        self.data = self.generate()
        self.crossed_nums = 0

    def generate(self):
        data = []
        count = self.rows * self.nums_per_row
        numbers = unique_numbers(count, 1, self.num_kegs)
        for row in range(self.rows):
            # get numbers for row
            nums_on_row = [Keg(val) for val in
                           sorted(numbers[self.nums_per_row * row:
                                          self.nums_per_row * (row + 1)])]
            empty_poses = self.cols - len(nums_on_row)
            indexes = choices(range(self.cols), k=empty_poses)
            for idx in indexes:
                nums_on_row.insert(idx, Keg(None))
            data += nums_on_row
        return data

    def __contains__(self, keg: Keg):
        return keg in self.data

    def __str__(self):
        separator = '|'
        col_width = len(str(self.num_kegs))
        row_len = col_width * self.cols + self.cols + 1
        delimiter = '-' * row_len + '\n'

        s = ''
        s += delimiter
        for row in range(self.rows):
            s += separator
            s += separator.join([rjust(str(keg), col_width) for keg in
                                 self.data[self.cols * row:
                                           self.cols * (row + 1)]])
            s += separator + '\n'
            s += delimiter
        return s

    def cross_out(self, keg: Keg):
        idx = self.data.index(keg)
        self.data[idx].cross_out()
        self.crossed_nums += 1

    def is_crossed(self) -> bool:
        return self.crossed_nums == self.rows * self.nums_per_row


class Player:
    def __init__(self, name: str, card: Card):
        self.name = name
        self.card = card

    def cross_out(self, keg: Keg) -> bool:
        if keg in self.card:
            self.card.cross_out(keg)
        return True


class ComputerPlayer(Player):
    pass


class HumanPlayer(Player):
    def cross_out(self, keg: Keg):
        print(keg)
        print(keg in self.card)
        answer = input('Зачеркнуть цифру? (y/n)').lower().strip()
        print(answer == 'y')
        if answer == 'y' and not keg in self.card or \
           answer != 'y' and keg in self.card:
            return False
        if keg in self.card:
            self.card.cross_out(keg)
        return True


class Game:
    def __init__(self, naum_kegs: int = 100):
        self.players = []
        self.naum_kegs = naum_kegs
        self.kegs = []

    def add_player(self, player: Player):
        self.players.append(player)

    def start(self):
        num_computers = 0
        num_players = int(input('Введите кол-во игроков: '))
        for i in range(num_players):
            while True:
                ptype = input('Игрок Человек или Компьютер? (h/c): ').lower().strip()
                if ptype == 'c':
                    self.add_player(ComputerPlayer(name=f'Computer {num_computers+1}', card=Card()))
                    break
                elif ptype == 'h':
                    name = input('Введите имя игрока: ')
                    self.add_player(HumanPlayer(name=name, card=Card()))
                    break
                else:
                    print('Ввежите c - Компьютер, h - Человек.')
        self.kegs = [Keg(val) for val in range(1, self.naum_kegs + 1)]
        shuffle(self.kegs)

    def play_round(self):
        resume = True
        players_to_remove = []

        if not self.kegs:
            print('Больше нет бочонков.')
            return False

        keg = self.kegs.pop()
        print(f'Новый бочонок: {keg} (осталось {len(self.kegs)})')
        for player in self.players:
            print(f'Ходит игрок {player.name}')
            print('Карточка игрока:')
            print(player.card)
            print()
            res = player.cross_out(keg)
            if not res:
                print(f'Игрок {player.name} - выбывает!')
                players_to_remove.append(player)
            else:
                print(player.card)

            if player.card.is_crossed():
                print(f'Игрок {player.name} - выиграл!')
                return False

        for players in players_to_remove:
            self.players.remove(players)

        if all(isinstance(player, ComputerPlayer) for player in self.players):
            resume = False

        return resume


if __name__ == '__main__':
    game = Game(naum_kegs=100)
    game.start()

    while True:
        resume = game.play_round()
        if not resume:
            break
