import pandas as pd
import numpy as np
import os
import gc
import matplotlib.pyplot as plt
from sklearn.datasets import make_s_curve, make_circles, make_moons
from sklearn.datasets.samples_generator import make_swiss_roll



def load_digits(basepath,csv_filename,rows_toload):
	df = pd.read_csv(basepath+"/Dataset/"+csv_filename,nrows=rows_toload)
	groundtruth = np.array(df[df.columns[0]])
	df = df.drop(df.columns[0],axis=1)
	data = np.array(df)
	del df
	gc.collect()
	return data,groundtruth



def generate_circles(path,samples,factor,noise,random_state):
	X,y = make_circles(n_samples = samples,factor = factor,noise = noise, random_state = random_state)
	df_data = pd.DataFrame(data=X)
	df_labels = pd.DataFrame(data=y)
	df_data.to_csv(path+"circles.csv",header=None,index=False)
	df_labels.to_csv(path+"groundtruth.csv",header=None,index=False)
	del df_data
	del df_labels
	gc.collect()
	return X,y



def swissroll(path):
	X, color = make_swiss_roll(n_samples=2000, random_state=123)
	df_data = pd.DataFrame(X)
	df_labels = pd.DataFrame(color)
	df_data.to_csv(path+"swissroll.csv",header=None,index=False)
	df_labels.to_csv(path+"groundtruth.csv",header=None,index=False)
	del df_data
	del df_labels
	gc.collect()
	return X,color



def moons(path):
	X,y = make_moons(n_samples=1000,noise=0.1)
	df_data = pd.DataFrame(X)
	df_labels = pd.DataFrame(y)
	df_data.to_csv(path+"moons.csv",header=None,index=False)
	df_labels.to_csv(path+"groundtruth.csv",header=None,index=False)
	del df_data
	del df_labels
	gc.collect()
	return X,y



def generate_3ds(samples,noise):
	data,groundtruth = make_s_curve(samples,noise)
	


def load_letters(path,filename,rows_toload):
	df = pd.read_csv(path+filename,nrows=rows_toload,header=None)
	label = np.array(df[df.columns[0]])
	df = df.drop(df.columns[0],axis=1)
	data = np.array(df)	
	del df
	gc.collect()
	return data,label







#path = "/home/nachiket/Desktop/thesis/Dataset/circles/"
#generate_circles(path,1000,0.3,0.1,2)
#basepath = os.getcwd()
#csv_filename = "letters.csv"
#rows_toload = 5

#data,groundtruth = load_digits(basepath,csv_filename,rows_toload)
#generate_3ds(100,0.1)
#data,label = load_letters(basepath,csv_filename,rows_toload)
#print(data.shape,label.shape)
#print(label)