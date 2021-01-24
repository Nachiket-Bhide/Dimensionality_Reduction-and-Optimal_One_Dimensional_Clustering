import numpy as np
import pandas as pd
import sys
from scipy.optimize import linear_sum_assignment


def hungarian(method,basepath,k,size,dropped_class_numbers):
	c=50

	groundtruth_distribution = np.full((k,c),0,dtype=np.int)
	#assignment_error_matrix = np.full((k,c),0,dtype=np.float64)
	l=[]
	##ith row gives cluster and jth column gives count of a class in that cluster.
	
	for i in range(0,k):
		groundtruth_distribution[i] = (np.array(pd.read_csv(basepath+"Cluster_"+str(i)+"_groundtruth_distribution",header=None))).reshape(1,-1)
	#Accuracy for assigning ith cluster to jth class.
	

	remaining_classes = c - len(dropped_class_numbers)

	#Creating new groundtruth distribution by eliminating previously removed classes(columns)
	if(len(dropped_class_numbers)>=0):
		temp_groundtruth_distribution = np.full((k,remaining_classes),0,dtype=np.int64)
		counter = 0
		for j in range(0,c):
			if(not (j in dropped_class_numbers)):
				temp_groundtruth_distribution[:,counter] = groundtruth_distribution[:,j]
				counter+=1

	temp_assignment_error_matrix = np.full((k,remaining_classes),0,dtype=np.float64)




	for i in range(0,k):
		for j in range(0,remaining_classes):
			temp_assignment_error_matrix[i][j] = (sum(temp_groundtruth_distribution[i])-temp_groundtruth_distribution[i][j])/size
	row_ind, col_ind = linear_sum_assignment(temp_assignment_error_matrix)
	
	#Actual column number to class number mapping and respective assignment error cost
	class_numbers = [*range(0,c,1)]
	for i in dropped_class_numbers:
		class_numbers.remove(i)

	if(len(class_numbers)!=len(col_ind)):
		print("Mismatch in number of columns and classes . . .")
		sys.exit()




	#print("\n\nCluster(row indices) assigned to class(column indices)\n\n",row_ind,col_ind)
	#print("\n\nCost of assignment = ",assignment_error_matrix[row_ind,col_ind].sum(),"\n\n")

	'''for i in range(0,k):
		l.append(np.sum(groundtruth_distribution[:,i]))'''

	#print(l)

	
	purity = 0.0
	for i in range(0,k):
		temp_row = temp_groundtruth_distribution[i]
		purity = purity + ((temp_row[col_ind[i]])/size)
	#print("\n\nCluster Purity = "+str(purity))
	
	return groundtruth_distribution,temp_assignment_error_matrix,row_ind,col_ind,class_numbers,purity

'''
size=1000.0
k=26
method = input()
if(method=='k'):
	basepath = "/home/nachiket/Desktop/thesis/Output/KMeans/"
elif(method=='t'):
	basepath = "/home/nachiket/Desktop/thesis/Output/"
hungarian(method,basepath,k,size)
'''