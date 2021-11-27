import pickle
import numpy as np
import tensorflow as tf
import csv
import os

def get_data(cat_path,image_path):
	"""
	Given a file path, returns an array of 
	normalized inputs (images) and an array of labels. 
	"""
	id2cat = {}
	id2image = {}
	with open(cat_path,newline='') as f:
		reader = csv.reader(f)
		for row in reader:
			id2cat[row[0]]=row[1]
		print(len(id2cat))
	with open(image_path,newline='') as f:
		reader = csv.reader(f)
		for row in reader:
			id2image[row[0]]=row[1]
		print(len(id2image))
	#reshaped_inputs = subset_inputs.reshape(subset_inputs.shape[0],3,32,32).transpose(0,2,3,1).astype("float")
	#normalized_inputs = reshaped_inputs / 255

	return None

get_data('d:/DeepLearning/FinalProj/categories.csv','d:/DeepLearning/FinalProj/images.csv')