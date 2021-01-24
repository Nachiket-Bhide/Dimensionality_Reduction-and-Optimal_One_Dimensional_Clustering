import pandas as pd 
import numpy as np
from numpy import savetxt


def category_tolabel(path):
	df = pd.read_csv(path+"label.csv",header=None)
	df = df[df.columns[0]]
	labels = np.array(df)
	labels_array = np.full((labels.shape[0],1),-1)
	labels_list = []
	
	for i in labels:
		if i not in labels_list:
			labels_list.append(i)

	category_tolabel = np.full((len(labels_list),2)," ",dtype='object')
	for i in range(0,len(labels_list)):
		category_tolabel[i,0] = labels_list[i]
		category_tolabel[i,1] = int(labels_list.index(labels_list[i])) 
	df=pd.DataFrame(category_tolabel,columns=["Category Name","Label Number"])
	df.to_csv(path+"/Category_tolabel.csv",index=False)
	
	for i in range(0,labels.shape[0]):
		labels_array[i] = labels_list.index(labels[i])
	df = pd.DataFrame(labels_array,columns=["class"])
	df.to_csv(path+"/groundtruth.csv",header=None,index=False)	
	#print(df.head(5))


def label_to_class_dict(path):
	df = pd.read_csv(path)
	df = df.iloc[:, ::-1]
	df.set_index('Label Number',inplace=True)
	mapping = df.to_dict()['Category Name']
	return mapping


	





'''
path = "/home/nachiket/Desktop/thesis/Dataset"
category_tolabel(path)
'''