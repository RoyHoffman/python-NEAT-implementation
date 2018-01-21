# -*- coding: utf-8 -*-
import random_funcs
import random
import globals
import math



class Species(object):



    genomes = []
    max_fit = 0
    unimproved = 0
    adjusted_fitness = 0.0
    num_children = 0

    def __init__(self,proto):
        self.proto = proto
        self.genomes = [proto]

    def add_if_close(self,genome):
        not_matching = 0.0
        weight_dif = 0.0
        for gene1 in genome.genes:
            for gene2 in self.proto.genes:
                if gene1.inn_num == gene2.inn_num:
                    weight_dif += abs(gene1.weight - gene2.weight)
                    break
            else:
                not_matching += 1
        not_matching /= max(len(self.proto.genes),len(genome.genes))
        if globals.MAX_DIST > not_matching*globals.NOT_MATCHING_GENE_COEFFICIENT + weight_dif*globals.WEIGHT_DIF_COEFFICIENT:
            self.genomes.append(genome)
            return True
        return False

    def next_gen(self):
        if self.genomes:
            self.proto = random.choice(self.genomes)
            self.genomes = []
            return True
        return False

    def extinct(self):
        if not self.genomes:
            return True
        self.unimproved += 1
        for genome in self.genomes:
            if genome.fit > self.max_fit:
                self.max_fit=genome.fit
                self.unimproved = 0
        if self.unimproved > globals.MAX_UNIMPROVED:
            return True
        return False

    def calculate_adjusted_fitness(self):
        # should try out both ways!!!!!
        fitness = 0
        for genome in self.genomes:
            fitness += genome.fit
        if fitness == 0:
            self.adjusted_fitness = 0
            return
        fitness /= len(self.genomes)
        self.adjusted_fitness = fitness #/ len(self.genomes)

    def calculate_children(self,total_adjusted_fitness,s_num,pop_size):
        if total_adjusted_fitness == 0:
            self.num_children = int(math.floor(pop_size/s_num))
        elif self.adjusted_fitness == 0:
            self.num_children = 0
        else:
            self.num_children = int(math.floor(pop_size*(self.adjusted_fitness/total_adjusted_fitness)))
        return self.num_children

    def create_children(self):
        if self.max_fit > 0.9:
            pass
        children = []
        num_parents = max(int(math.ceil(len(self.genomes)*globals.TOP_PRECENTAGE)),globals.MIN_PARENTS)
        self.genomes.sort(key= lambda genome: genome.fit,reverse=True)
        if num_parents < len(self.genomes):
            self.genomes = self.genomes[:num_parents]
        for i in range(self.num_children-1):
            children.append(Genome(random.choice(self.genomes),(random.choice(self.genomes))).mutate())
        #children = [Genome(random.choice(self.genomes),(random.choice(self.genomes))).mutate() for i in range(self.num_children-1)]
        children.append(self.genomes[0])
        return children

    def __str__(self):
        return str([str(genome)+"\n" for genome in self.genomes])+"\n----------------------"

    def __repr__(self):
        return str([str(genome)+"\n" for genome in self.genomes])+"\n----------------------"










class Genome(object):
    global_inn_num = -1
    global_node_num = 0
    global_existing_links = {}
    global_hidden_nodes = {}
    ins = []
    outs = []
    hiddens = {} #num to set of nums
    genes = []

    def __init__(self,parent1=None,parent2=None):
        if parent2:
            self.mate_init(parent1,parent2)
        else:
            self.default_init()


    def mate_init(self,parent1=None,parent2=None):
        #self.genes = [random.choice([g1,g2]) for g1 in parent1.genes for g2 in parent2.genes if g1.inn_num==g2.inn_num]
        """
        """
        self.hiddens = {} #num to set of nums
        self.genes = []
        if parent1.fit > parent2.fit:
            fit_parent = parent1
            worse_parent = parent2
        else: #same fitness picks random parent, change in the future maybe
            fit_parent = parent2
            worse_parent = parent2
        for fit_gene in fit_parent.genes:
            for worse_gene in worse_parent.genes:
                if fit_gene.inn_num == worse_gene.inn_num:
                    self.genes.append(random.choice([fit_gene,worse_gene]))
                    break
            else:
                self.genes.append(fit_gene)
        self.hiddens=fit_parent.hiddens

    @staticmethod
    def set_ins_and_outs(in_num,out_num):
        Genome.ins = range(in_num)
        Genome.outs = range(in_num,in_num+out_num)
        Genome.global_node_num = in_num+out_num
        return Genome.ins,Genome.outs

    @staticmethod
    def give_inn_num(link):
        if link in Genome.global_existing_links.keys():
            return Genome.global_existing_links[link]
        Genome.global_inn_num+=1
        Genome.global_existing_links[link] = Genome.global_inn_num
        return Genome.global_inn_num

    @staticmethod
    def give_node_num(link):
        if link in Genome.global_hidden_nodes.keys():
            return Genome.global_hidden_nodes[link]
        Genome.global_node_num+=1
        Genome.global_hidden_nodes[link] = Genome.global_node_num
        return Genome.global_node_num


    @staticmethod
    def reset_gen_links():
        ''' optional '''
        Genome.global_existing_links = {}

    @staticmethod
    def reset_gen_nodes():
        ''' optional '''
        Genome.global_existing_nodes = {}

    #y = 0
    def default_init(self):
        #self.genes = [Gene(Link(inp,out),random_funcs.random_in_range(range))]
        self.hiddens = {} #num to set of nums
        self.genes = []
        if globals.START_ALL_LINKS:
            for inp in Genome.ins:
                for out in Genome.outs:
                    self.genes.append(Gene(Link(inp,out),random_weight()))
        else:
            self.mutate_link()

    def __str__(self):
        return "<"+str([str(gene) for gene in self.genes])+">\n"

    def __repr__(self):
        return "<"+str([str(gene) for gene in self.genes])+">\n"

    def fitness(self,fit):
        self.fit = fit


    def mutate_node(self):
        split_gene = random.choice(self.genes)
        split_gene.expressed = False
        split_link  = split_gene.link
        node_num = Genome.give_node_num(split_link)
        self.hiddens[node_num] = [split_link.inp]
        if split_link.out in self.hiddens.keys():
            self.hiddens[split_link.out].append(node_num)
        self.genes.append(Gene(Link(split_link.inp,node_num),1))
        self.genes.append(Gene(Link(node_num,split_link.out),1))

    def all_links(self):
        return [gene.link for gene in self.genes]

    def dependent(self,inp,out):
        if out in Genome.outs:
            return False
        return self.dependent_rec(inp,out)


    def dependent_rec(self,inp,out):
         if inp in Genome.ins:
             return False
         for inp2 in self.hiddens[inp]:
             if inp2 == out:
                 return True
             if self.dependent_rec(inp2,out):
                 return True
         return False

    def mutate_link(self):
        inns = Genome.ins+self.hiddens.keys()
        outs = Genome.outs+self.hiddens.keys()
        random.shuffle(inns)
        random.shuffle(outs)
        for inp in inns:
            for out in outs:
                link = Link(inp,out)
                if not self.link_exists(link) and  (globals.RECURRENT_CONNECTIONS or (inp != out and not self.dependent(inp,out))):
                    self.genes.append(Gene(link,random_weight()))
                    return True
        return False


    def link_exists(self,link):
        for gene in self.genes:
            if gene.link == link:
                return True
        return False

    def mutate_weights(self):
        for gene in self.genes:
            gene.mutate_weight()

    def mutate(self):
        if random_funcs.prob_of_event(globals.MUTATE_NODE_PROB):
            self.mutate_node()
        elif random_funcs.prob_of_event(globals.MUTATE_LINK_PROB):
            self.mutate_link()
        if random_funcs.prob_of_event(globals.MUTATE_WEIGHT_PROB):
            self.mutate_weights()
        return self

    def get_hidden_nodes(self):
        return self.hiddens.keys()



    def node_input_genes(self,node):
        genes = []
        for gene in self.genes:
            if gene.link.out == node:
                genes.append(gene)
        return genes









class Gene(object):
    def __init__(self,link,weight,expressed = True):
        self.link = link
        self.weight = weight
        self.inn_num = Genome.give_inn_num(link)
        self.expressed = expressed

        #maybe add mutations
    def mutate_weight(self):
        """

        :type self: object
        """
        if random_funcs.prob_of_event(globals.WEIGHT_OVERWRITE_MUTATION):
            self.weight = random_weight()
        else:
            i = random.choice([-1, 1])
            self.weight += self.weight*globals.WEIGHT_MUTATION_COEFFICIENT*i


    def __str__(self):
        return str(self.link)+"|"+str(round(self.weight,4))

    def __repr__(self):
        return str(self.link)+"|"+str(round(self.weight,4))



def random_weight():
    return random_funcs.random_in_range(globals.DEFAULT_RANGE)

class Link(object):
    def __init__(self,inp,out):
        self.inp = inp
        self.out = out

    def __eq__(self, other):
        return self.inp == other.inp and self.out == other.out

    def __hash__(self):
        return hash((self.inp,self.out))

    def __str__(self):
        return "("+str(self.inp)+","+str(self.out)+")"

    def __repr__(self):
        return "("+str(self.inp)+","+str(self.out)+")"










def main():


    pass



if __name__ == '__main__':
    main()