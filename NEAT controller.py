# -*- coding: utf-8 -*-
from genome_encoding import *
import globals
import random_funcs
#import flappy
import random
import neural_net
from copy import copy

import warnings

def sort_children(species,children):
    for child in children:
        for sp in species:
            if sp.add_if_close(child):
                break
        else:
            species.append(Species(child))
#what
def create_first_gen():
    children = []
    for i in xrange(globals.POPULATION_SIZE):
        children.append(Genome())
    return children

def test_all(species):
    for sp in species:
        for genome in sp.genomes:
            fit = neural_net.test_genome(genome) #build neural net, test it, assign fitness
            genome.fitness(fit)
            debug_fit_test(genome)
            #genome.fitness(random.random())
            pass

def debug_fit_test(genome):
    if genome.fit >= globals.FIT_CHECK:
        print str(genome.fit) + " did it" + str(genome)
        if raw_input() == "q":
            globals.FIT_CHECK += globals.FIT_INC

gen = 0

def print_stats(species):
    global gen
    gen += 1
    print "gen: "+str(gen) + "\ns: "+str(len(species))
    s = 0
    for sp in species:
        s += len(sp.genomes)
    print "g: "+str(s)+"\n------------------------"





def distribute_left_children(species,children_left):
    species.sort(key= lambda sp: sp.adjusted_fitness,reverse=True)
    for sp in species:
        sp.num_children += 1
        children_left -= 1
        if children_left <= 0:
            return

def topSpecies(species):
    if len(species) < 3:
        return species
    species.sort(key= lambda sp: sp.max_fit,reverse=True)
    return species [:globals.ALL_SPECIES_UNIMPROVED_PURGE]

def main():
    """
    Add Documentation here
    """
    genc  = 0
    warnings.filterwarnings("ignore")
    inn_list,out_list = Genome.set_ins_and_outs(3,1)
    species = []
    children = create_first_gen()
    print children
    max_fit = 0
    while(True):
        genc += 1
        sort_children(species,children)
        #print species
        #print ";;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;"
        test_all(species)
        total_adjusted_fitness = 0
        for sp in species:
            sp.calculate_adjusted_fitness()
            total_adjusted_fitness += sp.adjusted_fitness
        w = 0
        species = [sp for sp in species if not sp.is_empty()]
        species_left = [sp for sp in species if not sp.extinct()]
        species = species_left if len(species_left)>0 else topSpecies(species)
        print_stats(species)

        children = []
        s_num = len(species)
        children_left = globals.POPULATION_SIZE
        for sp in species:
            children_left -= sp.calculate_children(total_adjusted_fitness,s_num,globals.POPULATION_SIZE)
        if children_left > 0:
            distribute_left_children(species,children_left)
        for sp in species:
            children.extend(sp.create_children())
            sp.next_gen()





        Genome.reset_gen_links()
        Genome.reset_gen_nodes()
        if globals.STOP:
            globals.iteration+=1
            if globals.iteration % globals.STOP_EVERY == 0:
                raw_input();
                print children
                raw_input();








    pass  # Add Your Code Here



if __name__ == '__main__':
    main()