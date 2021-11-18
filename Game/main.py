from src.screen import FlappyWindow
from pyglet import app
import sys


def main(mode: str, gen_size: int = None) -> None:
    FlappyWindow(mode=mode, gen_size=gen_size)
    app.run()


def print_usage() -> None:
    with open("data//usage.txt") as file:
        print(file.read())


if __name__ == "__main__":
    if len(sys.argv) == 2:
        if sys.argv[1] == "--help" or sys.argv[1] == "-h":
            print_usage()
        elif sys.argv[1] == "--play" or sys.argv[1] == "-p":
            main("play")
        elif sys.argv[1] == "--learn" or sys.argv[1] == "-l":
            main("learn", gen_size=100)
    elif len(sys.argv) == 1:
        main("play")
    else:
        print_usage()
