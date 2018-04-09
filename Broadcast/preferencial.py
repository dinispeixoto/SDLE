#!/usr/local/bin/python3

import random
import argparse
import networkx as nx
import matplotlib.pyplot as plt

from collections import Counter
from sys import argv

def draw_graph(Graph):
    labels = nx.get_node_attributes(Graph, 'weight')
    nx.draw(Graph, labels = labels)
    plt.savefig(args.output)

def draw_plot(x_axis, y_axis):
    plt.xlabel('Degree')
    plt.ylabel('Nodes')
    plt.plot(x_axis, y_axis, marker='.')
    plt.savefig(args.output)

def generate_preferencial_graph(n_vertex):
    Graph = nx.Graph()
    Graph.add_nodes_from(range(n_vertex), weight = 1)

    while not nx.is_connected(Graph):
        probability_list = sum([[node] * Graph.node[node]['weight'] for node in Graph.nodes],[]) 
        source_node = random.choice(list(Graph.nodes()))
        dest_node = random.choice(probability_list)
        Graph.add_edge(source_node, dest_node)
        try:
            nx.find_cycle(Graph)
            Graph.remove_edge(source_node, dest_node)
        except:
            Graph.node[source_node]['weight'] += 1 
            Graph.node[dest_node]['weight'] += 1
        
    return Graph 

def generate_plot():
    degree_nodes = Counter([degree for (node, degree) in generate_preferencial_graph(args.nodes).degree()])
    x_axis, y_axis = zip(*degree_nodes.items())    
    draw_plot(x_axis, y_axis)    

if __name__== "__main__":
    parser = argparse.ArgumentParser(prog='preferencial')
    parser.add_argument('-o', '--output', help='output file', required=True)
    parser.add_argument('-p','--plot',help='generates a plot', action="store_true")
    parser.add_argument('-n','--nodes', help = 'number of initial nodes', type = int, default = 10)

    args = parser.parse_args()

    if args.plot:
        generate_plot()
    else:
        Graph = generate_preferencial_graph(args.nodes)
        draw_graph(Graph)