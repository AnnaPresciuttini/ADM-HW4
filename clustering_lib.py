#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import matplotlib
import math
import random
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import scale

def euclidean_distance(x, y):
    return np.linalg.norm(x - y)

def get_rand_centroids(min_lst,max_lst,n):
    centroids=np.zeros((n,len(min_lst)))
    for i in range(n):
        for j in range(len(min_lst)):
            max_=max_lst[j]
            min_=min_lst[j]
            rand=random.uniform(min_,max_)
            #print(i,j)
            centroids[i][j]=rand
    return centroids

def get_clusters(centroids, data, n):
    clusters= np.zeros(len(data))
    for i in range(len(data)):
        min_dis=10000
        for j in range(len(centroids)):
            distance = euclidean_distance(data[i], centroids[j])
            if distance < min_dis: 
                min_dis = distance
                clusters[i]= j
        min_dis=10000
    
    new_centroids = get_centroids(clusters, data, n)
    
    
    return clusters,new_centroids

def get_centroids(clusters, data, n):
    centroids=np.zeros((n,len(data[0])))
    for i in range(n):
        cluster_points = np.where(clusters == i)
        centroids[i]= data[cluster_points].mean(0)
    return centroids

def kmeans_model(data,n):
    max_lst= np.array([data[:,i].max() for i in range(len(data[0])) ])
    min_lst= np.array([data[:,i].min() for i in range(len(data[0])) ])
    centroids= get_rand_centroids(min_lst,max_lst,n)
    clusters= np.zeros(len(data))

    new_clusters, new_centroids= get_clusters(centroids, data, n)

    while not np.array_equal(new_clusters,clusters):
        clusters, centroids=new_clusters, new_centroids
        new_clusters, new_centroids= get_clusters(centroids, data, n)

    return clusters

