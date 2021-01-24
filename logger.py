import timeit 
from datetime import datetime
import time
from paths import result_path

basepath = result_path
separator = ","
logfile = "log.txt"
f_log = None 
f_result = None
f_finalresult = None
f_result_maxsc = None
openfile_flag = 0

def write_to_file(file_handler,l,timestamp):
	if(timestamp==True):
		file_handler.write((datetime.now()).strftime("%H:%M:%S"))
		file_handler.write(separator)
	for i in range(0,len(l)):
		file_handler.write(str(item))
		if(i<(len(l)-1)):
			file_handler.write(separator)
	file_handler.write("\n")


def log_open():
	global f_log
	f_log = open(basepath+logfile,"a+")


def result_open(method):
	global f_result
	global f_finalresult
	global openfile_flag
	f_result = open(basepath+method+"_result.txt","a+")
	f_finalresult = open(basepath+method+"_finalresult.txt","a+")
	if(openfile_flag==0):
		f_result.write("Serial No."+separator+"Clusters"+separator+"Execution Time"+separator+"Gamma"+separator+"Silhouette Score"+separator+"Cluster Purity"+"\n\n")
		f_finalresult.write("Serial No."+separator+"Clusters"+separator+"Execution Time"+separator+"Gamma"+separator+"Silhouette Score"+separator+"Cluster Purity"+"\n\n")
		openfile_flag = 1

def result_maxsc_open():
	global f_result_maxsc
	f_result_maxsc = open(basepath+"max_silhouette.txt","a+")
	f_result_maxsc.write("Method"+separator+"Serial No."+separator+"Execution Time"+separator+"Gamma"+separator+"Silhouette Score"+separator+"Cluster Purity"+"\n\n")
	



def writelog(info,description):
	f_log.write((datetime.now()).strftime("%H:%M:%S")+separator+description+separator+str(info)+"\n")
	f_log.flush()


def writeresult_maxsc(method,serialnum,time,gamma,sc,acc):
	f_result_maxsc.write(str(method)+separator+str(serialnum)+separator+str(time)+separator+str(gamma)+separator+str(sc)+separator+str(acc)+"\n")
	f_result_maxsc.flush()	


def writeresult(serialnum,clusters,method,time,gamma,sc,acc):
	f_result.write(str(serialnum)+separator+str(clusters)+separator+str(time)+separator+str(gamma)+separator+str(sc)+separator+str(acc)+"\n")
	f_result.flush()	


def writefinalresult(serialnum,clusters,method,time,gamma,sc,acc):
	f_finalresult.write(str(serialnum)+separator+str(clusters)+separator+str(time)+separator+str(gamma)+separator+str(sc)+separator+str(acc)+"\n")
	f_finalresult.flush()


def result_close():
	f_result.close()
	f_finalresult.close()


def log_close():
	f_log.close()
	

def result_maxsc_close():
	f_result_maxsc.close()



	


