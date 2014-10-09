#!/usr/bin/env python
# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import csv

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
	csvfiles = {
		'cel': open('cel.csv', 'rb'),
		'2cel': open('2cel.csv', 'rb'),
		'rsel': open('rsel.csv', 'rb'),
		'cel-rs': open('cel-rs.csv', 'rb'),
		'2cel-rs': open('2cel-rs.csv', 'rb')
	};

	csv_arrays = { k: csv_to_array(v) for k, v in csvfiles.items() }
	avgs_arrays = { k: zip(*avgs_only(v)) for k, v in csv_arrays.items() }
	
	effort_series = { k: v[0] for k, v in avgs_arrays.items() }
	avg_series = { k: v[1] for k, v in avgs_arrays.items() }

	plots = { k: [effort_series[k], avg_series[k]] for k, v in csvfiles.items() }
	
	plt.figure(figsize=(4, 3))

	for k, v in plots.items():
		plt.plot(plots[k][0],plots[k][1])



	plt.plotfile
	plt.savefig('myplot.pdf')	
	plt.close()

if __name__ == '__main__':
	main()
