import sys
from loto.core import LotoGame, Config


def main():
    config = Config(sys.argv)
    # Or enter the parameters manually
    # config.computers = 2
    # config.humans = 2
    game = LotoGame(config)
    game.run()


if __name__ == '__main__':
    main()
