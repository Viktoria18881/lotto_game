from random import randint, shuffle, sample

class Bag:

    def __init__(self):
        self.number = sample(range(1, 91), 90)

    def next(self):
        if self.number:
            return self.number.pop()
        raise Exception('Мешок пуст!')

    def stats(self):
        print(f'В мешке {len(self.number)} боченков.')

class RandomCard:

    #карточка с номерами бочонков и мест
    def __init__(self, name):
        self.player_name = name
        # генерация чисел для карточки
        self.card_number = sample(range(1, 91), 15)
        # генерация мест для этих чисел на карточке
        self.place_idx = sample(range(0, 9), 5) + sample(range(9, 18), 5) + sample(range(18, 27), 5)
        # print(place_idx)

        # словарь {№места: число}
        self.randomcard = {key: 0 for key in range(27)}
        for i in range(len(self.card_number)):
            self.randomcard[self.place_idx[i]] = self.card_number[i]

        # модификация в словаре
        def modify(self, num):
            del_idx = self.place_idx[self.card_number.index(num)]
            self.randomcard[del_idx] = None

        def show(self):

            # печать карточки
            print(f'\n-{self.player_name}{"-" * (26 - len(self.player_name) - 1)}')
            for i in range(len(self.randomcard)):
                if self.randomcard[i] is None:
                    print('--', end='')
                elif self.randomcard[i] == 0:
                    print('  ', end='')
                elif self.randomcard[i] < 10:
                    print(f' {self.randomcard[i]}', end='')
                else:
                    print(self.randomcard[i], end='')
                print() if i + 1 in (9, 18, 27) else print(' ', end='')
            print('-' * 26, end='\n')


class Computer:

    def __init__(self, name=' Компьютер'):
        self.name = name
        self.randomcard = RandomCard(name)
        self.number = self.randomcard.card_number.copy()
        self.is_winner = False

    def motion(self, num):
        if num in self.randomcard.card_number:
            self.randomcard.modify(num)
            self.number.remove(num)
            self.is_winner = not self.number

    def stats(self):
        print(f'{self.name}. Осталось {len(self.number)} чисел : {self.number}')


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
            if num in self.randomcard.card_number:
                self.randomcard.modify(num)
                self.number.remove(num)
                self.is_winner = not self.number
            else:
                self.is_looser = True
        elif answer == 'n':
            if num in self.randomcard.card_number:
                self.is_looser = True


class Game:
    def __init__(self):
        self.num_users = 0
        self.num_computers = 0
        self.players = {}
        self.bag = Bag()
        self.winners = []
        self.losers = []

    def generate_players(self, num_computers, num_users):

        for i in range(num_computers):
            pl_name = f'computer-{i + 1}'
            self.players[pl_name] = Computer(pl_name)

        for i in range(num_users):
            pl_name = f'user-{i + 1}'
            self.players[pl_name] = User(pl_name)

    def run(self, num_computers, num_users):
        self.num_computers = num_computers
        self.num_users = num_users

        self.generate_players(num_computers, num_users)
        self.cards_show()

        while True:
            num = self.bag.next()

            print(f'Из мешка вынут боченок номер {num}!')

            self.step(num)

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

    def step(self, num):
        for player in self.players.values():
            player.step(num)
            if isinstance(player, User):
                if player.is_looser:
                    print(f'\nСОЖАЛЕЮ, {player.name}, но ВЫ ПРОИГРАЛИ... Нужно быть внимательнее!')
                    self.num_users -= 1
                    # заносим лузеров в список для удаления из словаря игроков
                    self.losers.append(player)
                    # break
        # удаляем лузеров
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


if __name__ == '__main__':
    pass