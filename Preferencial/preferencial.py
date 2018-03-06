#!/usr/local/bin/python3

import random
import argparse
import networkx as nx
import matplotlib.pyplot as plt

from sys import argv

def generate_preferencial_graph(n_vertex):
    # init graph
    Graph = nx.Graph()
    Graph.add_nodes_from(range(n_vertex), weight = 1)

    # adding preferencial edges
    while not nx.is_connected(Graph):
        probability_list = sum([[node] * Graph.node[node]['weight'] for node in Graph.nodes],[]) 
        [x,y] = random.sample(probability_list, 2)
        Graph.add_edge(x,y)
        Graph.node[x]['weight'] += 1 
        Graph.node[y]['weight'] += 1

    return Graph 

def draw_graph(Graph):
    labels = nx.get_node_attributes(Graph, 'weight')
    nx.draw(Graph, labels = labels)
    plt.savefig('this.png')
    plt.show() 

if __name__== "__main__":
    parser = argparse.ArgumentParser(prog='preferencial')
    parser.add_argument('-v','--vertex',help = 'number of initial vertex', type=int, default=10)
    parser.add_argument('-o', '--output', help='output file', required=True)
    parser.add_argument('-p','--plot',help='generates a plot', action="store_true")

    args = parser.parse_args()

    if not args.plot:
        Graph = generate_preferencial_graph(args.vertex)
        draw_graph(Graph)