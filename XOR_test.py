# -*- coding: utf-8 -*-

import globals
import math





def test_network(network,run,debug = False):
    fitness = 16
    fitness -= (abs(0-network.run(0,0,globals.BIAS)[0])*2)**2
    fitness -= (abs(1-network.run(1,0,globals.BIAS)[0])*2)**2
    fitness -= (abs(1-network.run(0,1,globals.BIAS)[0])*2)**2
    fitness -= (abs(0-network.run(1,1,globals.BIAS)[0])*2)**2


    if debug:
        print "here"
        a = 0
        a= network.run(0,0,globals.BIAS)[0]
        print str(a) + " expected: 0"
        a= network.run(1,0,globals.BIAS)[0]
        print str(a) + " expected: 1"
        a= network.run(0,1,globals.BIAS)[0]
        print str(a) + " expected: 1"
        a= network.run(1,1,globals.BIAS)[0]
        print str(a) + " expected: 0"
        raw_input()

    return fitness**2






def main():
    """
    Add Documentation here
    """

    pass  # Add Your Code Here


if __name__ == '__main__':
    main()