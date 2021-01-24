dataset_folder_path = "/home/nachiket/Desktop/thesis/Dataset/"
program_folder_path = "/home/nachiket/Desktop/thesis/"
Output_folder_path = "/home/nachiket/Desktop/thesis/Output/"
#------------------------------------------------------------------------
'''
data_folder_path = dataset_folder_path + "letters/"
data_file_name = "letters_data.csv"
groundtruth_file_name = "groundtruth.csv"
'''

data_folder_path = dataset_folder_path + "moonpairs/"
data_file_name = "moons_data.csv"
groundtruth_file_name = "groundtruth.csv"

#-------------------------------------------------------------------------
KPCA_output_path = Output_folder_path + "kpca.txt"
#-------------------------------------------------------------------------
KMeans_output_folder_path = Output_folder_path + "KMeans/"
KMeans_Labelfile = KMeans_output_folder_path + "KMeans_Labels.txt"
#-------------------------------------------------------------------------
Thresholding_output_folder_path = Output_folder_path + "Thresholding/"
Thresholding_Labelfile = Thresholding_output_folder_path + "Labels.txt"
#-----------------------------------------------------------------------
#result_path = "/home/nachiket/Desktop/Letters/"
result_path = "/home/nachiket/Desktop/Moons/"

th_groundtruth_distribution_path = result_path + "Thresholding/groundtruth_distribution"
k1D_groundtruth_distribution_path = result_path + "Kmeans1D/groundtruth_distribution"
k2D_groundtruth_distribution_path = result_path + "Kmeans2D/groundtruth_distribution"

#assignment_error_matrix_path = "/home/nachiket/Desktop/Letters/assignment_error_matrix"
assignment_error_matrix_path = "/home/nachiket/Desktop/Moons/assignment_error_matrix"

th_assignment_path = result_path + "Thresholding/assignment"
k1D_assignment_path = result_path + "Kmeans1D/assignment"
k2D_assignment_path = result_path + "Kmeans2D/assignment"


folder_paths = [dataset_folder_path,program_folder_path,Output_folder_path]
datafiles_names = [data_folder_path,data_file_name,groundtruth_file_name]
KMeans_paths = [KMeans_output_folder_path,KMeans_Labelfile]
Thresholding_paths = [Thresholding_output_folder_path,Thresholding_Labelfile]
th_hungarian_results = [th_groundtruth_distribution_path,assignment_error_matrix_path,th_assignment_path]
k1D_hungarian_results = [k1D_groundtruth_distribution_path,assignment_error_matrix_path,k1D_assignment_path]
k2D_hungarian_results = [k2D_groundtruth_distribution_path,assignment_error_matrix_path,k2D_assignment_path]