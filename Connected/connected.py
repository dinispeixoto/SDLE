#!/usr/local/bin/python3

import random
import argparse
import networkx as nx
import matplotlib.pyplot as plt

from sys import argv

def draw_graph(graph):
	nx.draw(graph)
	plt.savefig(args.output)

def draw_plot(x_axis, y_axis):
	plt.xlabel('Number of nodes')
	plt.ylabel('Average edges')
	plt.plot(x_axis, y_axis, marker='.')
	plt.savefig(args.output)	

def generate_graph(n_vertex):
	Graph = nx.Graph()
	Graph.add_nodes_from(range(n_vertex))

	while not nx.is_connected(Graph):
		[x,y] = random.sample(Graph.nodes, 2)
		Graph.add_edge(x,y)

	return Graph

def generate_plot():
	vertex_edges = [(n_vertex, sum([generate_graph(n_vertex).number_of_edges() for x in range(args.n_iterations)])/args.n_iterations)
		for n_vertex in range(args.initial_nodes, args.final_nodes, args.step)]			

	[x_axis, y_axis] = list(zip(*vertex_edges))
	draw_plot(x_axis, y_axis)

if __name__== "__main__":
	parser = argparse.ArgumentParser(prog='connected')
	parser.add_argument('-i','--initial_nodes', help = 'number of initial nodes', type = int, default = 10)
	parser.add_argument('-s','--step', help = 'step for next number of nodes', type = int, default = 10)
	parser.add_argument('-f','--final_nodes', help = 'number of final nodes', type = int, default = 110)
	parser.add_argument('-n','--n_iterations', help ='number of iterations for each node', type = int, default = 10)
	parser.add_argument('-o', '--output', help = 'output file', required = True)
	parser.add_argument('-p','--plot', help ='generates a plot with the average number of random edges necessary to completly connect a graph', action="store_true")

	args = parser.parse_args()

	if args.plot:
		generate_plot()
	else:
		graph = generate_graph(args.initial_nodes)
		draw_graph(graph)
