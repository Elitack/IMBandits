import os
from Oracle.generalGreedy import generalGreedy
from Oracle.degreeDiscount import degreeDiscountIC, degreeDiscountIC2, degreeDiscountIAC, degreeDiscountIAC2, degreeDiscountIAC3

save_address = "./SimulationResults"

graph_address = './datasets/Flickr-Topic-SimEdge/Small_Final_SubG.G'
topic_address = './datasets/Flickr-Topic-SimEdge/TopicTheta.list'
feature_address = './datasets/Flickr-Topic-SimEdge/Small_Final_Normalized_edgeFeatures_uniform_dim4.dic'

dataset = 'Flickr' #Choose from 'default', 'NetHEPT', 'Flickr'
FeatureScaling = 1.0
batchSize = 1
alpha = 0.1
alpha_2 = 0.1
lambda_ = 0.3
gamma = 0
dimension = 4
seed_size = 40
iterations = 100
cores = 4

oracle = degreeDiscountIAC3
