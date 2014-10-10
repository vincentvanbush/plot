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

# Converts a list of lists to a list containing just the keys and aggregate averages
# (for the format specific to the exercise's sample files)
def avgs_only(csv_array):
	result = csv_array
	del result[0]
	for i in range(0, len(result)):
		# print result[i]
		result[i].pop(0)
		effort = result[i][0]
		result[i].pop(0)
		avg = sum(result[i])/float(len(result[i]))
		result[i] = [effort, avg]
	return result

def main():
	datasets = ['cel', '2cel', 'rsel', 'cel-rs', '2cel-rs']
	dataset_names = ['1-Coev', '2-Coev', '1-Evol-RS', '1-Coev-RS', '2-Coev-RS']

	csvfiles = { filename: open('data/%s.csv' % filename) for filename in datasets }

	# Original CSV files converted to lists of lists
	csv_arrays = { k: csv_to_array(v) for k, v in csvfiles.items() }

	# Original lists aggregated to averages and transposed
	avgs_arrays = { k: zip(*avgs_only(v)) for k, v in csv_arrays.items() }
	
	effort_series = { k: v[0] for k, v in avgs_arrays.items() }
	avg_series = { k: v[1] for k, v in avgs_arrays.items() }

	# Series for each datafile
	plots = [ [effort_series[k], avg_series[k]] for k in datasets ]
	
	# Set serif font
	rcParams['font.family'] = 'serif'
	rcParams['font.sans-serif'] = ['Times']

	# Set graph aspect ratio
	plt.figure(figsize=(8, 6))

	# Plot series for each datafile
	for k in plots:
		plt.plot(k[0],k[1])

	# Legend
	legend = plt.legend(dataset_names, loc='lower right')

	

	# Axis range
	plt.axis([0, 500000, 0.6, 1.0])

	# Axis labels
	plt.xlabel('Rozegranych gier')
	plt.ylabel('Odsetek wygranych gier')

	# Save plot to file
	plt.plotfile
	plt.savefig('myplot.pdf')
	plt.close()

if __name__ == '__main__':
	main()
