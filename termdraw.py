import curses
import dataclasses
import time
import traceback
from collections import namedtuple

from utils import Point

FULL_CHAR = "█"


f = open("error.log", "a+")


class Screen:
    stdscr = None

    def __enter__(self) -> "Screen":
        self.stdscr = curses.initscr()
        curses.start_color()
        curses.noecho()
        curses.cbreak()
        self.stdscr.nodelay(True)
        self.stdscr.keypad(True)
        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)  # APPLE 1 RED
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)  # SNAKE 2 GREEN
        curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_BLACK)  # NOTHING 3 BLACK
        curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_BLACK)  # WALL 4 WHITE
        curses.init_pair(5, curses.COLOR_YELLOW, curses.COLOR_BLACK)  # HEAD 5 WHITE
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.stdscr is not None:
            curses.nocbreak()
            curses.echo()
            curses.endwin()

    def draw_box_outline(self, size):
        for i in range(size):
            # f.write(str(stdscr.getyx()))
            self.stdscr.move(0, i)
            self.stdscr.addstr(FULL_CHAR)
            self.stdscr.move(i, 0)
            self.stdscr.addstr(FULL_CHAR)
            self.stdscr.move(i, size)
            self.stdscr.addstr(FULL_CHAR)
            self.stdscr.move(size, i)
            self.stdscr.addstr(FULL_CHAR)

    def draw_box(self, a: Point, b: Point, color_pair: int = 1):
        for x in range(a.x, b.x + 1):
            for y in range(a.y, b.y + 1):
                self.stdscr.addstr(y, x, FULL_CHAR, curses.color_pair(color_pair))

    def refresh(self):
        self.stdscr.refresh()

    def erase(self):
        self.stdscr.erase()

    def read_input(self) -> str:
        return self.stdscr.getch()

    def draw_screen(self, arr):
        for x in range(len(arr)):
            for y in range(len(arr[x])):
                if arr[x][y] == "apple":
                    self.stdscr.addstr(y + 1, x + 1, FULL_CHAR, curses.color_pair(1))
                if arr[x][y] == "snake":
                    self.stdscr.addstr(y + 1, x + 1, FULL_CHAR, curses.color_pair(2))
                if arr[x][y] == "empty":
                    self.stdscr.addstr(y + 1, x + 1, FULL_CHAR, curses.color_pair(3))
                if arr[x][y] == "head":
                    self.stdscr.addstr(y + 1, x + 1, FULL_CHAR, curses.color_pair(5))

    def add_char(self, char: str, point: Point, color_pair: int):
        try:
            self.stdscr.addstr(point[1], point[0], char, curses.color_pair(color_pair))
        except Exception as e:
            # Happens when drawing out of bounds
            # TODO: Do sth about it
            pass

    def add_pixel(self, point: Point, color_pair: int):
        self.add_char(FULL_CHAR, point, color_pair)
