# -*- coding: utf-8 -*-
# author=QIUKU
import numpy as np
import h5py
import os
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import argparse
from extract_cnn_vgg16_keras import VGGNet

# to hide tensorflow warnings
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

''' FutureWarning: Conversion of the second argument of issubdtype from `float` to `np.floating` is deprecated. 
    In future, it will be treated as `np.float64 == np.dtype(float).type`.
    from ._conv import register_converters as _register_converters'''
# TODO: resolve this FutureWarning


'''command line arguments parse procedure'''
'''returns a dict of command line argument'''
ap = argparse.ArgumentParser()
ap.add_argument("-query", required=True,
                help="Path to query which contains image to be queried")
ap.add_argument("-index", required=True,
                help="Path to index")
ap.add_argument("-result", required=True,
                help="Path for output retrieved images")
args = vars(ap.parse_args())


'''read in indexed images' feature vectors and corresponding image names'''
'''并将Dataset对象转为numpy.ndarray数组对象'''
h5f = h5py.File(args["index"], 'r')
img_feats_set = h5f['dataset_1'][:]
img_names_set = h5f['dataset_2'][:]
# print(img_feats.T)
# decode: bytes -> str
img_names_decode = [bytes(img_name).decode('utf-8', 'ignore') for img_name in img_names_set]
h5f.close()

print("--------------------------------------------------")
print("               searching starts                   ")
print("--------------------------------------------------")

# read and show query image
queryDir = args["query"]
queryImg = mpimg.imread(queryDir)
plt.title("Query Image")
plt.imshow(queryImg)
plt.show()
plt.close()

# init VGGNet16 model
model = VGGNet()

# extract query image's feature,compute similarity score and sort
query_img_feat = model.extract_feature(queryDir)
# dot()函数计算并返回两个numpy数组的内积
# 即**查询图片与图片库内各图片的相似度数组**
simil_scores = np.dot(query_img_feat, img_feats_set.T)
print("about shape:", query_img_feat.shape, img_feats_set[0].shape, img_feats_set.shape)
print("dot(query_img_feat, img_feats_set[1]): ", np.dot(query_img_feat, img_feats_set[1]))
# argsort函数返回将数组元素从小到大排列后所对应的原索引号组成的数组
# 列表切片操作[::-1]则将该索引数组的内容翻转输出
rank_index = np.argsort(simil_scores)[::-1]
rank_scores = simil_scores[rank_index]
# TODO
print(type(simil_scores), type(rank_index), type(rank_scores))
print("similarity score array: ", simil_scores)
print("img_index_array: ", rank_index)
print("sorted similarity score array: ", rank_scores)


# # 按要求的数量display相似图片
# max_ret = 3
# ret_img_list = [img_names_decode[index] for i, index in enumerate(rank_index[0:max_ret])]

# 按要求的相似度display相似图片
rank_scores_index = [index for index, element in enumerate(rank_scores) if element >= 0.6]
rank_index_ok = [rank_index[index] for index in rank_scores_index]
ret_img_names = [img_names_decode[index] for index in rank_index_ok]
# TODO
print("retrieve images's index: ", rank_index_ok)
print("retrieved images in order are: ", ret_img_names)
# show top max_ret retrieved result one by one
for i, im in enumerate(ret_img_names):
	img_path = args["result"] + "/" + str(im)
	image = mpimg.imread(img_path)
	plt.title("Searching Output %d" % (i + 1))
	plt.imshow(image)
	plt.show()

