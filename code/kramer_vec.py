from __future__ import print_function
import numpy as np
import csv
import time
#import matplotlib.pyplot as plt
from math import exp, log, floor, fabs, pi, sqrt, pow
# from plot_bird import plot_ts
# from plot_bird.py import PlotBirdGraph

def LagCorrelation(v1, v2, lag):
	# cc = np.correlate(v1,np.hstack([np.zeros(lag), v2[lag:]]));
	n = v1.size
	v1 -= v1[:(n-lag)].mean()
	v2 -= v2[lag:].mean()
	v1 /= v1[:(n-lag)].std()
	v2 /= v2[lag:].std()
	return np.correlate(v1[:(n-lag)], v2[lag:])/(n-lag)

def LagCorrelationRange(v1, v2, start, stop):
	results = np.zeros(stop-start+1);
	for lag in range(start, stop):
		results[lag] = LagCorrelation(v1, v2, lag);
	# print results

def FisherTransform(C):
	one_vec = np.ones(C.shape);
	return 0.5 * np.log( (one_vec + C)/(one_vec-C) )
	
def ProbZ(Zij, tn):
	an = sqrt(2*log(tn))
	bn = an - (log(log(tn)) + np.log(4*pi))/(2*an)
	return exp( -2 * exp(-an*(Zij-bn)) )

# Returns the first k sorted values that fail null hypothesis
def FDRController(p_vals, q):
	m = len(p_vals)
	k = 0;
	for i in range(m):
		# print('{:f}    {:f}'.format(p_vals[i][1], q*(1+i)/m))
		if (p_vals[i][1] > q*(i+1)/m):
			break;
		k = i;
	return k;

def InterpolateEdges(vec):
	return 0;


def Get4Neighbors(map_m, map_n, i):
	neigh = [];
	for j in [i-map_n, i+1, i+map_n, i-1]:
		if(j < 0 or j >= map_n*map_m): continue
		# left edge
		if i%map_n == 0:
			if j == i-1: continue
		# right edge 
		if i%map_n == map_n-1:
			if j == i+1: continue
		neigh.append(j);
	return neigh

def Get8Neighbors(map_m, map_n, i):
	neigh = [];
	for j in [i-map_n-1, i-map_n, i-map_n+1, i-1, i+1, i+map_n-1, i+map_n, i+map_n+1 ]:
		if(j < 0 or j >= map_n*map_m): continue
		# left edge
		if i%map_n == 0:
			if j == i-1 or j == i-map_n-1 or j == i+map_n-1: continue
		# right edge
		if i%map_n == map_n-1:
			if j == i+1 or j == i-map_n+1 or j == i+map_n+1: continue
		neigh.append(j);
	return neigh

def FindZeroTimeSeries(data):
	[n,t] = data.shape
	bad_inds = [];
	for row in range(0, n):
		if np.sum(data[row, :]) < 1.:
			bad_inds.append(row);
	return bad_inds

def GetStdWithoutDiag(mat):
	[m,n] = mat.shape
	temp = np.zeros(m*n-m)
	offset = 0;
	for i in range(0,m):
		for j in range(0,n):
			if(i == j):
				offset+=1
				continue
			temp[i*n +j-offset] = mat[i,j] 
	return np.std(temp)

def GetDerivative(v1):
	m = len(v1);
	acc = 0;
	for i in range(0,m-1):
		acc += np.abs(v1[i]-v1[i+1]);
	return  acc/m;

def GetValidEdges(ts_data, zero_inds, time_start, time_stop, graphwriter):
	t_range = 3;
	[n,tn] = np.shape(ts_data)
	corr_list = []
	action_threshold = 0.05
	derivative_threshold = 0.008

	num_res_per_lag = 1;
	dim = 50
	assert(int(np.sqrt(n)) == dim)
	map_m = dim
	map_n = dim
	max_derivative = 0;
	
	Corrs = np.zeros((map_m*map_n,map_m*map_n,t_range));
	# This will change for the regions we are using 
	for t in range(1, t_range):
		for i in range(0, map_m*map_n):
			if i in zero_inds: continue;
			neigh = Get8Neighbors(map_m, map_n, i)
			ti = ts_data[i, time_start:time_stop]
			for j in neigh:
				if j in zero_inds: continue
				tj = ts_data[j, time_start:time_stop]
				if np.max(ti) < action_threshold or np.max(tj) < action_threshold: continue	
				
				if GetDerivative(ti) < derivative_threshold or GetDerivative(tj) < derivative_threshold: 	
						continue;
				else:
					max_derivative = max(max_derivative, GetDerivative(ti));
					max_derivative = max(max_derivative, GetDerivative(tj));
				if(Corrs[i, j, t] == 0):
					Corrs[i, j, t] = FisherTransform(LagCorrelation(ti.copy(), tj.copy(), t));
					# print("corrs:"+str(Corrs[i,j,t]))
					Corrs[j, i, t] = Corrs[i, j, t];
						
						# print('[{:d},{:d},{:f}], '.format(i,j, Corrs[i,j,t]), end="")
					# Corrs[i,j,t] = FisherTransform(LagCorrelation(ts_data[i,:], ts_data[j,:], t));
		
	# print np.count_nonzero(Corrs[:,:, 0]);
	# print Corrs[:,:, 0];
	# print
	max_freq = np.max(ts_data)
	std_by_t = np.zeros(t_range)				
	# write to file 
	# graphwriter = csv.writer(csvfile, delimiter=',', dialect='excel');
	for t in range(1, t_range):
		std_by_t[t] = np.std(Corrs[:,:,t])
		print(std_by_t[t])
		for i in range(0, map_m*map_n):
			if i in zero_inds: continue;
			ti = ts_data[i, time_start:time_stop].copy()
			neigh = Get8Neighbors(map_m, map_n, i)
			# print neigh
			for j in neigh:
				# if j%map_n == i//map_n: continue;
				if j in zero_inds: continue;
				tj = ts_data[j, time_start:time_stop].copy()
				if np.max(ti) < action_threshold or np.max(tj) < action_threshold  : continue
				# alpha_value = ((np.max(ti)+np.max(tj))/2) /max_freq
				alpha_value = ((GetDerivative(ti)+GetDerivative(tj))/2) / max_derivative
				graphwriter.writerow([time_start,t,i,j, ProbZ(np.fabs(Corrs[i,j,t].copy())/std_by_t[t], tn-t), alpha_value])


	# max_corrs = np.zeros(t_range*num_res_per_lag)
	# max_locs = np.zeros(t_range*num_res_per_lag)				
	# for t in range(1, t_range):
	# 	# std_by_t[t] =  GetStdWithoutDiag( Corrs[:,:,t] )
	# 	for i in range(0, num_res_per_lag):
	# 		max_locs[t*num_res_per_lag+i] = np.argmax(np.fabs(Corrs[:,:,t]))
	# 		max_corrs[t*num_res_per_lag+i] = np.max(np.fabs(Corrs[:,:,t])) 
	# 		# print "Result" + str(i) + "  " +  str(Corrs[max_locs[t+i]])
			
	# 		new_i = max_locs[t*num_res_per_lag+i]//(map_n*map_m)
	# 		new_j = int(max_locs[t*num_res_per_lag+i]%(map_n*map_m))
	# 		Corrs[new_i, new_j, t] = -1;
	
	
	# p_val = []
	# # print(std_by_t)
	# # print "FUCKFUCKFUCKFUCKFUCK"
	# # print max_corrs
	# # print max_locs
	# #Take all the edges with statistically significant edge chance
	# for c in range(0, len(max_corrs)):
	# 	p_val.append( 1.0-ProbZ(max_corrs[c]/std_by_t[c//num_res_per_lag], tn));

	# # p_val = map( (lambda x: 1.0-ProbZ(x, tn)), max_corrs/corr_std)
	# p_val_w_ind = []
	# for i in range(0, len(p_val)):
	# 	# make a tuple with (flat loc    pval      tval )
	# 	p_val_w_ind.append((max_locs[i], p_val[i], i//num_res_per_lag))
	# 	# print('edge: {:d}--->{:d}, p-val={:e}, t={:d}'.format(int(max_locs[i]//(map_n*map_m)), int(max_locs[i]%(map_n*map_m)), p_val[i], i//num_res_per_lag));
	# sorted_p_val = sorted(p_val_w_ind, key=lambda tup: tup[1])
	# # print "\nSorted P vals:"
	# # print sorted_p_val	


	# q = 0.15;
	# k = FDRController(sorted_p_val, q)
	# edge_list = set()
	# # print str(len(sorted_p_val)) + "VS" + str(k)
	# for i in range(0, k+1):
	# 	# edge_list.append( (sorted_p_val[i][0]//map_n, sorted_p_val[i][0]%map_n, sorted_p_val[i][1], sorted_p_val[i][2]))
	# 	# plot input structure
	# 	edge_list.add( ( sorted_p_val[i][0]//(map_n*map_m) ,sorted_p_val[i][0]%(map_n*map_m)))  #, sorted_p_val[i][1], sorted_p_val[i][2]) )
	# 	# print('edge: {:d}--->{:d}, p-val={:f}  t={:d}  '.format(int(floor(max_locs[sorted_p_val[i][0]]/n)), max_locs[sorted_p_val[i][0]]%n, sorted_p_val[i][1], sorted_p_val[i][0]))	
	
	# # print('TIME: {:d}    to    {:d}'.format(time_start, time_stop))
	# # for edge in edge_list:
	# # 	print('[{:d},{:d},0.5], '.format(int(edge[0]), int(edge[1])), end="")
	# # # print max_locs
	# # print('\n')
	# # # print max_corrs
	# return 0



##################Experimental Data Generation##################
def PinkNoise(alpha, m, tn):
	pdata = np.random.rand(m, tn)	
	funky = np.vectorize(lambda x: 1/pow(x, alpha))
	return funky(pdata)


coords = np.genfromtxt('bird_coords.csv', delimiter=',');
ts = np.genfromtxt('bird_timeseries.csv', delimiter=',');


# print(str(GetDerivative(ts[1706, time_start:time_stop])) + " " + str(GetDerivative(ts[1707, time_start:time_stop])))
# coords = np.genfromtxt('cassins_vireo_coords.csv', delimiter=',');
# ts = np.genfromtxt('cassins_vireo_timeseries.csv', delimiter=',');
zero_inds = FindZeroTimeSeries(ts);

a = time.clock()
# with open('cassins_vireo_map_vals.csv', 'wb') as csvfile:
with open('map_vals.csv', 'wb') as csvfile:
	graphwriter = csv.writer(csvfile, delimiter=',', dialect='excel');
	for i in range(0,42,2):
		GetValidEdges(ts, zero_inds, i, i+9, graphwriter)
print(time.clock() - a)











