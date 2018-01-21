# -*- coding: utf-8 -*-
import flappy
import random
import warnings

calls = 0

def main():

    """
    Add Documentation here
    """
    warnings.filterwarnings("ignore")
    global calls
    c = Genome()
    while(True):
        calls = 0
        print flappy.test_network(c,30,Genome.trun)
    main()


class Genome(object):
    def trun(self,in1,in2,in3,in4):
        #print in1,in2,in3,in4
        global calls
        calls += 1
        #print calls
        return random.random()

    def flappy_run(self,in1,in2,in3,in4):
        if(self.trun(in1,in2,in3,in4)<0.05):
            return True
        return False

if __name__ == '__main__':
    main()