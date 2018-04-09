#!/usr/local/bin/python3
import queue, random, argparse
import networkx as nx
import matplotlib.pyplot as plt
from connected import generate_graph
from preferencial import generate_preferencial_graph

def init_queues(Graph):
    return [queue.Queue() for i in range(0, nx.number_of_nodes(Graph))]

def init_nodes(Graph):
    return [0 for i in range(0, nx.number_of_nodes(Graph))]   

def broadcast(Graph, percentage):
    round = 0
    exploring_queue = queue.Queue()             # queue of nodes to be explored
    reached_nodes = init_nodes(Graph)           # list of reached nodes
    node_queues = init_queues(Graph)            # queue for each node

    # Round 0
    initial_node = random.choice(list(Graph.nodes))
    for node in selectNeighbors(Graph, initial_node, percentage):
        exploring_queue.put(node)
        node_queues[node].put(round)
    reached_nodes[initial_node] = 1
    round += 1

    # Next rounds
    while nodesWithMessages(node_queues) != 0:
        next_exploring_queue = queue.Queue()
        while not exploring_queue.empty():
            next_node = exploring_queue.get()
            if reached_nodes[next_node] == 0:
                reached_nodes[next_node] = 1
                cleanQueue(node_queues[next_node])
                for node in selectNeighbors(Graph, next_node, percentage):
                    if reached_nodes[node] == 0:
                        next_exploring_queue.put(node)
                        node_queues[node].put(round+1)
        round += 1
        exploring_queue = next_exploring_queue
    return (reached_nodes.count(1)/nx.number_of_nodes(Graph)) * 100

def selectNeighbors(graph, node, percentage):
    return random.sample(list(graph.neighbors(node)), round(len(list(graph.neighbors(node))) * percentage/100))

def cleanQueue(queue):
    while not queue.empty():
        queue.get()

def nodesWithMessages(queue):
    count = 0
    for node_queue in queue:
        if not node_queue.empty():
            count += 1
    return count

def generate_plot(Graph):
    percentages_reach = [(percentage, sum([broadcast(Graph, percentage) for iteration in range(args.n_iterations)])/args.n_iterations) 
        for percentage in range(0, 100 + args.step, args.step)]
    [x_axis, y_axis] = list(zip(*percentages_reach))
    draw_plot(x_axis, y_axis) 

def draw_plot(x_axis, y_axis):
	plt.xlabel('% of selected nodes')
	plt.ylabel('% of reached nodes')
	plt.plot(x_axis, y_axis, marker='.')
	plt.savefig(args.output)       

if __name__== "__main__":
    parser = argparse.ArgumentParser(prog='broadcast')
    parser.add_argument('-i', '--initial_nodes', help = 'number of initial nodes to be generated', type = int, default = 100)
    parser.add_argument('-s', '--step', help = 'step for the next percentage', type = int, default = 10)
    parser.add_argument('-n', '--n_iterations', help = 'number of iterations for each percentage', type = int, default = 10)
    parser.add_argument('-o', '--output', help = 'output file (plot)', required = True)
    parser.add_argument('-p', '--preferencial_graph', help = 'generates preferencial graph instead of a connected one', action = 'store_true')

    args = parser.parse_args()
    if args.preferencial_graph:
        Graph = generate_preferencial_graph(args.initial_nodes)
    else:
        Graph = generate_graph(args.initial_nodes)    
    generate_plot(Graph)
    