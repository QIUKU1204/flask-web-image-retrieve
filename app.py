# -*- coding: utf-8 -*-
# TODO: 基于Flask的WEB应用
# author=QIUKU

import io
import imghdr
from base64 import b64encode
from flask import Flask, request, render_template,\
	Response, make_response, g, send_file, abort
from werkzeug.datastructures import FileStorage
from query_online import query
from PIL import Image

# 创建Flask实例，即一个web应用/wsgi应用
app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])  # 默认情况下，URL路由只回应GET请求，通过route()装饰器传递methods参数可以改变这个行为;
def upload_image():
	# Render index.html if request is a GET Request
	if request.method == 'GET':
		return render_template('index.html')
	# Process the form data if request is a POST Request
	elif request.method == 'POST':
		# Check if "image" key is in the form data else return 403 message
		if 'image' in request.files:
			# image is a FileStorage object
			image = request.files.get('image')
			print('uploaded image: ', image)

			# get uploaded image's extension and save
			img_type = imghdr.what(image)
			print('extension of image: ', img_type)
			print('iamge filename: ', image.filename)
			image.save('upload-images/' + image.filename)

			# query and return a similar images' path list
			# convert a FileStorage obj to a PIL Image object
			similar_imgs = query(Image.open(image))  # Image.open() can used by any file obj

			return render_template('view_image.html', images=similar_imgs)

		# # open image file and get an in-memory bytes buffer
		# with open(similar_imgs[1], 'rb') as image_fp:
		# 	# convert a File obj to a FileStorage obj
		# 	# FileStorage obj have save() method which File obj does not have
		# 	image_fs = FileStorage(image_fp)
		#
		# 	# returns a response obj, and show as image at webpage
		# 	resp = Response(image_fp.read(), mimetype='image/jpeg')
		# 	# return a response obj, and show as binary data at webpage
		# 	resp = make_response(image_fp.read())
		#   return resp
		#
		# 	# Sends the contents of a file to the client
		# 	# Use the WSGI server's file_wrapper support
		# 	return send_file(io.BytesIO(image_fs.read()), mimetype='image/{}'.format(image_type),
		# 	                 attachment_filename='image.pdf')

		return render_template('index.html')  # 发生403异常时的处理


# Flask封装了一个简单的开发用WSGI服务器，通过调用run()在服务器上运行flask应用
if __name__ == '__main__':
	# 当host='0.0.0.0'时，内置WSGI服务器外部可访问
	app.run(host='127.0.0.1', port=5001)
