# Efficient Clustering via Kernel Principcal Component Analysis and Optimal One Dimensional Clustering


## About Project

Several techniques are used for clustering of high-dimensional data. Traditionally, clustering approaches are based on performing dimensionality reduction of high-dimensional data followed by classical clustering such as k-means in lower dimensions. However, this approach based on k-means does not guarantee optimality. Moreover, the result of k-means is highly dependent on initialization of cluster centers and hence not repeatable, while not being optimal.

To overcome this drawback, an optimal clustering approach in one dimension based on dimensionality reduction is implemented.  The one-dimensional representation of high dimensional data is obtained using Kernel Principal Component Analysis. The one-dimensional representation of the data is then clustered optimally using a dynamic programming algorithm in polynomial time. Clusters in the one-dimensional data are obtained by minimizing the sum of within-class variance while maximizing the sum of between-class variance. 


## Programming Languages and Libraries

### Programming Languages:

  1. Python
  2. C
  
 
### Python Libraries

  1. Numpy
  2. Pandas
  3. scikit-learn
  4. Matplotlib
  5. traceback
  6. datetime



## Program file Description and Usage

To execute the program, run **main.py** program. It automatically calls the code present in other files as required. Following is a brief description of program files:

  1. **paths.py** - Specify dataset,program and output(result) paths in this file.
  2. **main.py** - Main python program to be executed.
  3. **c_thresholding_new.c**(C program) - Implements one dimensional optimal clustering.
  4. **kmeans.py** - Implements k-means clustering algorithm.
  5. **hungarian.py** - Implements Hungarian algorithm for class-cluster assignment. 
  6. **silhouette.py** - Calculates Silhouette Score for resulting clusters. 
  7. **gen_moonpairs.py** - Generates specified number of half-moon pairs at random positions, angles in 2 dimensional plane.
  8. **dataset.py** - Used for loading, handling datasets.
  9. **labelscan.py** - Converts non-numeric class categories to numeric labels.
  10. **logger.py** - Logs important information(such as runtime exception handling stacktrace), variables values during the program execution.   
  11. **plot_graph.py** - Plots the graph of "Numbers of Clusters"(X-axis) vs "Silhouette Score"(Y-axis) for comparing clustering performance.
  

## Datasets Used

**English Letters.csv** - Labeled real world dataset containing 20,000 samples of 26 letters of English alphabets. Each sample is a 16 dimensional                                           encoding, and there 26 different class labels corresponding to 26 letters of the English alphabet. Class labels(letter names) are in                               same file. 
**moons_data.csv** -      Labeled dataset datset containing 25 half moon pairs, that is 50 clusters corresponding to 50 individual half moons. Any number of half                           moon pairs can be generated using **gen_moonpairs.py** program.
**groundtruth.csv** -     Contains class labels for data points in **moon_data.csv**.  

