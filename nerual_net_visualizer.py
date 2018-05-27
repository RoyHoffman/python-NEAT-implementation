import neural_net
import pygame


DEFAULT_NODE_RADIUS = 20
MIN_VERTICAL_SPACING_CO = 3
MIN_HORIZONTAL_SPACING_CO = 6

HIDDENS_TO_INOUTS = +2
OPTIMAL_RATIO = 1/3 #hieght to width

TRY_DECREASE = 1

MIN_WIDTH = 600
MiIN_HIEGHT = 300
MAX_WIDTH = 1200
MAX_HIEGHT = 700

NODE_COLOR = (0,0,0)
EDGE = 2
BACKGROUND = (255,255,255)


def visualize_genome(genome):
    visualize_network(neural_net.NeuralNet(genome))

def visualize_network(neural_net):
    ins = len(neural_net.inn_nodes)
    outs = len(neural_net.out_nodes)
    hiddens = len(neural_net.genome.hiddens.keys())

    basic_vertical = max(ins,outs)

    node_radius = DEFAULT_NODE_RADIUS

    basic_hieght = basic_vertical*node_radius*MIN_VERTICAL_SPACING_CO

    official_hieght = 0
    while((basic_vertical+1)*node_radius*MIN_VERTICAL_SPACING_CO > MAX_HIEGHT):
        node_radius -= TRY_DECREASE
        official_hieght = (basic_vertical+1)*node_radius*MIN_VERTICAL_SPACING_CO

    square_attempt = int(hiddens**0.5 + 0.1)
    vertical = square_attempt
    horizontal = square_attempt
    last_horizontal = 0
    if(hiddens - square_attempt**2):
        vertical += 1
        last_horizontal = hiddens - vertical*(horizontal-1)
        while(last_horizontal > vertical):
            horizontal += 1
            last_horizontal -= vertical
        if not last_horizontal: horizontal -= 1

    while((vertical+1)*node_radius*MIN_VERTICAL_SPACING_CO > MAX_HIEGHT):
        vertical -= 1
        if last_horizontal: last_horizontal +=  (horizontal-1)*vertical
        else : last_horizontal +=  horizontal*vertical
        while(last_horizontal > vertical):
            last_horizontal - vertical
            horizontal += 1
        if not last_horizontal: horizontal -= 1
        official_hieght = (vertical+1)*node_radius*MIN_VERTICAL_SPACING_CO

    official_wiedth = 0
    horizontal += 2
    while((horizontal+1)*node_radius*MIN_HORIZONTAL_SPACING_CO > MAX_WIDTH):
        node_radius -= TRY_DECREASE
        official_wiedth = (horizontal+1)*node_radius*MIN_HORIZONTAL_SPACING_CO



    horizontal_spacing = node_radius*MIN_HORIZONTAL_SPACING_CO
    if not official_wiedth:
        official_wiedth = (horizontal+1)*node_radius*MIN_HORIZONTAL_SPACING_CO
        if official_wiedth < MIN_WIDTH:
            official_wiedth = MIN_WIDTH
            horizontal_spacing = official_wiedth/(horizontal+1)

    if not official_hieght:
        official_hieght = (vertical+1)*node_radius*MIN_VERTICAL_SPACING_CO
        if official_hieght < MiIN_HIEGHT:
            official_hieght = MiIN_HIEGHT

    pygame.init()
    screen = pygame.display.set_mode((official_wiedth, official_hieght))
    nodes = {} #{(node:x,y)}
    x = horizontal_spacing
    screen.fill(BACKGROUND)
    draw_collumn(screen,nodes,official_hieght,node_radius,x,neural_net.inn_nodes)
    counter = 0
    draw_nodes= []
    for node in neural_net.genome.hiddens.keys():
        draw_nodes.append(node)
        counter += 1
        if counter == vertical:
            x += horizontal_spacing
            draw_collumn(screen,nodes,official_hieght,node_radius,x,draw_nodes)
            counter = 0
            draw_nodes= []
    if draw_nodes:
        x += horizontal_spacing
        draw_collumn(screen,nodes,official_hieght,node_radius,x,draw_nodes)
    x += horizontal_spacing
    draw_collumn(screen,nodes,official_hieght,node_radius,x,neural_net.out_nodes)

    genes = neural_net.genome.genes
    for gene in genes:
        if gene.expressed:
            pygame.draw.line(screen,NODE_COLOR,(nodes[gene.link.inp][0]+node_radius,nodes[gene.link.inp][1]),(nodes[gene.link.out][0]-node_radius,nodes[gene.link.out][1]),EDGE)



    pygame.display.flip()
    #draw_arrows

    wait()





def wait():
    wait = True
    while wait:
        for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                            wait = False



def draw_collumn(screen,existing_nodes,hieght,node_radius,x,draw_nodes):
    '''
    if(len(draw_nodes)+1)*node_radius*MIN_VERTICAL_SPACING_CO >= hieght:
        vertical_spacing = node_radius*MIN_VERTICAL_SPACING_CO
        start_y = vertical_spacing
    else:
    '''
    vertical_spacing = hieght/(len(draw_nodes)+1)
    y = vertical_spacing
    for node in draw_nodes:
        existing_nodes[node] = (x,y)
        pygame.draw.circle(screen,NODE_COLOR,(x,y),node_radius,EDGE)
        y += vertical_spacing






















