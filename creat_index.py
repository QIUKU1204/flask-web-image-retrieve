# -*- coding: utf-8 -*-
# TODO: 使用VGGNet的extract_feature方法提取图片集的特征，并保存为一个特征集
# author=QIUKU
import h5py
import numpy as np
import argparse
from extract_cnn_vgg16_keras import VGGNet
import os

# to hide tensorflow warnings
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

''' 
FutureWarning: Conversion of the second argument of issubdtype from `float` to `np.floating` is deprecated. 
In future, it will be treated as `np.float64 == np.dtype(float).type`.
from ._conv import register_converters as _register_converters
'''
# TODO: resolve this FutureWarning

'''
command line arguments parse procedure
returns a dict of command line argument
'''
ap = argparse.ArgumentParser()
ap.add_argument("-database", required=True,
                help="Path to database which contains images to be indexed")
ap.add_argument("-index", required=True,
                help="Name of index file")
args = vars(ap.parse_args())


# Returns a list of filenames for all jpg images in a directory.
def get_imlist(path):
	return [os.path.join(path, f) for f in os.listdir(path) if f.endswith('.jpg')]


if __name__ == "__main__":

	db = args["database"]
	imgs_path_list = get_imlist(db)
	print(imgs_path_list)

	print("--------------------------------------------------")
	print("           feature extraction starts              ")
	print("--------------------------------------------------")

	feats = []
	names = []

	model = VGGNet()
	for i, img_path in enumerate(imgs_path_list):
		img_feat = model.extract_feature(img_path)
		# os.path.split(PATH)函数以PATH参数的最后一个'\'作为分隔符，
		# 返回目录名和文件名组成的元组,索引0为目录名，索引1则为文件名
		img_name = os.path.split(img_path)[1]
		feats.append(img_feat)
		names.append(img_name)
		print("extracting feature from image No. %d , %d images in total -> " % ((i + 1), len(imgs_path_list)), img_name)

	print("--------------------------------------------------")
	print("        writing feature extraction results        ")
	print("--------------------------------------------------")

	# file of storing extracted features
	# 创建一个h5py文件(对象)
	saved_name = args["index"]
	h5f = h5py.File(saved_name, 'w')

	# np.array()方法将list列表转为numpy数组
	feats = np.array(feats)

	# create_dataset method only accepts ascii encoding character
	# encode: str -> bytes
	names_ascii = [str(name).encode('ascii', 'ignore') for name in names]
	# 为h5py文件创建两个数据集对象
	h5f.create_dataset('dataset_1', data=feats)
	h5f.create_dataset('dataset_2', data=names_ascii)
	h5f.close()




