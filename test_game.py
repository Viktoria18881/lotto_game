import unittest
from game import Bag, RandomCard, Computer, User, Game


class TestBag (unittest.TestCase):

    def test_bag_unit(self):
        bag = Bag()
        assert min(bag.numbers) > 0
        assert max(bag.numbers) < 91
        assert len(bag.numbers) == 90

    def test_bag_next(self):
        bag = Bag()
        assert bag.numbers[-1] == bag.next()


class TestRandomCard (unittest.TestCase):

    def test_randomcard_unit(self):
        randomcard = RandomCard('Vika')

        assert randomcard.player_name == 'Vika'

        assert min(randomcard.card_numbers) > 0
        assert max(randomcard.card_numbers) < 91
        assert len(randomcard.card_numbers) == 15

        assert min(randomcard.place_idx) >= 0
        assert max(randomcard.place_idx) < 27
        assert len(randomcard.place_idx) == 15

        assert len(randomcard.card.items()) == 27

    def test_card_modify(self):
        randomcard = RandomCard('Vika')

        assert randomcard.card[randomcard.place_idx[0]] == randomcard.card_numbers[0]

        randomcard.modify(randomcard.card_numbers[0])
        assert randomcard.card[randomcard.place_idx[0]] is None


class TestComputer (unittest.TestCase):

    def test_computer_init(self):
        computer = Computer()
        assert computer.name == 'Computer'
        computer = Computer('Vika')
        assert computer.name == 'Vika'
        del computer

    def test_randomcard(self):
        computer = Computer()
        assert computer.randomcard.player_name == 'Computer'
        del computer

    def test_computer_numbers(self):
        computer = Computer()
        assert computer.numbers == computer.randomcard.card_numbers
        del computer

    def test_computer_is_winner(self):
        computer = Computer()
        assert computer.is_winner is False
        del computer

    def test_computer_motion(self):
        computer = Computer()
        number = computer.numbers[0]
        assert number in computer.numbers
        computer.motion(number)
        assert number not in computer.numbers
        del computer

    def test_computer_stats(self):
        computer = Computer()
        assert bool(computer.name) is True
        assert type(computer.name) is str
        assert len(computer.numbers) >= 0
        assert type(computer.numbers) is list
        assert type(computer.numbers[0]) is int
        del computer


class TestUser (unittest.TestCase):

    def test_user_init(self):
        user = User()
        assert user.name == 'User'
        user = User('Sara')
        assert user.name == 'Sara'
        assert user.is_looser is False
        assert user.answers[0] == 'y'
        assert user.answers[1] == 'n'
        assert len(user.answers) == 2
        del user


class TestGame (unittest.TestCase):

    def test_game_init(self):
        game = Game()
        assert game.number_users == 0
        assert game.number_computers == 0
        assert game.players == {}
        assert isinstance(game.bag, Bag)
        assert len(game.bag.numbers) == 90
        assert game.winners == game.losers

    def test_game_generate_players(self):
        game = Game()
        game.generate_players(1, 1)
        assert len(game.players) == 2
        assert 'computer-1' in game.players.keys()
        assert 'user-1' in game.players.keys()
        assert 'computer-2' not in game.players.keys()
        assert 'user-2' not in game.players.keys()
        assert isinstance(game.players['computer-1'], Computer)
        assert isinstance(game.players['user-1'], User)
        game.generate_players(2, 2)
        assert len(game.players) == 4

    def test_game_check_winner(self):
        game = Game()
        assert game.check_winner() is False
        assert len(game.winners) == 0
        user = User()
        game.winners.append(user)
        user.is_winner = True
        assert game.check_winner() is True
