import pandas as pd 
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt 
import numpy as np











def plot_graph(path):
	df = pd.read_csv(path+"Kmeans2D_finalresult.txt")
	df = df.iloc[1:]
	K1Dclusters = np.array(df['Clusters'])
	K1Dsc = np.array(df['Silhouette Score'])
	
	'''df = pd.read_csv(path+"Kmeans2D_finalresult.txt")
	df = df.iloc[1:]
	K2Dclusters = np.array(df['Clusters'])
	K2Dsc = np.array(df['Silhouette Score'])
'''
	df = pd.read_csv(path+"Thresholding_finalresult.txt")
	df = df.iloc[1:]
	thclusters = np.array(df['Clusters'])
	thsc = np.array(df['Silhouette Score'])	

	fig = plt.figure()
	plt.plot(K1Dclusters,K1Dsc,c='blue')
	#plt.plot(K2Dclusters,K2Dsc,c='blue')
	plt.plot(thclusters,thsc,c='red')
	fig.suptitle("Runtime: K-Means 2D clustering and Optimal Thresholding")
	plt.xlabel("Number of Clusters")
	plt.ylabel("Silhouette Score")
	red_curve = mpatches.Patch(color='red', label='Optimal Thresholding')
	blue_curve = mpatches.Patch(color='blue', label='K-Means 2D clustering')
	leg = plt.legend(handles=[red_curve,blue_curve],loc='upper right')
	'''for patch in leg.get_patches():
		patch.set_height(5)
		#patch.set_y(-6)
'''
	fig.savefig("K-Means 2D vs Optimal Thresholding.png")
	#plt.show()



path = "/home/nachiket/Desktop/Moons/"
#filename = "Thresholding_finalresult.txt"
plot_graph(path)
