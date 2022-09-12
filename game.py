from random import sample


class Bag:

    def __init__(self):
        self.numbers = sample(range(1, 91), 90)

    def next(self):
        if self.numbers:
            return self.numbers.pop()
        raise Exception('Мешок пуст!')

    def stats(self):
        print(f'В мешке {len(self.numbers)} боченков.')


class RandomCard:

    def __init__(self, name):
        self.player_name = name
        # генерация чисел для карточки
        self.card_numbers = sample(range(1, 91), 15)
        # генерация мест для этих чисел на карточке
        self.place_idx = sample(range(0, 9), 5) + sample(range(9, 18), 5) + sample(range(18, 27), 5)
        # print(place_idx)

        # словарь {№места: число}
        self.card = {key: 0 for key in range(27)}
        for i in range(len(self.card_numbers)):
            self.card[self.place_idx[i]] = self.card_numbers[i]

    def modify(self, number):
        del_idx = self.place_idx[self.card_numbers.index(number)]
        self.card[del_idx] = None

    def show(self):

        # печать карточки
        print(f'\n-{self.player_name}{"-" * (26 - len(self.player_name) - 1)}')
        for i in range(len(self.card)):
            if self.card[i] is None:
                print('--', end='')
            elif self.card[i] == 0:
                print('  ', end='')
            elif self.card[i] < 10:
                print(f' {self.card[i]}', end='')
            else:
                print(self.card[i], end='')
            print() if i + 1 in (9, 18, 27) else print(' ', end='')
        print('-' * 26, end='\n')


class Computer:

    def __init__(self, name='Computer'):
        self.name = name
        self.randomcard = RandomCard(name)
        self.numbers = self.randomcard.card_numbers.copy()
        self.is_winner = False

    def motion(self, number):

        if number in self.randomcard.card_numbers:
            self.randomcard.modify(number)
            self.numbers.remove(number)
            self.is_winner = not self.numbers

    def stats(self):
        print(f'{self.name}. Осталось {len(self.numbers)} чисел : {self.numbers}')


class User(Computer):

    def __init__(self, name='User'):
        Computer.__init__(self, name)

        self.is_looser = False
        self.answers = ['y', 'n']

    def motion(self, number):
        answer = input(f'{self.name}, зачеркнуть цифру? (y/n) ')
        while answer not in self.answers:
            answer = input('Не понял вас... Зачеркнуть цифру? (y/n) ')
        if answer == 'y':
            if number in self.randomcard.card_numbers:
                self.randomcard.modify(number)
                self.numbers.remove(number)
                self.is_winner = not self.numbers
            else:
                self.is_looser = True
        elif answer == 'n':
            if number in self.randomcard.card_numbers:
                self.is_looser = True


class Game:

    def __init__(self):
        self.number_users = 0
        self.number_computers = 0
        self.players = {}
        self.bag = Bag()
        self.winners = []
        self.losers = []

    def generate_players(self, number_computers, number_users):

        for i in range(number_computers):
            pl_name = f'computer-{i + 1}'
            self.players[pl_name] = Computer(pl_name)

        for i in range(number_users):
            pl_name = f'user-{i + 1}'
            self.players[pl_name] = User(pl_name)

    def run(self, number_computers, number_users):
        self.number_computers = number_computers
        self.number_users = number_users

        self.generate_players(number_computers, number_users)
        self.cards_show()

        while True:
            number = self.bag.next()

            print(f'Из мешка вынут боченок номер {number}!')

            self.motion(number)

            if self.number_users == 0 and self.number_computers == 0:
                print('\nИГРА ОКОНЧЕНА')
                break

            self.cards_show()
            self.stats_show()

            self.bag.stats()

            if self.check_winner():
                break
            else:
                print('Игра продолжается...\n')

    def motion(self, number):
        for player in self.players.values():
            player.motion(number)
            if isinstance(player, User):
                if player.is_looser:
                    print(f'\nСОЖАЛЕЮ, {player.name}, но ВЫ ПРОИГРАЛИ... Нужно быть внимательнее!')
                    self.number_users -= 1
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


if __name__ == '__main__':
    pass
