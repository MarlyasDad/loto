from typing import Dict, List, Optional
from random import randint, choice


class NumberInfo:
    number: int
    is_used: bool
    line: int
    slot: Optional[int]

    def __init__(self, number: int, line: int, slot: int):
        self.number = number
        self.is_used = False
        self.line = line
        self.slot = slot


class Bag:
    barrels: list

    def __init__(self):
        self.barrels = [i for i in range(1, 91)]

    def get_barrel(self) -> int:
        number = choice(self.barrels)
        self.barrels.remove(number)
        return number


class Card:
    numbers_info: Dict[int, NumberInfo]
    slots: Dict[int, int]
    remained: int

    def __init__(self):
        self.numbers_info = dict()
        self.slots = dict()
        self.remained = 15
        self.fill_slots()

    def fill_slots(self):
        # Набираем 15 уникальных номеров бочонков
        card_numbers: list = []
        while len(card_numbers) < 15:
            new_number = randint(1, 90)
            if new_number in card_numbers:
                continue
            card_numbers.append(new_number)

        for line in range(3):
            line_idx = 5 * line
            # Получаем следующие 5 номеров и сортируем их
            line_numbers: list = card_numbers[0 + line_idx: 5 + line_idx]
            # Определяем 5 случайных слотов для текущей строки
            line_slots: list = self.get_slots(line)
            # Создаём бочонки и распределяем по строкам/слотам
            for number in sorted(line_numbers):
                # Расставляем значения по слотам
                slot_line = line
                slot_number = line_slots.pop(0)
                number_info = NumberInfo(number, slot_line, slot_number)
                self.slots[slot_number] = number
                self.numbers_info[number] = number_info

    @staticmethod
    def get_slots(line: int) -> list:
        line_indexes = 9 * line
        # Набираем 5 уникальных номеров слотов в line-строке
        slots_numbers: list = []
        while len(slots_numbers) < 5:
            new_slot = randint(0 + line_indexes, 8 + line_indexes)
            if new_slot in slots_numbers:
                continue
            slots_numbers.append(new_slot)
        return sorted(slots_numbers)


class Player:
    id: str
    type: str
    card: Card
    name: str

    def __init__(self, name: str, player_type: str):
        self.card = Card()
        self.win = False
        self.name = name
        self.type = player_type

    def auto_step(self, number: int) -> bool:
        if number in self.card.slots.values():
            self.card.numbers_info[number].is_used = True
            self.card.remained -= 1
            return True
        return False

    def check_step(self, user_choice: str, number: int) -> bool:
        success = self.auto_step(number)
        if user_choice == 'y' and success:
            return False
        elif user_choice == 'y' and not success:
            return True
        elif user_choice == 'n' and success:
            return True
        elif user_choice == 'n' and not success:
            return False
        else:
            return True


class InfoPrinter:
    players: List[Player]

    def __init__(self, players: List[Player]):
        self.players = players

    def print_all_cards(self):
        for player in self.players:
            print(f'Игрок: {player.name}')
            self.print_card(player.card)

    def print_card(self, card: Card):
        print('--------------------------')
        for i in range(27):
            number = card.slots.get(i)
            if number:
                used: bool = card.numbers_info[number].is_used
                self.pprint_number(number, used)
            else:
                print('  ', end=" ")
            if not (i + 1) % 9:
                print('')
        print('--------------------------')

    @staticmethod
    def pprint_number(number: int, is_used: bool):
        if not is_used:
            slot_end = ' '
            if number < 10:
                slot_end = '  '
            print(number, end=slot_end)
        else:
            print('--', end=" ")


class LotoGame:
    printer: InfoPrinter
    players: List[Player]
    bag: Bag
    play: bool

    def __init__(self, computers: int, humans: int):
        self.players = list()
        self.create_players(int(computers), humans)
        self.printer = InfoPrinter(self.players)
        self.bag = Bag()
        self.play = True

    def create_players(self, computers: int, humans: int):
        if computers > 0:
            for computer in range(computers):
                computer_name = f'Computer {computer + 1}'
                self.players.append(Player(computer_name, 'computer'))
                print(f'Искуственный интеллект {computer_name} создан')
        if humans > 0:
            for human in range(humans):
                name = input(f'Введите имя живого игрока {human + 1}: ')
                self.players.append(Player(name, 'human'))

    def run(self) -> None:
        print('Добро пожаловать в игру Лото')
        print('В этой игре участвуют: \n')
        self.printer.print_all_cards()
        print('Будьте осторожны, компьютер никогда не ошибается!\n')
        input('Нажмите любую клавишу для начала игры: ')
        while self.play:
            # Достаём бочонок из мешка
            barrel = self.bag.get_barrel()
            print(f'Выпал бочонок № {barrel}')
            self.step(barrel)

    def step(self, barrel: int):
        # Делаем ходы по очереди
        for player in self.players:
            print(f'Ход игрока: {player.name}')
            if player.type == 'computer':
                player.auto_step(barrel)
            else:
                self.printer.print_card(player.card)
                user_choice = input(f'Зачеркнуть цифру {barrel}? Y/N: ').lower()
                loss = player.check_step(user_choice, barrel)
                if loss:
                    print(f'Игрок {player.name} выбывает из игры!')
                    self.players.remove(player)
                    continue
            self.printer.print_card(player.card)
            # Если карточка заполнена или остался один игрок
            if player.card.remained == 0 or len(self.players) == 1:
                self.play = False
                print(f'Поздравляем игрока {player.name} с ПОБЕДОЙ!!!')
                break


if __name__ == '__main__':
    game = LotoGame(1, 1)
    game.run()
