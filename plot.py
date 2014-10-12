#!/usr/bin/env python
# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
from matplotlib import rcParams
from matplotlib.ticker import FuncFormatter
import csv
import numpy as np

# Converts a csvfile to list of lists
def csv_to_array(csvfile):
	result = []
	for row in csv.reader(csvfile):
		result.append(row)
		for i in range(0, len(row)):
			try:
				row[i] = float(row[i])
			except ValueError:
				pass
	return result


# Converts a list of lists to a list containing just the generations, efforts
# and aggregate averages (for the format specific to the exercise's sample files)
def aggregate_avgs(csv_array):
	result = list(csv_array)
	del result[0]
	for i in range(0, len(result)):
		generation = result[i][0]
		effort = result[i][1]
		avg = sum(result[i][2:])/float(len(result[i][2:]))
		result[i] = [generation, effort, avg]
	return result

# Draws left graph
def left_graph(plot_data):
	left = plt.subplot(121)
	dataset_names = []
	for plot in plot_data:
		dataset_names.append(plot['name'])
		this_plot = plt.plot(
			plot['x'], plot['y'],
			color=plot['color'],
			marker=plot['marker'],
			markersize=5)
		plt.setp(this_plot, markevery=25)

	# Axes
	plt.axis([0, 500000, 0.6, 1.0])
	plt.xlabel('Rozegranych gier')
	plt.ylabel('Odsetek wygranych gier')
	left.tick_params(labelsize="small")
	plt.xticks(rotation=20)

	# Legend
	legend = plt.legend(dataset_names, loc='lower right', scatterpoints=12)

	# Generation axis
	gen_axis = plt.twiny()
	plt.xlabel('Pokolenie')
	gen_axis.set_xticks([0,40,80,120,160,200])
	gen_axis.tick_params(labelsize="small")

	pass

def right_graph(plot_data):
	right = plt.subplot(122)

	data = []
	for plot in plot_data:
		data.append(plot['last_row'])

	plt.boxplot(data, True, 'b+')
	plt.axis((0.5,5.5,0.6,1.0), size="small")
	right.grid(linewidth=0.1)
	right.yaxis.tick_right()
	
	
	right.tick_params(labelsize="small")
	plt.xticks(range(1,6),[plot['name'] for plot in plot_data],rotation=20,size="x-small")



	pass

def main():
	datasets = ['cel', '2cel', 'rsel', 'cel-rs', '2cel-rs']
	dataset_names = {'cel': '1-Coev', '2cel': '2-Coev', 'rsel': '1-Evol-RS', 'cel-rs': '1-Coev-RS', '2cel-rs': '2-Coev-RS'}
	dataset_colors = { 'cel': 'b', '2cel': 'y', 'rsel': 'g', 'cel-rs': 'r', '2cel-rs': 'c'}
	dataset_markers = { 'cel': 'o', '2cel': 'v', 'rsel': '^', 'cel-rs': 's', '2cel-rs': '*'}

	csvfiles = { filename: open('data/%s.csv' % filename) for filename in datasets }

	# Original CSV files converted to lists of lists
	csv_arrays = { k: csv_to_array(v) for k, v in csvfiles.items() }
	
	# Original lists aggregated to averages and transposed
	avgs_arrays = { k: zip(*aggregate_avgs(v)) for k, v in csv_arrays.items() }

	effort_series = { k: v[1] for k, v in avgs_arrays.items() }
	avg_series = { k: v[2] for k, v in avgs_arrays.items() }
	last_rows = { k: v[-1][2:]  for k, v in csv_arrays.items() }


	# Series for each datafile
	plots = [ {
				'x': effort_series[k],
				'y': avg_series[k],
				'color': dataset_colors[k],
				'marker': dataset_markers[k],
				'name': dataset_names[k],
				'last_row': last_rows[k]
			 } for k in datasets ]
	
	# Set serif font
	rcParams['font.family'] = 'serif'
	rcParams['font.sans-serif'] = ['Times']

	left_graph(plots)
	right_graph(plots)

	# for k in plots:
	# 	ax1.plot(k['x'], k['y'], color=k['color'])

	# Save plot to file
	plt.show()
	# plt.plotfile
	# plt.savefig('myplot.pdf')
	# plt.close()

if __name__ == '__main__':
	main()
