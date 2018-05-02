"""
This simple flask apps accepts images from users,
and displays the image to the user without saving it to the location on the server.
"""

import io
import imghdr
from base64 import b64encode
from flask import Flask, request, \
	Response, make_response, g, \
	render_template, send_file, abort
from werkzeug.datastructures import FileStorage
from query_online import query
from PIL import Image

app = Flask(__name__)

'''
0.建立一个前后台链接;
1.route装饰器: 将URL路由映射到视图函数;
2.因此访问根目录'/'(GET请求)就会进入到hello_world()视图函数;
3.在此URL路径'/'(index.html)下发送的POST请求，将传给视图函数hello_world()进行处理;
4.默认情况下，路由只回应GET请求，但是通过route()装饰器传递methods参数可以改变这个行为;
5.需要手动对HTML做转义来保证应用的安全。Flask配备了Jinja2模板引擎，可以使用render_template()方法来渲染模板;
'''


@app.route('/', methods=['GET', 'POST'])
def upload_image():
	# Render index.html if request is a GET Request
	if request.method == 'GET':
		return render_template('index.html')
	# Process the from data if request is a POST Request
	elif request.method == 'POST':
		# Check if "image" key is in the form data; if false return 403 message
		if 'image' in request.files:
			# image is a FileStorage object
			image = request.files.get('image')
			print('uploaded image: ', image)
			# print("image binary data: ", image.read())

			# get uploaded image's extension and save()
			img_type = imghdr.what(image)
			print('extension of image: ', img_type)
			image.save('upload-images/'+image.filename)

			# query similar images and return a similar images's path list
			# convert a FileStorage object to a PIL Image object
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

		abort(403)  # 抛出403异常


# 自定义异常处理

# @app.errorhandler(500)
# def error500(e):
# 	return "您请求的页面后台发生错误！错误信息:" % e
#
#
# @app.errorhandler(404)
# def error404(e):
# 	return "您访问的页面飞去了火星！错误信息:" % e
#
#
# @app.errorhandler(403)
# def error403(e):
# 	return "您的权限不足！无法获取请求资源！错误信息:" % e


if __name__ == '__main__':
	app.run(port=5001)
