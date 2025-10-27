# -*- coding: utf-8 -*-
class Estado:
    def __init__(self, id):
        self.id = int(id)
    def __str__(self):
        return f"E{self.id}"

class Terminal:
    def __init__(self, sym):
        self.sym = sym
    def __str__(self):
        return self.sym

class NoTerminal:
    def __init__(self, name):
        self.name = name
    def __str__(self):
        return self.name

class Pila:
    def __init__(self):
        self._data = []
    def push(self, x):
        self._data.append(x)
    def pop(self):
        return self._data.pop()
    def top(self):
        return self._data[-1]
    def __str__(self):
        return "[" + " ".join(str(x) for x in self._data) + "]"
