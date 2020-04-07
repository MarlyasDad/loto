import pytest

from loto.core import Config, Bag, Card, Player, NumberInfo


class TestConfig:
    # TEST 1 Config.init_parameters()
    @pytest.mark.parametrize('argv, answers', [
        pytest.param(
            ['-c', '2', '-h', '1'], {'c': 2, 'h': 1},
            id="complete params 1",
        ),
        pytest.param(
            ['-c', '0', '-h', '3'], {'c': 0, 'h': 3},
            id="complete params 2",
        ),
        pytest.param(
            ['-c', '1'], {'c': 1},
            id="incomplete params 1",
        ),
        pytest.param(
            ['-h', '1'], {'h': 1},
            id="incomplete params 2",
        ),
        pytest.param(
            ['-h', '-c', '1'], {'h': 0, 'c': 1},
            id="incomplete params 3",
        ),
    ])
    def test_init_parameters(self, argv, answers):
        # Create class with parameters
        config = Config(argv)
        if 'c' in answers.keys():
            assert config.computers == answers['c']
        if 'h' in answers.keys():
            assert config.humans == answers['h']

    # TEST 2 Config.init_from_argv(argv)
    @pytest.mark.parametrize('argv', [
        pytest.param(
            ['-c', 'qwerty', '-h', '1'],
            id="incorrect complete params",
        ),
        pytest.param(
            ['-c', '-h', 'qwerty'],
            id="incorrect incomplete params",
        ),
    ])
    def test_init_from_argv_exceptions(self, argv):
        config = Config(['-c', '1', '-h', '1'])
        with pytest.raises(ValueError):
            config.init_from_argv(argv)

    # TEST 3 Config.init_from_keyboard()
    def test_init_from_keyboard(self, monkeypatch):
        # Simulating keyboard input
        monkeypatch.setattr('builtins.input', lambda x: "1")
        # Creating class without parameters
        config = Config()
        # Checking values
        assert config.computers == 1
        assert config.humans == 1


class TestBag:

    # TEST 4 Bag.get_barrel()
    def test_get_barrel(self):
        bag = Bag()
        for _ in range(90):
            barrel = bag.get_barrel()
            assert isinstance(barrel, int)
            assert 1 <= barrel <= 90


class TestCard:
    def setup_class(self):
        self.card = Card()

    # TEST 5 Card.fill_slots()
    def test_fill_slots(self):
        assert len(self.card.slots) == 15
        assert len(self.card.numbers_info) == 15

    # TEST 6 Card.get_slots()
    def test_get_slots(self):
        for line in range(3):
            slots = self.card.get_slots(line)
            assert len(slots) == 5


class TestPlayer:
    def setup_class(self):
        self.player = Player('Test player')
        self.player.type = 'human'
        # Переопределяем карточку
        new_slots = {x: x for x in range(1, 16)}
        self.player.card.slots = new_slots
        new_numbers_info = {x: NumberInfo(x, 1, x) for x in range(1, 16)}
        self.player.card.numbers_info = new_numbers_info

    # TEST 7 Player.auto_step(number: int)
    def test_auto_step_true(self):
        for i in range(1, 16):
            success = self.player.auto_step(i)
            assert success
            assert self.player.card.remained == 15 - i

    # TEST 8 Player.auto_step(number: int)
    def test_auto_step_false(self):
        out_of_range_index = 16
        success = self.player.auto_step(out_of_range_index)
        assert not success
