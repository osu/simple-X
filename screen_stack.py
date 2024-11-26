import sqlite3
import os.path
from tkinter import messagebox
import sys
from exceptions import EmptyStackAccessException


class ScreenStack:
    def __init__(self):
        self.length = 0
        self.screens = []

    def push(self, item):
        # print(item)
        # print("Received")
        self.screens.append(item)
        self.length += 1

    def pop(self):
        if self.length == 0:
            raise EmptyStackAccessException()
        else:
            self.returned_item = self.screens.pop()
            self.length -= 1
            return self.returned_item

    def peek(self):
        if self.length == 0:
            raise EmptyStackAccessException()
        else:
            return self.screens[self.length - 1]

    def __len__(self):
        return self.length

    def clear(self):
        self.screens.clear()
        self.length = 0

    def print(self):
        print("[", end="")
        for i in range(self.length):
            if i < self.length - 1:
                print(self.screens[i], ", ", end="", sep="")
            else:
                print(self.screens[i], end="")

        print("]")
