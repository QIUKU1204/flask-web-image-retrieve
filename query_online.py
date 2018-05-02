# -*- coding: utf-8 -*-
# author=QIUKU
import numpy as np
import h5py
import os
from extract_cnn_vgg16_keras import VGGNet
from PIL import Image

# to hide tensorflow warnings
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'


def query(image):  # image or image_path
	# 读取图片特征集
	h5f = h5py.File('CNN_extracted_image_feature_many.h5', 'r')
	img_feats_set = h5f['dataset_1'][:]
	img_names_set = h5f['dataset_2'][:]
	img_names_decode = [bytes(img_name).decode('utf-8', 'ignore') for img_name in img_names_set]
	h5f.close()

	# init VGGNet16 model
	model = VGGNet()

	# extract query image's feature,then compute similarity score and sort
	query_img_feat = model.extract_feature(image)
	# dot()函数计算并返回两个numpy数组的内积
	# 即**查询图片与图片库内各图片的相似度数组**
	simil_scores = np.dot(query_img_feat, img_feats_set.T)
	# argsort()函数返回将数组元素从小到大排列后所对应的原索引号组成的数组
	# 列表切片操作[::-1]则将该索引数组的内容翻转输出
	rank_index = np.argsort(simil_scores)[::-1]
	rank_scores = simil_scores[rank_index]

	# # output similar images by required number
	# max_ret = 3
	# ret_img_list = [img_names_decode[index] for i, index in enumerate(rank_index[0:max_ret])]

	# output similar images by similarity scores
	rank_scores_index = [index for index, element in enumerate(rank_scores) if element >= 0.5]
	rank_index_ok = [rank_index[index] for index in rank_scores_index]
	ret_img_nams = ['../static/database-many/'+img_names_decode[index] for index in rank_index_ok]
	# TODO
	print("retrieve images's index: ", rank_index_ok)
	print('retrieved images in order are: ', ret_img_nams)
	# get similary images and put them in an image list
	# Image.open() method returns An :py:class:`~PIL.Image.Image` object.
	# similar_images = [Image.open("database-less/"+name) for name in ret_img_nams]
	return ret_img_nams


__all__ = [query]


if __name__ == '__main__':
	# query("4-002.jpg")
	query_image = Image.open('../static/database-many/301.jpg', mode='r')
	query(query_image)
