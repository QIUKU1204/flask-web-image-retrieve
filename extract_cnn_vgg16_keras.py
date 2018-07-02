# -*- coding: utf-8 -*-
# TODO: 定义一个基于VGG16的深度神经网络模型VGGnet
# author=QIUKU
import numpy as np
from keras.applications.imagenet_utils import decode_predictions
from numpy import linalg as LA
from keras.applications.vgg16 import VGG16
from keras.preprocessing import image
from keras.applications.vgg16 import preprocess_input
import keras


class VGGNet:
	def __init__(self):
		"""
        # weights: 'imagenet' -- 加载预训练权重
		# pooling: 'max' or 'avg' -- 全局平均池化或全局最大值池化
		# input_shape: (width, height, 3), width and height should >= 48
		# include_top=False -- 不保留顶部的3个全连接层
		"""
		self.input_shape = [224, 224, 3]
		self.weight = 'imagenet'
		self.pooling = 'max'
		# 返回一个VGG16模型的实例 - model
		self.model = VGG16(weights=self.weight,
		                   input_shape=(self.input_shape[0], self.input_shape[1], self.input_shape[2]),
		                   pooling=self.pooling,
		                   include_top=False)
		# 绑定一个VGG16模型的方法
		self.model.predict(np.zeros((1, 224, 224, 3)))

	'''
	Use vgg16 model to extract features.
	Output normalized feature vector.
	'''

	def extract_feature(self, img):  # img or img_path

		# img = image.load_img(img_path, target_size=(self.input_shape[0], self.input_shape[1]))
		img = img.resize(size=(self.input_shape[0], self.input_shape[1]))
		img = image.img_to_array(img)
		print(type(img), 'img_to_array(img): ', img.shape)
		img = np.expand_dims(img, axis=0)
		print(type(img), "expand_dims(img):", img.shape)

		'''
		preprocess_input()函数完成图像数据预处理工作
		图像数据预处理能够提高算法的运行效果
		mode='caffe' or mode='tf' 
		'''
		img = preprocess_input(img, mode='caffe')
		print('reprocess_input(img): ', img.shape)

		'''
		Generates output predictions for the input samples.
		Returns Numpy array(s) of predictions. 
		predict() method generated 预测分类结果-predictions.
		'''
		feat = self.model.predict(img)
		print('predict(img): ', feat.shape)

		'''
		decode_predictions()函数将预测分类结果predictions
		解码为易读的键值对：标签号、标签名以及该标签的概率
		'''
		# feat_decode = decode_predictions(feat)
		# print("prediction:", feat_decode)

		'''
		feat[0]: 将二维数组转换为一维数组
		LA.norm(): 特征向量归一化/标准化
		'''
		norm_feat = feat[0] / LA.norm(feat[0])
		print('feat[0]: ', feat[0].shape)
		print('LA.norm(feat[0]): ', LA.norm(feat[0]))
		return norm_feat
