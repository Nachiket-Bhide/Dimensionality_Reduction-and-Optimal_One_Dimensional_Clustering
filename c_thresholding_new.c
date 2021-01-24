#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <string.h>



char* concatenate(char *s1,char *s2)
{
	char *s = malloc(strlen(s1)+strlen(s2)+1);
	strcpy(s,s1);
	strcat(s,s2);
	return s;
}



long double* read_text(unsigned long size,char *path,unsigned short buffer_size)
{

    FILE *fp = fopen(path,"r");
    char buffer[buffer_size];
    long double *points = malloc(sizeof(long double)*size);
    long double *start = points;

    if(!fp)
    {
        printf("%s\n","File not found");
        return NULL;
    }

    unsigned long count = 0;
    while(fgets(buffer,buffer_size,fp))
    {
         count = count + 1;
        if(count>size)
    	{
        	printf("%s\n","Error in reading the file");
        	fclose(fp);
        	exit(1);
    	}
        *points = strtod(buffer,NULL);
         points = points + 1;
       

    }

    fclose(fp);
    points = start;
    
   

    return points;

}


void write_sortedpoints(long double *points,unsigned long size,unsigned short buffer_size)
{
	char buffer[buffer_size];
	long double *points_start = points;
	FILE *fp = fopen("/home/nachiket/Desktop/thesis/Output/Thresholding/Sorted_points.txt","w");
	if(!fp)
    {
        printf("%s\n","File not found");
        return;
    }
    unsigned short i;
    for(i=0;i<size;i++)
    {
    	sprintf(buffer,"%.19Lf\n",*points);
    	fputs(buffer,fp);
    	points = points + 1;
    }
    points = points_start;
    fclose(fp);


}



void write_result(unsigned long *T,unsigned long *labels,unsigned short k,unsigned long size,unsigned short buffer_size)
{
	char buffer[buffer_size];
	unsigned long *T_start = T;
	unsigned long *labels_start = labels;
	FILE *fp1 = fopen("/home/nachiket/Desktop/thesis/Output/Thresholding/Thresholds.txt","w");
	if(!fp1)
    {
        printf("%s\n","File not found");
        return;
    }
    unsigned short	T_size = k+1;
    unsigned short i;
    for(i=0;i<T_size;i++)
    {
    	sprintf(buffer,"%lu\n",*T);
    	fputs(buffer,fp1);
    	T = T + 1;
    }
    T = T_start;
    fclose(fp1);

    if(labels==NULL){return;}
  	FILE *fp2 = fopen("/home/nachiket/Desktop/thesis/Output/Thresholding/Labels.txt","w");
  	if(!fp2)
    {
        printf("%s\n","File not found");
        return;
    }
    for(i=0;i<size;i++)
    {
    	sprintf(buffer,"%lu\n",*labels);
    	fputs(buffer,fp2);
    	labels = labels + 1;
    }
    labels = labels_start;
    fclose(fp2);
}



void print_double_array(double *p,unsigned long size)
{
	unsigned long i=0;
	for(i=0;i<size;i=i+1)
	{
		printf("%f\n",*p);
		p = p + 1;	
	}
}



void print_integer_array(unsigned long *p,unsigned long size)
{
	unsigned long i=0;
	for(i=0;i<size;i=i+1)
	{
		printf("%lu\n",*p);
		p = p + 1;	
	}
}

int cmpfunc( const void* a, const void* b)
{
     long double *d_a =  (long double *) a;
     long double *d_b =  (long double *) b;

     if ( *d_a < *d_b ) return -1;
     else if ( *d_a > *d_b ) return 1;
     return 0;
}



unsigned long* assign_labels(unsigned long *T,unsigned long *sorted_indices,unsigned short k,unsigned long size)
{
	unsigned long *T_start = T;
	unsigned long *sorted_indices_start = sorted_indices;
	unsigned long *labels = malloc(sizeof(unsigned long)*size);
	unsigned long label_counter = 0;
	unsigned long tr;
	unsigned short T_size = k+1;
	for(unsigned short i =1;i<T_size;i++)
	{	
		tr = T[i] - T[i-1];
		for(unsigned long j=0;j<tr;j++)
		{	
			labels[*sorted_indices] = label_counter;
			//printf("%lu\n",labels[*sorted_indices]);
			sorted_indices = sorted_indices + 1;
			
		}
		//sorted_indices = sorted_indices_start;
		label_counter = label_counter + 1;
		
	}

	T = T_start;
	sorted_indices = sorted_indices_start;
	return labels;

}

struct result
	{
		unsigned long *T_ptr;
		unsigned long *labels_ptr;
		long double *sorted_points;
	};

struct result dpsearch(unsigned long size,long double *points,unsigned short M)
{
	//Memory Allocation and declarations
	long double *unsorted_points = malloc(sizeof(long double)*size);
	//printf("%lu bytes of memory allocated for %lu unsorted input points. . .\n",(sizeof(double)*size),size);
	unsigned long *sorted_indices = malloc(sizeof(unsigned long)*size);
	//printf("%lu bytes of memory allocated for storing indices based on sorted points. . .\n",(sizeof(unsigned long)*size));
	unsigned long L = size;
	unsigned long *T = malloc(sizeof(unsigned long)*(M+1));
	//printf("%lu bytes of memory allocated for storing %hu thresholds. . .\n",(sizeof(double)*size),(M+1));
	T[0] = 0;
	T[M] = L;
	double trellis_value[M+1][L+1];
	unsigned long trellis_backpointer[M+1][L+1];
	unsigned long i;
	unsigned long j;
	double withinss_previous;
	double withinss_current;
	double mean_previous;
	double mean_current;
	clock_t t;
	double time_taken;
	for(i=0;i<(M+1);i++)
	{
		for(j=0;j<(L+1);j++)
		{
			trellis_value[i][j] = 1.0/0.0;
			trellis_backpointer[i][j] = 1.0/0.0;
		}
	}
	unsigned long m;
	unsigned long back_ptr;
	unsigned long l;
	double J_min = 1.0/0.0;
	double J_temp = 1.0/0.0;
	unsigned long index;
	int found;
	double NAN = 0.0/0.0;

	//Making another copy of unsorted input points
	t = clock();
	for(i=0;i<size;i=i+1)
	{
		*unsorted_points = *points;
		unsorted_points = unsorted_points + 1;
		points = points + 1;
	}
	unsorted_points = unsorted_points - size;
	points = points - size;
	t = clock() - t;
	double time_taken_copyingdata = ((double)t)/CLOCKS_PER_SEC;



	//Sorting input points - Quick Sort
	t = clock();
	qsort(points,size,sizeof(long double),cmpfunc);
	t = clock() - t;
	double time_taken_sorting = ((double)t)/CLOCKS_PER_SEC;


	//Creating array of indices corresponding to sorted order of input points
	t = clock();
	i=0;
	for(i=0;i<size;i++)
	{	found = 0;
		index = 0;
		while(!found)
		{
			if(*points==*unsorted_points)
			{
				found = 1;
				*sorted_indices = index;
				sorted_indices = sorted_indices + 1;
				*unsorted_points = NAN;
				points = points + 1;
				unsorted_points = unsorted_points - index;
				continue;
			}

			index = index + 1;
			unsorted_points = unsorted_points + 1;
		}
	}

	//Freeing memory and setting pointers back to starting position of arrays
	free(unsorted_points);
	//printf("%lu bytes of memory freed. . .\n",(sizeof(long double)*size));
	points = points - size;
	sorted_indices = sorted_indices - size;
	t = clock() - t;
	double time_taken_order_indices = ((double)t)/CLOCKS_PER_SEC;

	t = clock();
	//Stage 1: m=1
	long double *start = points;
	withinss_previous = 0.0;
	mean_previous = *points;
	trellis_value[1][1] = withinss_previous;
	trellis_backpointer[1][1] = 0;

	for(l=2;l<(L-M+2);l=l+1)
	{
		points = points + 1;
		mean_current = ((mean_previous*(l-1))+(*points))/l;
		withinss_current = withinss_previous+(((*points)-mean_current)*((*points)-mean_current));
		trellis_value[1][l] = withinss_current;
		trellis_backpointer[1][l] = 0;
		mean_previous = mean_current;
		withinss_previous = withinss_current;
	}
	points = start;
	t = clock() - t;
	double time_taken_stage1 = ((double)t)/CLOCKS_PER_SEC;


	t = clock();
	//Stage 2: m=2 to m=M-1
	if(M>2)
	{
		for(m=2;m<M;m=m+1)
		{
			for(l=m;l<(L-M+m+1);l=l+1)
			{
				J_min = 1.0/0.0;
				J_temp = 1.0/0.0;
				points = points + (l-2);
				mean_previous = *(points+1);
				withinss_previous = 0.0;
				J_temp = trellis_value[m-1][l-1] + withinss_previous;
				if(J_temp<J_min)
				{
					J_min = J_temp;
					back_ptr = l-1;
				}
				//for(i=m-1;i<l;i=i+1)
				for(i=(l-2);i>=(m-1);i=i-1)
				{
					points = points - 1;
					mean_current = ((mean_previous*(l-i-1))+(*(points+1)))/(l-i);
					withinss_current = withinss_previous+(((*(points+1))-mean_current)*((*(points+1))-mean_current)); 
					//J_temp = trellis_value[m-1][i] + withinss(points,i,l);
					J_temp = trellis_value[m-1][i] + withinss_current;
					if(J_temp<J_min)
					{
						J_min = J_temp;
						back_ptr = i;
					}
					mean_previous = mean_current;
					withinss_previous = withinss_current;
				}
				trellis_value[m][l] = J_min;
				trellis_backpointer[m][l] = back_ptr;
				points = start;
			}
		}
	}
	t = clock() - t;
	double time_taken_stage2 = ((double)t)/CLOCKS_PER_SEC;


	t = clock();
	//Stage 3: m=M
	m = M;
	l = L;
	//finding optimal path
	J_min = 1.0/0.0;
	J_temp = 1.0/0.0;
	points = points + (l-2);
	mean_previous = *(points+1);
	withinss_previous = 0.0;
	J_temp = trellis_value[m-1][l-1] + withinss_previous;
	if(J_temp<J_min)
	{
		J_min = J_temp;
		back_ptr = l-1;
	}
	//for(i=m-1;i<l;i=i+1)
	for(i=(l-2);i>=(m-1);i=i-1)
	{
		points = points - 1;
		mean_current = ((mean_previous*(l-i-1))+(*(points+1)))/(l-i);
		withinss_current = withinss_previous+(((*(points+1))-mean_current)*((*(points+1))-mean_current));
		J_temp = trellis_value[m-1][i] + withinss_current;
		if(J_temp<J_min)
		{
			J_min = J_temp;
			back_ptr = i;
		}
		mean_previous = mean_current;
		withinss_previous = withinss_current;

	}
	trellis_value[M][L] = J_min;
	trellis_backpointer[M][L] = back_ptr;
	points = start;
	t = clock() - t;
	double time_taken_stage3 = ((double)t)/CLOCKS_PER_SEC;


	t = clock();
	//Backtracking
	l = L;
	m = M;
	while(m>=2)
	{
		T[m-1] = trellis_backpointer[m][l];
		l = trellis_backpointer[m][l];
		m = m - 1;
	}
	t = clock() - t;
	double time_taken_backtracking = ((double)t)/CLOCKS_PER_SEC;


	t = clock();
	unsigned long *labels = assign_labels(T,sorted_indices,M,size);
	t = clock() - t;
	double time_taken_assignlabels = ((double)t)/CLOCKS_PER_SEC;

	double time_taken_dpsearch = time_taken_stage1+time_taken_stage2+time_taken_stage3+time_taken_backtracking+time_taken_assignlabels+time_taken_copyingdata+time_taken_sorting+time_taken_order_indices;
	

	struct result r;
	r.T_ptr = T;
	r.labels_ptr = labels;
	r.sorted_points = points;

	/*
	printf("Copying data: %f seconds\n",time_taken_copyingdata);
	printf("Sorting data: %f seconds\n",time_taken_sorting);
	printf("Ordering Indices: %f seconds\n",time_taken_order_indices);
	printf("Stage 1: %f seconds\n",time_taken_stage1);
	printf("Stage 2: %f seconds\n",time_taken_stage2);
	printf("Stage 3: %f seconds\n",time_taken_stage3);
	printf("Backtracking: %f seconds\n",time_taken_backtracking);
	printf("Assign labels: %f seconds\n",time_taken_assignlabels);
	printf("Total time: %f seconds\n",time_taken_dpsearch);
	*/
	return r;
}



void write_cluster_indices(char *path,unsigned long cluster_size,unsigned long *ptr,unsigned short buffer_size)
{
	FILE *fp = fopen(path,"w");
	unsigned long *ptr_start = ptr;
	char buffer[buffer_size];
	if(!fp)
    {
        printf("%s\n","File not found");
        return;
    }
   	for(unsigned long i=0;i<cluster_size;i++)
    {
    	sprintf(buffer,"%lu\n",*ptr);
    	fputs(buffer,fp);
    	ptr = ptr + 1;
    }
    ptr = ptr_start;
    fclose(fp);

}


void write_groundtruth_distribution(char *path,unsigned short c,unsigned long *ptr,unsigned short buffer_size)
{
	FILE *fp = fopen(path,"w");
	unsigned long *ptr_start = ptr;
	char buffer[buffer_size];
	if(!fp)
    {
        printf("%s\n","File not found");
        return;
    }
    for(unsigned short i=0;i<c;i++)
    {
    	sprintf(buffer,"%lu\n",*ptr);
    	fputs(buffer,fp);
    	ptr = ptr + 1;
    }
    ptr = ptr_start;
    fclose(fp);

}



 void group(unsigned long *T,unsigned long *labels,unsigned long size,unsigned short buffer_size,char *path,unsigned short k)
 {

 	unsigned long *groundtruth = malloc(sizeof(unsigned long)*size);
 	unsigned long *groundtruth_start = groundtruth;
 	char buffer[buffer_size];
 	unsigned long *arrayOfptr[k];
 	unsigned long *arrayOfptr_start[k];
 	unsigned long *arrayOfptr_groundtruth_distribution[k];
 	unsigned long *ptr;
 	unsigned long groundtruthvalue;

	

 	FILE *fp_groundtruth = fopen(concatenate("/home/nachiket/Desktop/thesis/Dataset/moonpairs/","groundtruth.csv"),"r");
 	if(!fp_groundtruth)
    {
        printf("%s\n","File not found");
        return;
    }
	while(fgets(buffer,buffer_size,fp_groundtruth))
    {
    	*groundtruth = strtoul(buffer,NULL,10);
    	groundtruth = groundtruth + 1;
    }
    fclose(fp_groundtruth);
    groundtruth = groundtruth_start;
   
    
    for(unsigned short i=0;i<k;i++)
    {
    	arrayOfptr[i] = malloc(sizeof(unsigned long)*(T[i+1]-T[i]));
    	//arrayOfptr_groundtruth_distribution[i] = malloc(sizeof(unsigned long)*26.0);
    	arrayOfptr_start[i] = arrayOfptr[i];
    	//ptr = arrayOfptr_groundtruth_distribution[i];
    	/*for(unsigned short j=0;j<26;j++)
    	{
    		ptr[j] = 0;
    	}*/
    }
    

    for(unsigned short i=0;i<k;i++)
    {
    	arrayOfptr_groundtruth_distribution[i] = malloc(sizeof(unsigned long)*50.0);
    	ptr = arrayOfptr_groundtruth_distribution[i];
    	for(unsigned short j=0;j<50;j++)
    	{
    		ptr[j] = 0;
    	}
    }




    for(unsigned long i=0;i<size;i++)
    {
    	*arrayOfptr[labels[i]] = i;
    	arrayOfptr[labels[i]] = arrayOfptr[labels[i]] + 1;
    	ptr = arrayOfptr_groundtruth_distribution[labels[i]];
    	groundtruthvalue = groundtruth[i];
    	ptr[groundtruthvalue] = ptr[groundtruthvalue] + 1;
    	
    }
   

    for(unsigned short i=0;i<k;i++)
    {
    	arrayOfptr[i] = arrayOfptr_start[i];
    }

    for(unsigned short i=0;i<k;i++)
    {
    	unsigned short c = 50; //number of classes
    	sprintf(buffer,"Cluster_%hu_members_indices",i);
    	write_cluster_indices((concatenate(path,buffer)),(T[i+1]-T[i]),arrayOfptr[i],1024);
	   	sprintf(buffer,"Cluster_%hu_groundtruth_distribution",i);
    	write_groundtruth_distribution((concatenate(path,buffer)),c,arrayOfptr_groundtruth_distribution[i],1024);
    }

    
    
 }









void main(int argc,char *argv[])
{
		
	//unsigned short k = 26;
	unsigned short k = atoi(argv[1]);
	clock_t t;
	//unsigned long size = atoi(argv[2]);
	char *p;
	unsigned long size = strtoul(argv[2],&p,10);
	long double *points = read_text(size,"/home/nachiket/Desktop/thesis/Output/kpca.txt",1024);
	struct result r;
	t = clock();
	r = dpsearch(size,points,k);
	t = clock() - t;
	write_result(r.T_ptr,r.labels_ptr,k,size,1024);
	write_sortedpoints(r.sorted_points,size,1024);
	group(r.T_ptr,r.labels_ptr,size,1024,"/home/nachiket/Desktop/thesis/Output/Thresholding/",k);
	//double time_taken = ((double)t)/CLOCKS_PER_SEC;
	//printf("Time taken:	%f seconds\n",time_taken);
	
}