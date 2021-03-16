# Efficient Clustering via Kernel Principcal Component Analysis and Optimal One Dimensional Clustering


## About Research Work

### Motivation:

  1. Traditional approaches for clustering high dimensional data involve dimensionality reduction followed by classical clustering algorithms such as k-means in             lower dimensions.
  2. However, approaches based on k-means clustering suffer from the drawbacks and limitations of k-means clustering, namely, high dependency on initialization of cluster centroids, non-repeatability of clustering results. Also, k-means can converge locally and hence does not guarantee optimal clustering.


### Proposed Approach:

1. An optimal clustering approach in one dimension based on dimensionality reduction is proposed.
2. One dimensional representation of high dimensional data is obtained using Kernel Principal Component Analysis using a suitable kernel function such as Radial Basis Function(RBF).
3. One dimensional representation is then clustered optimally using dynamic programming algorithm in polynomial time


### Contribution:

1. Developed a program using Python and C programming languages for implementing proposed clustering approach.
2. Using Silhouette score as a metric to evaluate quality of clustering, the advantages of proposed approach over traditional k-means based approaches are demonstrated.
3. For testing the proposed approach, a real world high dimensional dataset and a synthetic two dimensional dataset is used.


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

1. **English Letters.csv** - Labeled real world dataset containing 20,000 samples of 26 letters of English alphabets. Each sample is a 16 dimensional                                          encoding, and there 26 different class labels corresponding to 26 letters of the English alphabet. Class labels(letter names) are in                              same file. 
2. **moons_data.csv** -      Labeled dataset datset containing 25 half moon pairs, that is 50 clusters corresponding to 50 individual half moons. Any number of                                half moon pairs can be generated using **gen_moonpairs.py** program.
3. **groundtruth.csv** -     Contains class labels for data points in **moon_data.csv**.  


## Contact Information

1. Nachiket Bhide - bhiden@uwindsor.ca
2. Dr. Luis Rueda - lrueda@uwindsor.ca
