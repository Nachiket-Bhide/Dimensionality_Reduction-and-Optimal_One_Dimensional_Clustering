import pandas as pd
import gc
from sklearn.cluster import KMeans
import numpy as np
import timeit



def kmeans(data_path,label_path,clusters):
	data = np.array(pd.read_csv(data_path,header=None))
	#print(data.shape)
	start = timeit.default_timer()
	kmeans = KMeans(n_clusters=clusters,algorithm="full",n_init=1,init='random').fit(data)
	end = timeit.default_timer()
	kmeans_time =  (end-start)
	#print("KMeans Time:	"+str(end-start))
	#print(kmeans.labels_.shape)
	df = pd.DataFrame(kmeans.labels_) 
	df.to_csv(label_path,header=None,index=False)
	del df
	gc.collect()
	return kmeans_time


def label_frequency(label_path,clusters):
	labels = np.array(pd.read_csv(label_path,header=None,dtype=int))
	label_freq = np.zeros(clusters,dtype=int)
	for i in range(0,labels.shape[0]):
		label_freq[labels[i]] += 1
	return label_freq



def group_cluster_memeber_indices(label_path,basepath,clusters):
	labels = np.array(pd.read_csv(label_path,header=None,dtype=int))
	label_freq = label_frequency(label_path,clusters)
	member_indices = []
	counter = np.zeros(clusters,dtype=int)
	for i in range(0,clusters):
		member_indices.append(np.zeros(label_freq[i],dtype=int))
	for i in range(0,labels.shape[0]):
		l = int(labels[i])
		c = int(counter[l])
		member_indices[l][c] = i
		counter[l] += 1
	for i in range(0,clusters):
		df = pd.DataFrame(member_indices[i])
		df.to_csv(basepath+"Cluster_"+str(i)+"_member_indices",header=None,index=False)
	return member_indices


def groundtruth_distribution(label_path,basepath,groundtruth_path,groundtruth_filename,clusters):
	c=50
	groundtruth = np.array(pd.read_csv(groundtruth_path+groundtruth_filename,header=None,dtype=int))
	#print(groundtruth.shape)
	member_indices = group_cluster_memeber_indices(label_path,basepath,clusters)

	for i in range(0,clusters):
		groundtruth_dist = np.zeros(c,dtype=int)
		for j in range(0,member_indices[i].shape[0]):
			groundtruth_dist[groundtruth[member_indices[i][j]]] += 1
		df = pd.DataFrame(groundtruth_dist)
		df.to_csv(basepath+"Cluster_"+str(i)+"_groundtruth_distribution",header=None,index=False)



'''
clusters = 26
basepath = "/home/nachiket/Desktop/thesis/Output/KMeans/"
groundtruth_path = "/home/nachiket/Desktop/thesis/Dataset/groundtruth.csv"
data_path = "/home/nachiket/Desktop/thesis/Output/kpca.txt"
#data_path = "/home/nachiket/Desktop/thesis/Dataset/letters_data.csv"

label_path = basepath+"KMeans_Labels.txt"
kmeans(data_path,label_path,clusters)
groundtruth_distribution(label_path,basepath,groundtruth_path,clusters)
#group_cluster_memeber_indices(label_path,basepath,10)
'''