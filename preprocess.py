import pickle
import numpy as np
import tensorflow as tf
import csv
import gzip
import requests
import os
from concurrent.futures import ThreadPoolExecutor


"reference to turn images to bytes: https://github.com/gskielian/JPG-PNG-to-MNIST-NN-Format/blob/master/convert-images-to-mnist-format.py"

filename = "./data/inputs-ubytes"



def download(url):
	i = requests.get(url).content
	#print(type(i))
	#i = np.array([i])
	#print(type(i))
	#print(i.shape)
	return i

def early_processing(cat_path,image_path, images, labels):
	"""
	Given a file path, returns an array of
	normalized inputs (images) and an array of labels.
	"""
	id2cat = {}
	id2image = {}
	id2image2 = {}
	image2id = {}


	# categories sheet
	with open(cat_path, newline='') as f:
		reader = csv.reader(f)
		for row in reader:
			try:
				id2cat[row[0]].append(row[1])
			except:
				id2cat[row[0]] = [row[1]]

	# image sheet
	with open(image_path, newline='') as f2:
		reader = csv.reader(f2)
		for row in reader:
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


	# writing to csv
	"""write=[]
	for id in id2image:
		writing={}
		writing['event_id'] = id
		writing['image'] = id2image[id]
		write.append(writing)

	with open(new_path, 'w') as new:
		writer = csv.DictWriter(new, fieldnames=('event_id', 'image'))
		writer.writeheader()
		writer.writerows(write)"""

	# convert two dictionaries to one 2d array
	image2cat = []
	for id in id2image:
		try:
			image2cat.append([id2image[id],id2cat[id]])
		except:
			pass

	# convert one array into two arrays
	altogether = np.array(image2cat).T
	image_array = altogether[0]
	cat_array = altogether[1]

	big_bad_array = []
	# download images

	print("starting downloading")
	with ThreadPoolExecutor(max_workers=14) as executor:
		big_bad_array = executor.map(download, image_array)

	print(np.array(big_bad_array).shape)

	print("writing to gz file")
	# write byte img_file into a file
	with gzip.open(images, 'wb') as f:
		for bba in big_bad_array:

			f.write(bba)

	# convert cat array into a bytes
	cat2byte = []
	for c in cat_array:
		for word in c:
			cat2byte.append(bytes(word, "ascii"))

	# write byte cat_array into a file
	with gzip.open(labels, 'wb') as f2:
		for c in cat2byte:
			f2.write(c)


def get_data(cat_path,image_path, images, labels):
	# obtain the images and labels gz files ONCE
	early_processing(cat_path, image_path, images, labels)

	# read from images gz file
	# bug: I think this works, but it takes forever
	# multi threading might also be possible here, but would need locks
	# possible implementation of file reading lock: https://blog.majid.info/a-reader-writer-lock-for-python/
	"""with open(images, 'rb') as f, gzip.GzipFile(fileobj=f) as bytestream:
		img_array = np.frombuffer(bytestream.read(), dtype=np.uint8)
	"""

	# read from labels gx file
	with open(labels, 'rb') as f2, gzip.GzipFile(fileobj=f2) as bytestream2:
		cat_array = np.frombuffer(bytestream2.read(), dtype=np.uint8)

#	print(np.arr(img_array).shape)

	# TODO: pad images
	# normalization
	# reshaped_inputs = subset_inputs.reshape(subset_inputs.shape[0],3,32,32).transpose(0,2,3,1).astype("float")
	# normalized_inputs = reshaped_inputs / 255


	return cat_array #, img_array

get_data( "./data/categories.csv", "./data/images.csv", "./data/inputs-ubytes", "./data/labels-ubytes")

#get_data('d:/DeepLearning/FinalProj/categories.csv','d:/DeepLearning/FinalProj/images.csv','d:/DeepLearning/FinalProj/new.csv')
