import unittest
from game import Bag, RandomCard, Computer, User, Game


class TestBag (unittest.TestCase):

    def test_bag_unit(self):
        bag = Bag()
        assert min(bag.nums) > 0
        assert max(bag.nums) < 91
        assert len(bag.nums) == 90

    def test_bag_next(self):
        bag = Bag()
        assert bag.nums[-1] == bag.next()


class TestRandomCard (unittest.TestCase):

    def test_randomcard_unit(self):
        randomcard = RandomCard('Vika')

        assert randomcard.player_name == 'Vika'

        assert min(randomcard.randomcard_nums) > 0
        assert max(randomcard.randomcard_nums) < 91
        assert len(randomcard.randomcard_nums) == 15

        assert min(randomcard.place_idx) >= 0
        assert max(randomcard.place_idx) < 27
        assert len(randomcard.place_idx) == 15

        assert len(randomcard.randomcard.items()) == 27

    def test_card_modify(self):
        randomcard = RandomCard('Vika')

        assert randomcard.randomcard[randomcard.place_idx[0]] == randomcard.randomcard_nums[0]

        randomcard.modify(randomcard.randomcard_nums[0])
        assert randomcard.randomcard[randomcard.place_idx[0]] is None


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

    def test_computer_nums(self):
        computer = Computer()
        assert computer.nums == computer.randomcard.randomcard_nums
        del computer

    def test_computer_is_winner(self):
        computer = Computer()
        assert computer.is_winner is False
        del computer

    def test_computer_motion(self):
        computer = Computer()
        num = computer.nums[0]
        assert num in computer.nums
        computer.motion(num)
        assert num not in computer.nums
        del computer

    def test_computer_stats(self):
        computer = Computer()
        assert bool(computer.name) is True
        assert type(computer.name) is str
        assert len(computer.nums) >= 0
        assert type(computer.nums) is list
        assert type(computer.nums[0]) is int
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
        assert game.num_users == 0
        assert game.num_computers == 0
        assert game.players == {}
        assert isinstance(game.bag, Bag)
        assert len(game.bag.nums) == 90
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
