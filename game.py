from random import sample


class Bag:

    def __init__(self):
        self.nums = sample(range(1, 91), 90)

    def next(self):
        if self.nums:
            return self.nums.pop()
        raise Exception('Мешок пуст!')

    def stats(self):
        print(f'В мешке {len(self.nums)} боченков.')

    def __str__(self):
        str_nums = ''
        for n in sorted(self.nums.copy()):
            str_nums += f'{n}, '
        return f'Всего {len(self.nums)}, бочонков №: {str_nums}'

    def __eq__(self, other):
        return sorted(self.nums) == sorted(other.nums)

    def __len__(self):
        return len(self.nums)


class RandomCard:

    def __init__(self, name):
        self.player_name = name
        # генерация чисел для карточки
        self.randomcard_nums = sample(range(1, 91), 15)
        # генерация мест для этих чисел на карточке
        self.place_idx = sample(range(0, 9), 5) + sample(range(9, 18), 5) + sample(range(18, 27), 5)
        # print(place_idx)

        # словарь {№места: число}
        self.randomcard = {key: 0 for key in range(27)}
        for x in range(len(self.randomcard_nums)):
            self.randomcard[self.place_idx[x]] = self.randomcard_nums[x]

    def modify(self, num):
        del_idx = self.place_idx[self.randomcard_nums.index(num)]
        self.randomcard[del_idx] = None

    def show(self):

        # печать карточки
        print(f'\n-{self.player_name}{"-" * (26 - len(self.player_name) - 1)}')
        for x in range(len(self.randomcard)):
            if self.randomcard[x] is None:
                print('--', end='')
            elif self.randomcard[x] == 0:
                print('  ', end='')
            elif self.randomcard[x] < 10:
                print(f' {self.randomcard[x]}', end='')
            else:
                print(self.randomcard[i], end='')
            print() if i + 1 in (9, 18, 27) else print(' ', end='')
        print('-' * 26, end='\n')

    def __str__(self):
        str_randomcard = f'\n-{self.player_name}{"-" * (26 - len(self.player_name) -  1)}\n'
        for x in range(len(self.randomcard)):
            if self.randomcard[x] is None:
                str_randomcard += '--'
            elif self.randomcard[x] == 0:
                str_randomcard += ''
            elif self.randomcard[x] < 10:
                str_randomcard += f'{self.randomcard[x]}'
            else:
                str_randomcard += f'{self.randomcard[x]}'
            str_randomcard += '\n' if i + 1 in (9, 18, 27) else ' '
        str_randomcard += '-' * 26 + '\n'
        return str_randomcard

    def __eq__(self, other):
        return sorted(self.randomcard_nums) == sorted(other.randomcard_nums)

    def __len__(self):
        return len(self.randomcard_nums)


class Computer:

    def __init__(self, name='Computer'):
        self.name = name
        self.randomcard = RandomCard(name)
        self.nums = self.randomcard.randomcard_nums.copy()
        self.is_winner = False

    def motion(self, num):

        if num in self.randomcard.randomcard_nums:
            self.randomcard.modify(num)
            self.nums.remove(num)
            self.is_winner = not self.nums

    def stats(self):
        print(f'{self.name}. Осталось {len(self.nums)} чисел : {self.nums}')

    def __str__(self):
        str_randomcard = str(self.randomcard)
        return str_randomcard + f'Имя игрока: {self.name}\nОсталось {len(self.nums)} чисел : {sorted(self.nums)}'

    def __eq__(self, other):
        return (sorted(self.nums) == sorted(other.nums)) and (self.is_winner == other.is_winner)

    def __len__(self):
        return len(self.nums)

    def __getitem__(self, item):
        return self.nums[item]

    def __contains__(self, item):
        return True if self.name == item else False


class User(Computer):

    def __init__(self, name='User'):
        Computer.__init__(self, name)

        self.is_looser = False
        self.answers = ['y', 'n']

    def motion(self, num):
        answer = input(f'{self.name}, зачеркнуть цифру? (y/n) ')
        while answer not in self.answers:
            answer = input('Не понял вас... Зачеркнуть цифру? (y/n) ')
        if answer == 'y':
            if num in self.randomcard.randomcard_nums:
                self.randomcard.modify(num)
                self.nums.remove(num)
                self.is_winner = not self.nums
            else:
                self.is_looser = True
        elif answer == 'n':
            if num in self.randomcard.randomcard_nums:
                self.is_looser = True

    def __str__(self):
        str_user = str(self.randomcard)
        return str_user + f'Имя игрока: {self.name}\nОсталось {len(self.nums)} чисел : {sorted(self.nums)}'

    def __eq__(self, other):
        return (sorted(self.nums) == sorted(other.nums)) and (self.is_winner == other.is_winner)

    def __len__(self):
        return len(self.nums)


class Game:

    def __init__(self):
        self.num_users = 0
        self.num_computers = 0
        self.players = {}
        self.bag = Bag()
        self.winners = []
        self.losers = []

    def generate_players(self, num_computers, num_users):

        for x in range(num_computers):
            pl_name = f'computer-{x + 1}'
            self.players[pl_name] = Computer(pl_name)

        for x in range(num_users):
            pl_name = f'user-{x + 1}'
            self.players[pl_name] = User(pl_name)

    def run(self, num_computers, num_users):
        self.num_computers = num_computers
        self.num_users = num_users

        self.generate_players(num_computers, num_users)
        self.cards_show()

        while True:
            num = self.bag.next()

            print(f'Из мешка вынут боченок номер {num}!')

            self.motion(num)

            if self.num_users == 0 and self.num_computers == 0:
                print('\nИГРА ОКОНЧЕНА')
                break

            self.cards_show()
            self.stats_show()

            self.bag.stats()

            if self.check_winner():
                break
            else:
                print('Игра продолжается...\n')

    def motion(self, num):
        for player in self.players.values():
            player.motion(num)
            if isinstance(player, User):
                if player.is_looser:
                    print(f'\nСОЖАЛЕЮ, {player.name}, но ВЫ ПРОИГРАЛИ... Нужно быть внимательнее!')
                    self.num_users -= 1
                    # заносим проигравших в список для удаления из словаря игроков
                    self.losers.append(player)
                    # break
        # удаляем проигравших
        for loser in self.losers:
            self.players.pop(loser.name)
        # удаляем список проигравших, т.к. мы их только что удалили
        self.losers = []

    def cards_show(self):
        for player in self.players.values():
            player.card.show()

    def stats_show(self):
        for player in self.players.values():
            player.stats()

    def check_winner(self):

        # Составляем список победителей, если они есть
        for player in self.players.values():
            if player.is_winner:
                self.winners.append(player)

        if len(self.winners) > 1:
            print(f'\nНИЧЬЯ!!! Победили {[winner.name for winner in self.winners]}!')
            return True
        elif self.winners:
            print(f'ПОБЕДИЛ {self.winners[0].name}!')
            return True

        return False

    def __str__(self):
        str_game = f'\nПАРАМЕТРЫ ИГРЫ:\nЧисло игроков: {self.num_users + self.num_computers} \n' \
                   f'- реальный человек: {self.num_users}\n- искуственный интелект: {self.num_computers}\n' \
                   f'Число боченков: {len(self.bag.nums)}\nНомеров в каждой карточке: {15}\n' \
                   f'Чило победителей: {len(self.winners)}\nИмена победителей: {self.winners}\n' \
                   f'Чило проигравших: {len(self.losers)}\nИмена проигравших: {self.losers}\n'

        return str_game

    def __eq__(self, other):
        return (self.num_users == other.num_users) \
               and (self.num_computers == other.num_computers) \
               and (self.winners == other.winners) \
               and (self.losers == other.losers) \
               and (self.bag == other.bag) \
               and (self.players == other.players)

    def __len__(self):
        return len(self.players)


if __name__ == '__main__':
    import copy

    print('\nРаспечатываем объект класса Bag')
    bag = Bag()
    print(bag)

    print('\nРаспечатываем объект класса Card')
    randomcard = RandomCard('Vika')
    print(randomcard)

    print('\nРаспечатываем объект класса Computer')
    computer = Computer('Computer')
    print(computer)

    print('\nРаспечатываем объект класса User')
    user = User('Макс')
    print(user)

    print('\nРаспечатываем объект класса Game')
    game = Game()
    print(game)

    # Проверка сравнения объектов класса Bag
    print('\nПроверка сравнения объектов класса Bag')

    bag1 = Bag()
    bag2 = Bag()
    print(bag1 == bag2)

    num3 = bag2.nums[3]
    bag2.nums[3] = 99
    print(bag1 == bag2)

    bag2.nums[3] = num3
    print(bag1 == bag2)

    # Проверка сравнения объектов класса Card
    print('\nПроверка сравнения объектов класса Card')

    randomcard1 = RandomCard('card1')
    randomcard2 = RandomCard('card1')
    randomcard3 = copy.copy(randomcard1)

    print(randomcard1 == randomcard2)
    print(randomcard2 == randomcard3)
    print(randomcard3 == randomcard1)

    # Проверка сравнения объектов класса Computer и User
    print('\nПроверка сравнения объектов класса Computer  и User')
    comp1 = Computer('comp')
    comp2 = Computer('comp')
    comp3 = copy.copy(comp1)

    user1 = User('user')
    user2 = User('user')
    user3 = copy.copy(user1)

    print(comp1 == comp2)
    print(comp2 == comp3)
    print(comp3 == comp1)

    print(user1 == user2)
    print(user2 == user3)
    print(user3 == user1)

    print(user1 == comp3)

    # Проверка сравнения объектов класса Game
    print('\nПроверка сравнения объектов класса Game')

    game1 = Game()
    game2 = Game()
    game3 = copy.copy(game1)

    print(game1 == game2)
    print(game2 == game3)
    print(game3 == game1)

    game2.number_users = 6

    print(game1 == game2)
    print(game2 == game3)
    print(game3 == game1)

    # Проверка наличия игрока с данным именем в объекте класса User
    print('\nПроверка наличия игрока с данным именем в объекте класса User')

    user1 = User('Вика')
    user2 = User('Макс')
    print('Вика' in user1)
    print('Вика' in user2)

    # Проверка наличия игрока с данным именем в объекте класса Computer
    print('\nПроверка наличия игрока с данным именем в объекте класса Computer')

    comp = Computer()
    print('Computer' in comp)

    # Проверка итерируемости списка незачеркнутых номеров в карточках игроков Computer и User
    print('\nПроверка итерируемости списка незачеркнутых номеров в карточках игроков Computer и User')

    usr = User()
    for num in usr:
        print(num)

    i = 5
    print(f'{i}-м числом на карточке {usr.name} является число {usr[i - 1]}')

    # Проверка длины объектов классов Bag, Card, Computer, User, Game
    print('\nПроверка длины объектов классов Bag, Card, Computer, User, Game')

    bag = Bag()
    randomcard = RandomCard('Игрок2')
    comp = Computer()
    user = User()
    game = Game()

    print(f'Длина объекта класса Bag = {len(bag)} боченков')
    print(f'Длина объекта класса Card = {len(randomcard)} незачеркнутых чисел')
    print(f'Длина объекта класса Computer = {len(comp)} незачеркнутых чисел')
    print(f'Длина объекта класса User = {len(user)} незачеркнутых чисел')
    print(f'Длина объекта класса Game = {len(game)} игроков')
