import pickle
import numpy as np
import tensorflow as tf
import csv
import requests
import os

def get_data(cat_path,image_path,new_path):
	"""
	Given a file path, returns an array of 
	normalized inputs (images) and an array of labels. 
	"""
	id2cat = {}
	id2image = {}
	id2image2 = {}
	image2id={}

	#categories sheet
	with open(cat_path,newline='') as f:
		reader = csv.reader(f)
		for row in reader:
			try:
				#print('previous',row[0],row[1],id2cat[row[0]])
				id2cat[row[0]].append(row[1])
				#print('appending',row[0],id2cat[row[0]])
			except:
				id2cat[row[0]] = [row[1]]
				#print('initializing',row[0],id2cat[row[0]])
		#print(len(id2cat))

	#image sheet
	with open(image_path,newline='') as f:
		reader = csv.reader(f)
		for row in reader:
			#id2image2[row[0]]=row[1]
			image2id[row[1]]=row[0]
		id2image = dict([(value,key)for key,value in image2id.items()])
		""" for key,value in image2id.items():
			try:
				assert value in id2image
				id2image[value].append(key)
				print('appending',id2image[value],value,key)
				break
			except:
				id2image[value]=key
				print('initializing',id2image[value],value,key) """
		#print(len(id2image))
		#print(len(image2id)) # there is actually a bug to fix.

	#writing to csv
	write=[]
	for id in id2image:
		writing={}
		writing['event_id']=id
		writing['image']=id2image[id]
		write.append(writing)
	with open(new_path,'w') as new:
		writer = csv.DictWriter(new,fieldnames=('event_id','image'))
		writer.writeheader()
		writer.writerows(write)

	#convert two dictionaries to one 2d array
	image2cat=[]
	for id in id2image:
		try:
			image2cat.append([id2image[id],id2cat[id]])
		except:
			pass
	#print(image2cat)

	#convert one array into two arrays
	altogether = np.array(image2cat).T
	image_array = altogether[0]
	cat_array = altogether[1]

	#TODO: replace links with image arrays
	for i in image_array:
		i = requests.get(i).content
		print(i)#bytes
	print(image_array.shape)

	#TODO: pad images

	#normalization
	#reshaped_inputs = subset_inputs.reshape(subset_inputs.shape[0],3,32,32).transpose(0,2,3,1).astype("float")
	#normalized_inputs = reshaped_inputs / 255

	return image_array,cat_array

get_data('d:/DeepLearning/FinalProj/categories.csv','d:/DeepLearning/FinalProj/images.csv','d:/DeepLearning/FinalProj/new.csv')