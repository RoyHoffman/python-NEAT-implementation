# -*- coding: utf-8 -*-
import random

def random_in_range(range):
    return random.random()*abs((range[0]-range[1]))+range[0]

def prob_of_event(prob):
    return prob > random.random()


def main():
    """
    Add Documentation here
    """
    pass  # Add Your Code Here


if __name__ == '__main__':
    main()