import os
from dataset import load_letters,generate_circles
import logger
from sklearn.decomposition import KernelPCA
import gc
import sys
import timeit
import kmeans
import silhouette
import hungarian
import numpy as np
import pandas as pd
import labelscan
import traceback
from datetime import datetime
from labelscan import label_to_class_dict
from paths import folder_paths,datafiles_names,KMeans_paths,Thresholding_paths,KPCA_output_path,th_hungarian_results,k1D_hungarian_results,k2D_hungarian_results
from gen_moonpairs import generate_moonpairs
import ctypes



def remove_class(clusters,gamma,assignment_file_path,method,params,stepsize,dropped_class_numbers):
	df = pd.read_csv(assignment_file_path)
	df.sort_values(by=['Assignment Cost'],inplace=True)
	class_to_remove = df['Class'].iloc[0]
	dropped_class_numbers.append(class_to_remove)
	print("Cluster:	",clusters)
	print("Removed Class:	",class_to_remove)
	
	groundtruth_values = pd.read_csv(datafiles_names[0]+datafiles_names[2],header=None)
	l = []
	for i in range(0,groundtruth_values.size):
		if(groundtruth_values[groundtruth_values.columns[0]].iloc[i]==class_to_remove):
			l.append(i)
		#print(i,df[df.columns[0]].iloc[i])
	#Filter class from groundtruth
	#print(l)
	groundtruth_values.drop(l,inplace=True)
	groundtruth_values.to_csv(datafiles_names[0]+datafiles_names[2],index=False,header=None)
	#Filter class from data
	
	#data_values = pd.read_csv(datafiles_names[0]+"letters_data.csv",header=None)
	data_values = pd.read_csv(datafiles_names[0]+"moons_data.csv",header=None)

	
	data_values.drop(l,inplace = True)
	
	#data_values.to_csv(datafiles_names[0]+"letters_data.csv",index=False,header=None)
	data_values.to_csv(datafiles_names[0]+"moons_data.csv",index=False,header=None)


	clusters = clusters - 1
	
	#data = pd.read_csv(datafiles_names[0]+"letters_data.csv",header=None)
	data = pd.read_csv(datafiles_names[0]+"moons_data.csv",header=None)


	rows_toload = len(data.index)
	print("Data Size:	",rows_toload)
	dr_cluster(data,method,gamma,params,clusters,stepsize,rows_toload,dropped_class_numbers)



def write_hungarian_result(gamma,clusters,groundtruth_distribution,temp_assignment_error_matrix,row_ind,col_ind,class_numbers,purity,method,params,stepsize,dropped_class_numbers):
	if(method=="Thresholding"):
		hungarian_results = th_hungarian_results
	if(method=="Kmeans1D"):
		hungarian_results =k1D_hungarian_results
	if(method=="Kmeans2D"):
		hungarian_results =k2D_hungarian_results
	file_suffix = "_"+str(gamma)+"_"+str(clusters)+".csv"
	df = pd.DataFrame(groundtruth_distribution)
	df.to_csv(hungarian_results[0]+file_suffix,index=False,header=None)
	'''
	df = pd.DataFrame(temp_assignment_error_matrix)
	df.to_csv(hungarian_results[1]+file_suffix,index=False,header=None)
	'''
	class_name = np.full((clusters,1),' ')
	hungarian_assignment = pd.DataFrame()
	hungarian_assignment['Cluster'] = row_ind
	hungarian_assignment['Class'] 	= class_numbers
	mapping = label_to_class_dict("/home/nachiket/Desktop/thesis/Dataset/moonpairs/Category_tolabel.csv")
	for i in range(0,len(class_numbers)):
		class_name[i] = mapping[class_numbers[i]]
	hungarian_assignment['Class Name'] = class_name
	hungarian_assignment['Assignment Cost'] = temp_assignment_error_matrix[row_ind,col_ind]
	hungarian_assignment.to_csv(hungarian_results[2]+file_suffix,index=False)

	del hungarian_assignment
	del df
	gc.collect()
	if(clusters > 2):
		remove_class(clusters,gamma,hungarian_results[2]+file_suffix,method,params,stepsize,dropped_class_numbers)



def dr_cluster(data,method,gamma,params,clusters,stepsize,rows_toload,dropped_class_numbers):
	if(method=="Kmeans2D"):
		components = 2
	if(method=="Kmeans1D" or method=="Thresholding"):
		components = 1
		flag = 0
		resetflag = 0
	logger.writelog(components,"Components")
	logger.result_open(method)
	print(method)
	max_sc = -100.0
	best_purity = 0.0
	best_gamma = 0.0
	serial_num = 0
	try:
		for i in range(0,params+1):
			transformer = KernelPCA(n_components=components,kernel='rbf',gamma=gamma)
			data_transformed = transformer.fit_transform(data)
			df = pd.DataFrame(data_transformed)
			df.to_csv(KPCA_output_path,index=False,header=None)
			del df
			gc.collect()
			if(method=="Thresholding"):
				if(flag==0):
					os.system("cc c_thresholding_new.c")
					flag = 1
				start = timeit.default_timer()
				os.system("./a.out "+str(clusters)+" "+str(rows_toload))
				end = timeit.default_timer()
				thresholding_time = (end-start)
				sc = silhouette.silhouette(KPCA_output_path,Thresholding_paths[1])
				groundtruth_distribution,temp_assignment_error_matrix,row_ind,col_ind,class_numbers,purity = hungarian.hungarian('t',Thresholding_paths[0],clusters,rows_toload,dropped_class_numbers)
				logger.writeresult(i+1,clusters,method,thresholding_time,gamma,sc,purity)
				#print(i+1,thresholding_time,gamma,sc,purity)
				if(i<params):
					if(sc > max_sc):
						max_sc = sc
						best_gamma = gamma
						best_purity = purity
						serial_num = i+1
				if(i==(params-1)):
					gamma = best_gamma
					sc = max_sc
					purity = best_purity
				if(i==params):
					print(best_gamma,max_sc,best_purity)
					logger.writeresult(" "," "," "," "," "," "," ")
					logger.writeresult(serial_num,clusters,method,thresholding_time,best_gamma,max_sc,best_purity)
					logger.writeresult(" "," "," "," "," "," "," ")
					logger.writefinalresult(serial_num,clusters,method,thresholding_time,best_gamma,max_sc,best_purity)
					write_hungarian_result(best_gamma,clusters,groundtruth_distribution,temp_assignment_error_matrix,row_ind,col_ind,class_numbers,best_purity,method,params,stepsize,dropped_class_numbers)
			else:
				kmeans_time = kmeans.kmeans(KPCA_output_path,KMeans_paths[1],clusters)
				kmeans.groundtruth_distribution(KMeans_paths[1],KMeans_paths[0],datafiles_names[0],datafiles_names[2],clusters)
				sc = silhouette.silhouette(KPCA_output_path,KMeans_paths[1])
				groundtruth_distribution,temp_assignment_error_matrix,row_ind,col_ind,class_numbers,purity = hungarian.hungarian('k',KMeans_paths[0],clusters,rows_toload,dropped_class_numbers)
				logger.writeresult(i+1,clusters,method,kmeans_time,gamma,sc,purity)
				#print(i+1,kmeans_time,gamma,sc,purity)
				if(i<params):
					if(sc > max_sc):
						max_sc = sc
						best_gamma = gamma
						best_purity = purity
						serial_num = i+1
				if(i==(params-1)):
					gamma = best_gamma
					sc = max_sc
					purity = best_purity
				if(i==params):
					print(best_gamma,max_sc,best_purity)
					logger.writeresult(" "," "," "," "," "," "," ")
					logger.writeresult(serial_num,clusters,method,kmeans_time,best_gamma,max_sc,best_purity)
					logger.writeresult(" "," "," "," "," "," "," ")
					logger.writefinalresult(serial_num,clusters,method,kmeans_time,best_gamma,max_sc,best_purity)
					write_hungarian_result(best_gamma,clusters,groundtruth_distribution,temp_assignment_error_matrix,row_ind,col_ind,class_numbers,best_purity,method,params,stepsize,dropped_class_numbers)
			if(i<(params-1)):
				gamma = gamma + stepsize
	except (KeyboardInterrupt, SystemExit, Exception) as ex:
		ex_type, ex_value, ex_traceback = sys.exc_info()
		trace_back = traceback.extract_tb(ex_traceback)
		logger.writelog(str(ex_type.__name__),"Exception Type")
		logger.writelog(str(ex_value),"Exception Message")
		logger.writelog(str(trace_back),"Traceback")
	finally:
		logger.result_close()









rows_toload = 20000
gamma_start = 1.0e-5
gamma_end = 10.0
params = 10000
clusters = 50


logger.log_open()
stepsize = round(((gamma_end - gamma_start)/params),5)
logger.writelog(gamma_start,"Gamma_start")
logger.writelog(gamma_end,"Gamma_end")
logger.writelog(params,"Parameters")
logger.writelog(stepsize,"Step_size")
logger.writelog(clusters,"clusters")


'''
------Below commented code is for loading letters-----------

data,label = load_letters(datafiles_names[0],"letters.csv",rows_toload)
logger.writelog(str(data.shape),"Dataset_dimension")
logger.writelog(str(label.shape),"Groundtruth_dimension")

df = pd.DataFrame(label)
df.to_csv(datafiles_names[0]+"label.csv",index=False,header=None)
del label
gc.collect()
df = pd.DataFrame(data)
df.to_csv(datafiles_names[0]+"letters_data.csv",index=False,header=None)
labelscan.category_tolabel(datafiles_names[0])
del data
gc.collect()
'''
#generate_moonpairs()
labelscan.category_tolabel(datafiles_names[0])

df = pd.read_csv("/home/nachiket/Desktop/thesis/Dataset/moonpairs/Original/moons_data.csv",nrows=2500,header=None)
df.to_csv("/home/nachiket/Desktop/thesis/Dataset/moonpairs/moons_data.csv",index=False,header=None)
del df 
gc.collect()
df = pd.read_csv("/home/nachiket/Desktop/thesis/Dataset/moonpairs/Original/groundtruth.csv",nrows=2500,header=None)
df.to_csv("/home/nachiket/Desktop/thesis/Dataset/moonpairs/groundtruth.csv",index=False,header=None)
df.to_csv("/home/nachiket/Desktop/thesis/Dataset/moonpairs/label.csv",index=False,header=None)
del df 
gc.collect()

method_names = ["Kmeans2D"]
for method in method_names: 
	logger.writelog(method,"Method")
	#data = pd.read_csv(datafiles_names[0]+"letters_data.csv",header=None)
	data = pd.read_csv("/home/nachiket/Desktop/thesis/Dataset/moonpairs/moons_data.csv",nrows=2500,header=None)
	print(data.shape)
	dropped_class_numbers = []
	dr_cluster(data,method,gamma_start,int(params),clusters,stepsize,rows_toload,dropped_class_numbers)
logger.log_close()
