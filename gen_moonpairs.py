import random
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from sklearn.datasets import make_moons
import gc
import pandas as pd

def makemoons(samples,random_state):
	X,y = make_moons(n_samples=100,shuffle=True, noise=0.0, random_state=random_state)
	return X,y


def transform(data,count):
	angle = random.randint(1,360)
	add_mat = np.full((data.shape[0],data.shape[1]),random.randint(-5,5))
	data = np.add(data,add_mat)
	#print(angle)
	theta = np.radians(angle)
	cos_theta = np.cos(theta)
	sin_theta = np.sin(theta)
	data_new = np.copy(data)
	data_new[:,0] = data[:,0]*cos_theta + data[:,1]*sin_theta
	data_new[:,1] = -1*data[:,0]*sin_theta + data[:,1]*cos_theta
	del data
	gc.collect()
	return data_new



def plot(dataset,groundtruth,moon_pairs):
	#colors = {0:'red', 1:'green',2:'blue',3:'black',4:'yellow',5:'magenta',6:'purple'}
	arcs = moon_pairs*2
	colors = {}
	for i in range(0,arcs):
		rgb = (random.random(), random.random(), random.random())
		colors[i] = rgb
	x = dataset[:,0]
	y = dataset[:,1]
	groundtruth = groundtruth[:,0]
	for i in range(1,len(groundtruth)):
		plt.scatter(x[i],y[i],color = colors[groundtruth[i]])
	#plt.show()
	#plt.savefig("moonpairs_dataset")


def generate_moonpairs():
	moon_pairs = 25
	dataset = np.full((1,2),0)
	groundtruth = np.full((1,1),0)
	#groundtruth = groundtruth.reshape(-1,1)
	counter = 0
	for i in range(0,moon_pairs):
		random_state = random.randint(1,1000)
		samples = random.randint(100,200)
		#noise = random.uniform(0.01,0.1)
		X,label = makemoons(samples,random_state)
		X_new = transform(X,i)
		if(i>0):
			for j in range(0,len(label)):
				label[j] = label[j]+counter
		label = label.reshape(-1,1)
		dataset = np.concatenate([dataset,X_new],axis=0)
		groundtruth = np.concatenate([groundtruth,label],axis=0)
		counter = counter + 2


	dataset = np.delete(dataset,0,0)
	groundtruth = np.delete(groundtruth,0,0)
	df = pd.DataFrame(dataset)
	df.to_csv("/home/nachiket/Desktop/thesis/Dataset/moonpairs/moons_data.csv",index=False,header=None)
	df.to_csv("/home/nachiket/Desktop/thesis/Dataset/moonpairs/Original/moons_data.csv",index=False,header=None)

	df = pd.DataFrame(groundtruth)
	df.to_csv("/home/nachiket/Desktop/thesis/Dataset/moonpairs/groundtruth.csv",index=False,header=None)
	df.to_csv("/home/nachiket/Desktop/thesis/Dataset/moonpairs/Original/groundtruth.csv",index=False,header=None)


dataset = np.array(pd.read_csv("/home/nachiket/Desktop/thesis/Dataset/moonpairs/Original/moons_data.csv",nrows=2500))
groundtruth = np.array(pd.read_csv("/home/nachiket/Desktop/thesis/Dataset/moonpairs/Original/groundtruth.csv",nrows=2500))
plot(dataset,groundtruth,25)




'''

r=1000
colors = {0:'red', 1:'green'}
X,label = makemoons(r)
X_new = transform(X)
x = X_new[:,0]
y = X_new[:,1]

for i in range(0,len(y)):
	plt.scatter(x[i],y[i],color = colors[label[i]])
plt.show()

'''







'''
def y_val(a,b,c,x):
	return a*(x**2) + b*x + c

 
pts = 50


objects = 5
data_y = []
data_x = []
label = []

for i in range(0,objects):
	X = np.linspace(random.randrange(-5,0), random.randrange(0,5), pts)
	a = -1
	b = 20
	c = 10
	y = [y_val(a,b,c,x) + (random.gauss(x,1)) for x in X]	
	data_y.append(y)
	data_x.append(X)
	label.append(np.ones((pts,), dtype=int))



plt.scatter(data_x, data_y, c='r')
plt.show()
'''