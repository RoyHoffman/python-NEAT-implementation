# -*- coding: utf-8 -*-
import random
import globals

def random_in_range(range):
    return round(random.random()*abs((range[0]-range[1]))+range[0],globals.MAX_DECIMAL_PRECISION)

def prob_of_event(prob):
    return prob > random.random()


def main():
    """
    Add Documentation here
    """
    pass  # Add Your Code Here


if __name__ == '__main__':
    main()