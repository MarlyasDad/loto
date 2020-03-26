from loto.core import LotoGame

if __name__ == '__main__':
    computers_count = 1
    humans_count = 1

    game = LotoGame(computers_count, humans_count)
    game.run()
