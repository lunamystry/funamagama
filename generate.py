#! /usr/bin/env python
"""
author: Leonard Mbuli <mail@mandla.me>

creation date: 17 July 2014
update date: 25 December 2014

"""
from __future__ import print_function
from __future__ import unicode_literals

import random
import re
import string
import logging

from copy import copy
from collections import namedtuple

logging.basicConfig(level=logging.DEBUG,
                    format='%(message)s')

Point = namedtuple("Point", "row col")

class Word(object):
    def __init__(self, text, direction, grid):
        if len(text) < 2:
            raise ValueError("word '%s' is too short" % text)
        self.text = re.sub("["+string.punctuation+"\d]", "", text.lower(), 0, 0)
        self.direction = direction
        self.grid = grid

    @property
    def start(self):
        return self._start

    @start.setter
    def start(self, value):
        self._start = value
        self.points = self.calculate_points()

    def collision(self, second, max_overlap=None):# {{{
        '''
            Check if two words collide and cannot intersect
        '''
        if max_overlap is None:
            max_overlap = 30
        overlap = 0.0
        for i, p1 in enumerate(self.points):
            for j, p2 in enumerate(second.points):
                if p1 == p2 and self.text[i] != second.text[j]:
                    return True
                elif p1 == p2 and self.text[i] == second.text[j]:
                    overlap += 1.0
                    if 100*(overlap/min(len(self), len(second))) > max_overlap:
                        return True
        return False# }}}

    def calculate_points(self):
        row_incr, col_incr = self.increments()
        points = []
        row = self.start.row
        col = self.start.col
        points.append(Point(row, col))
        for letter in self.text[1:]:
            row += row_incr
            col += col_incr
            if (row < 0 or col < 0 or row > self.grid.rows or col > self.grid.cols):
                logging.debug("row:{0} col:{1}".format(row, col))
                raise IndexError("'" +self.text + "' is not completely inside grid")
            points.append(Point(row, col))
        return points

    def increments(self):
        col_incr = 0
        row_incr = 0
        if self.direction == 'EAST':
            col_incr = 1
        elif self.direction == 'WEST':
            col_incr = -1
        elif self.direction == 'SOUTH':
            row_incr = 1
        elif self.direction == 'NORTH':
            row_incr = -1
        elif self.direction == 'SOUTHEAST':
            row_incr = 1
            col_incr = 1
        elif self.direction == 'SOUTHWEST':
            row_incr = 1
            col_incr = -1
        elif self.direction == 'NORTHEAST':
            row_incr = -1
            col_incr = 1
        elif self.direction == 'NORTHWEST':
            row_incr = -1
            col_incr = -1
        return row_incr, col_incr

    def __str__(self):
        return self.text

    def __repr__(self):
        return self.text

    def __len__(self):
        return len(self.text)


class Grid():
    def __init__(self, rows, cols):# {{{
        '''
            create a grid with the given dimensions, and empty list of words
        '''
        self.rows = rows
        self.cols = cols
        self.words = []
        self._grid = self.init_grid(rows, cols)# }}}

    def init_grid(self, y, x):# {{{
        '''
            input: size of the grid
            returns: a list of strings representing the row of the grid
        '''
        bg = []
        alphabet = "abcdefghijklmnopqrstuvwxyz"
        for r in range(1, y + 1):
            row = []
            for c in range(1, x + 1):
                aindex = int(random.uniform(0, 26))
                row.append(alphabet[aindex])
            bg.append(row)
        return bg# }}}

    def place(self, *args, **kwargs):# {{{
        '''
            Tries to place the given string(s) on the grid in random directions
            and starting positions

            takes a list of strings to place
            and optionally, list of directions
        '''
        if 'directions' in kwargs:
            directions = kwargs['directions']
        else:
            directions = ['EAST', 'WEST', 'SOUTH', 'NORTH', 'NORTHEAST',
                    'NORTHWEST', 'SOUTHEAST', 'SOUTHWEST']
        not_placed = []

        for arg in args:
            dindex = int(random.uniform(0, len(directions)))
            word = Word(arg, directions[dindex], self)
            possible_starts = self.possible_starts(word)
            if possible_starts:
                sindex = int(random.uniform(0, len(possible_starts)))
                word.start = possible_starts[sindex]
                for i, point in enumerate(word.points):
                    self._grid[point.row][point.col] = word.text[i]
                    if word not in self.words:
                        self.words.append(word)
            else:
                not_placed.append(arg)

        return not_placed# }}}

    def possible_starts(self, word):# {{{
        '''
            find all the possible starts for the given word on the grid where
            it will not have a collision but may have an intersection.
        '''
        bounds = self.boundaries(word)
        within_bounds = []
        points = []
        collision_points = []
        for row in range(bounds.min_y, bounds.max_y):
            for col in range(bounds.min_x, bounds.max_x):
                point = Point(row, col)
                within_bounds.append(point)
        # Get collision points,
        for point in within_bounds:
            word.start = point
            for grid_word in self.words:
                if word.collision(grid_word):
                    collision_points.append(point)
        # filter points collision points
        for point in within_bounds:
            if point not in collision_points:
                points.append(point)
        return points# }}}

    def boundaries(self, word):# {{{
        '''
            Find all the positions which make sure the word is within the grid
        '''
        Bound = namedtuple('Bound', 'direction min_y max_y min_x max_x')
        bounds = {
                'EAST':
                Bound('EAST', 0,
                    len(self._grid), 0, len(self._grid[0]) - (len(word) - 1)),
                'WEST':
                Bound("WEST",
                    0, len(self._grid), len(word) - 1, len(self._grid[0])),
                'SOUTH':
                Bound("SOUTH", 0,
                    len(self._grid) - (len(word) - 1), 0, len(self._grid[0])),
                'NORTH':
                Bound("NORTH",
                    len(word) - 1, len(self._grid), 0, len(self._grid[0])),
                "SOUTHEAST":
                Bound("SOUTHEAST",
                    0, len(self._grid) - (len(word) - 1), 0,
                    len(self._grid[0]) - (len(word) - 1)),
                "NORTHWEST":
                Bound("NORTHWEST",
                    len(word) - 1, len(self._grid), len(word) - 1,
                    len(self._grid[0])),
                "SOUTHWEST":
                Bound("SOUTHWEST",
                    0, len(self._grid) - (len(word) - 1), len(word) - 1,
                    len(self._grid[-1])),
                "NORTHEAST":
                Bound("NORTHEAST",
                    len(word) - 1, len(self._grid), 0,
                    len(self._grid[0]) - (len(word) - 1))
                }
        return bounds[word.direction]# }}}

    def __str__(self):# {{{
        '''
            join up the grid so it can be shown
        '''
        grid_str = ""
        for row in self._grid:
            grid_str += " ".join(row)
            grid_str += "\n"
        return grid_str[:-1]# }}}

    def __repr__(self):
        return self.__str__()


if __name__ == '__main__':
    grid = Grid(20, 20)
    grid.place(*['leonard',
        'mandla',
        'phoebie',
        'book',
        'classic',
        'homecoming',
        'breast',
        'sibling',
        'war',
        'sand',
        'diary',
        'door',
        'cocky',
        'perfect',
        'nothing',
        'coven'])
    print(grid)
    print(grid.words)
