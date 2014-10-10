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

def main():
	datasets = ['cel', '2cel', 'rsel', 'cel-rs', '2cel-rs']
	dataset_names = ['1-Coev', '2-Coev', '1-Evol-RS', '1-Coev-RS', '2-Coev-RS']
	dataset_colors = { 'cel': 'b', '2cel': 'y', 'rsel': 'g', 'cel-rs': 'r', '2cel-rs': 'c'}
	dataset_markers = { 'cel': 'o', '2cel': 'v', 'rsel': '^', 'cel-rs': 's', '2cel-rs': '*'}

	csvfiles = { filename: open('data/%s.csv' % filename) for filename in datasets }

	# Original CSV files converted to lists of lists
	csv_arrays = { k: csv_to_array(v) for k, v in csvfiles.items() }
	
	# Original lists aggregated to averages and transposed
	avgs_arrays = { k: zip(*aggregate_avgs(v)) for k, v in csv_arrays.items() }
	effort_series = { k: v[1] for k, v in avgs_arrays.items() }
	avg_series = { k: v[2] for k, v in avgs_arrays.items() }

	# Series for each datafile
	plots = [ { 'x': effort_series[k], 'y': avg_series[k], 'color': dataset_colors[k],'marker': dataset_markers[k] } for k in datasets ]
	
	# Set serif font
	rcParams['font.family'] = 'serif'
	rcParams['font.sans-serif'] = ['Times']

	# Set graph aspect ratio
	plt.figure(figsize=(8, 6))

	# Plot series for each datafile
	for k in plots:
		plt.plot(k['x'], k['y'], color=k['color'])

	# Axis range
	plt.axis([0, 500000, 0.6, 1.0])

	# Draw dots on top of plots
	for k in plots:
		plt.scatter(k['x'][::16], k['y'][::16], s=50, c=[k['color']]*500, alpha=0.5, marker=k['marker'] )

	# Legend
	legend = plt.legend(dataset_names, loc='lower right', scatterpoints=12)

	# Axis labels
	plt.xlabel('Rozegranych gier')
	plt.ylabel('Odsetek wygranych gier')

	# Additional axis (for displaying generations)
	generations_axis = plt.twiny()
	generations_axis.set_xlabel('Pokolenie')
	generations_axis.set_xticks([20 * x for x in range(11)])
	print generations_axis.get_xticks()

	# Save plot to file
	plt.show()
	# plt.plotfile
	# plt.savefig('myplot.pdf')
	# plt.close()

if __name__ == '__main__':
	main()
