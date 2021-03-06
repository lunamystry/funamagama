#! /usr/bin/env python
"""
author: Leonard Mbuli <mail@mandla.me>

creation date: 13 December 2014
update date: 16 December 2014

"""
import pytest

from generate import Grid
from generate import Word

def test_words_cant_be_less_than_2():
    '''
        If words are less than 2 characters you have letters
    '''
    with pytest.raises(ValueError):
        Word('a', None, None)

def test_place_returns_list_if_successful():
    '''
        Can I place a word on the grid
    '''
    grid = Grid(5, 5)
    res = grid.place('monty')
    assert(res == [])

def test_place_returns_list_of_words_not_placed():
    '''
        What if some words don't fit into the grid?
    '''
    grid = Grid(5, 5)
    res = grid.place('monty', 'python')
    assert(res == ['python'])

def test_can_select_the_directions_to_place_in():
    '''
        What if I don't want diagonal placement of words
    '''
    grid = Grid(5, 5)
    res = grid.place('monty', 'python', directions=['EAST'])
    assert(res == ['python'])

def test_can_place_words_multiple_times_without_overlap():
    '''
        I would like to be able to place the same word multiple times,
        this is not really a test when I think I about it
    '''
    grid = Grid(5, 5)
    res = grid.place('monty', 'monty', 'monty', 'monty', 'monty',
            directions=['SOUTH'])
    assert(res == [])

