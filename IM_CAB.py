import math
from scipy.sparse.csgraph import connected_components
from scipy.sparse import csr_matrix
import datetime
import os.path
from conf import sim_files_folder, save_address
from sklearn import linear_model
from random import choice, random, sample
import networkx as nx
import numpy as np
from BanditAlgorithms_LinUCB import *
import collections
class CABUserStruct(LinUCBUserStruct):
	def __init__(self, featureDimension,  lambda_, userID):
		LinUCBUserStruct.__init__(self,featureDimension = featureDimension, lambda_= lambda_, userID = userID)
		self.reward = 0
		self.I = lambda_*np.identity(n = featureDimension)	
		self.counter = 0
		self.CBPrime = 0
		self.CoTheta= np.zeros(featureDimension)
		self.d = featureDimension
		self.ID = userID
		self.cluster = {}
	def updateParameters(self, articlePicked_FeatureVector, click):
		self.A += np.outer(articlePicked_FeatureVector,articlePicked_FeatureVector)
		self.b +=  articlePicked_FeatureVector*click
		self.AInv = np.linalg.inv(self.A)
		self.UserTheta = np.dot(self.AInv, self.b)
		self.counter+=1
		#print(self.CoTheta)
	def getCBP(self, alpha, article_FeatureVector,time):
		var = np.sqrt(np.dot(np.dot(article_FeatureVector, self.AInv),  article_FeatureVector))
		pta = alpha * var#*np.sqrt(math.log10(time+1))
		return pta

class CABAlgorithm():
	def __init__(self, G, seed_size, oracle, dimension, alpha,  alpha_2, lambda_, FeatureDic, FeatureScaling, gamma):
		self.time = 0
		self.G = G
		self.oracle = oracle
		self.seed_size = seed_size
		self.dimension = dimension
		self.alpha = alpha
		self.alpha_2 = alpha_2
		self.lambda_ = lambda_
		self.gamma = gamma
		self.FeatureDic = FeatureDic
		self.FeatureScaling = FeatureScaling

		self.users = {}  #Nodes
		self.currentP =nx.DiGraph()
		for u in self.G.nodes():
			self.users[u] = CABUserStruct(dimension, lambda_, u)
			for v in self.G[u]:
				self.currentP.add_edge(u,v, weight=random())
		n = len(self.users)

		self.userIDSortedList = list(self.users.keys())
		self.userIDSortedList.sort()
		self.SortedUsers = collections.OrderedDict(sorted(self.users.items()))

		self.a=0

	def decide(self):
		self.time +=1
        self.updateGraphClusters()
		S = self.oracle(self.G, self.seed_size, self.currentP)
		return S

	def updateGraphClusters(self):
        maxPTA = float('-inf')
        articlePicked = None
		for u in S:
			WI = self.users[u].UserTheta
			for (u, v) in self.G.edges(u):
				clusterItem=[]
				featureVector = self.FeatureScaling*self.FeatureDic[(u,v)]
				CBI = self.users[u].getCBP(self.alpha, featureVector, self.time)
				WJTotal=np.zeros(WI.shape)
				CBJTotal=0.0
	            for i in range(len(self.users)):
	            	j = self.userIDSortedList[i]
	                WJ = self.users[j].UserTheta
	                CBJ = self.users[j].getCBP(self.alpha, featureVector, self.time)
	                compare= np.dot(WI, featureVector) - np.dot(WJ, featureVector)               
	                if (j != userID):
	                    if (abs(compare) <= CBI + CBJ):
	                        clusterItem.append(self.users[j])
	                        WJTotal += WJ
	                        CBJTotal += CBJ
	                else:    
	                    clusterItem.append(self.users[userID])
	                    WJTotal + =WI
	                    CBJTotal += CBI
	            CW= WJTotal/len(clusterItem)
	            CB= CBJTotal/len(clusterItem)
	            x_pta = np.dot(CW,featureVector) + CB
	            if x_pta > 1:
	            	x_pta = 1
	            self.currentP[u][v]['weight']  = x_pta
	            self.users[u].cluster[v] = clusterItem

	def updateParameters(self, S, live_nodes, live_edges):
		gamma = self.gamma
		for u in S:
			for (u, v) in self.G.edges(u):
				featureVector = self.FeatureScaling*self.FeatureDic[(u,v)]
				if (u,v) in live_edges:
					reward = live_edges[(u,v)]
				else:
					reward = 0
				if (self.users[u].getCBP(self.alpha, featureVector, self.time) >= gamma):
					self.users[u].updateParameters(featureVector, reward)
				else:
					clusterItem = self.users[u].cluster[v]
					for i in range(len(clusterItem)):
						if(self.cluster[i].getCBP(self.alpha, featureVector, self.time) < gamma / 4):
							self.cluster[i].updateParameters(featureVector, reward)
							self.a +=1
				clusterNow.append(self.cluster[i].ID)

