from collections import deque
import math
import flappy
import globals

def sigmoid(x):
  return 1 / (1 + math.exp(-x))

class NeuralNet():


    current_vals = {}  #{(node,value)...}

    def __init__(self,genome):
        self.inn_nodes = genome.ins
        self.out_nodes = genome.outs
        nodes =  deque(genome.get_hidden_nodes())
        self.network = [] #[(outNode,{(inNode,weight)...})...]
        while nodes:
            node1 = nodes.popleft()
            possible = True
            if not globals.RECURRENT_CONNECTIONS:
                for node2 in nodes:
                    if genome.dependent_rec(node2,node1):
                        possible = False
            if possible:
                self.add_neuron(genome,node1)
            else:
                nodes.append(node1)
        for node in self.out_nodes:
            self.add_neuron(genome,node)
        self.reset()

    def add_neuron(self,genome,node):
        self.network.append((node,[]))
        input_genes = genome.node_input_genes(node)
        for gene in input_genes:
            if gene.expressed:
                self.network[-1][1].append((gene.link.inp,gene.weight))

    def run(self,*inputs):
        if not globals.RECURRENT_CONNECTIONS: #not actually needed
            self.reset()
        for i in xrange(len(self.inn_nodes)):
            self.current_vals[self.inn_nodes[i]]=inputs[i]
        for i in xrange(len(self.network)):
            sum = 0
            for input in self.network[i][1]:
                sum += self.current_vals[input[0]]*input[1]
            self.current_vals[self.network[i][0]]=sigmoid(sum)
        outputs = []
        for out_node in self.out_nodes:
            outputs.append(self.current_vals[out_node])

        return outputs

    def reset(self):
        for node in self.network:
            self.current_vals[node[0]]=0

def test_genome(genome):
    sum = 0
    net = NeuralNet(genome)
    for i in xrange(globals.NUM_TESTS):
        sum += flappy.test_network(net,NeuralNet.run)
    return sum/globals.NUM_TESTS












def main():
    """
    Add Documentation here
    """
    pass  # Add Your Code Here


if __name__ == '__main__':
    main()