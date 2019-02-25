# -----
# Script to get rid of all duplicate data points in the tracks_mood_amazon.csv
# -----

import os
from collections import Counter
from collections import defaultdict

def check_if_duplicate():

	pass

if __name__ == "__main__":


	f_in = open("tracks_mood_amazon.csv")
	f_out = open("tracks_mood_amazon_nodupli.csv", 'w')


	data = f_in.readlines()
	nohead_data = list(data)
	nohead_data.pop(0)


	list_to_check = [' '.join(line.rstrip().split(",")[1:3]) for line in data]
	# print(len([k for k,v in Counter(list_to_check).items() if v>1]))
	
	D = defaultdict(list)
	for i, item in enumerate(list_to_check):
		D[item].append(i+1)
	D = {k:v for k,v in D.items() if len(v)>1}

	print(D)

	indices_to_pop = []

	for key, value in D.iteritems():
		for index, row in enumerate(value):
			if index>0:
				indices_to_pop.append(row)


	print(sorted(indices_to_pop))
	# print(len(data))
	for line in reversed(sorted(indices_to_pop)):
		print(str(line-1) + " " + data[line-1])
		data.pop(line-1)
	# print(len(data))
	print(len([k for k,v in Counter(data).items() if v>1]))
	print(len(data))

	f_out.writelines(data)



	f_in.close()
	f_out.close()