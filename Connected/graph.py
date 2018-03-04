import random
import argparse
from sys import argv
import networkx as nx
import matplotlib.pyplot as plt

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

	while(not(nx.is_connected(Graph))):
		[x,y] = random.sample(Graph.nodes,2)
		Graph.add_edge(x,y)
	return Graph

def generate_plot():
	vertex_edges = [(n_vertex, generate_graph(n_vertex).number_of_edges()) 
		for n_vertex in [x * args.vertex for x in range(1,args.iterations+1)]]

	[x_axis, y_axis] = list(zip(*vertex_edges))
	draw_plot(x_axis, y_axis)


if __name__== "__main__":
	parser = argparse.ArgumentParser(prog='graph')
	parser.add_argument('-v','--vertex',help = 'number of initial vertex', type=int, default=10)
	parser.add_argument('-i','--iterations', help='number of iterations', type=int, default=10)
	parser.add_argument('-o', '--output', help='output file', required=True)
	parser.add_argument('-p','--plot',help='generates a plot with the average number of random edges necessary to completly connect a graph', action="store_true")

	args = parser.parse_args()

	if args.plot:
		generate_plot()
	else:
		graph = generate_graph(args.vertex)
		draw_graph(graph)
	