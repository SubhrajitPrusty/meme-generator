from flask import Flask, request, render_template, redirect, url_for
from werkzeug.utils import secure_filename
from PIL import Image
import os
import time
import generate
from gevent.pywsgi import WSGIServer


UPLOAD_FOLDER = os.path.join("static","upload")
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

app = Flask(__name__, static_url_path="/static")
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/", methods=['GET','POST'])
def index():
	if request.method == 'POST':
		print(request.files)
		print(request.form)
		if 'image' not in request.files:
			error = "No file part"
			return render_template("error.html", context=error)
		else:
			file = request.files['image']
			print(file.filename)
			print(len(file.filename))
			if len(file.filename) < 1:
				error = "No file selected"
				return render_template("error.html", context=error)

			if file and allowed_file(file.filename):
				filename = secure_filename(file.filename)
				ufpath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
				file.save(ufpath)
				if request.form['memetext']:
					text = request.form.get('memetext')

					img = Image.open(ufpath)
					if img.height < 100 or img.width < 100:
						img = img.resize((img.width*4, img.height*4))
					elif img.height < 200 or img.width < 200:
						img = img.resize((img.width*2, img.height*2))
					img = generate.memegen(img, text)

					fname = "meme-{}.png".format(int(time.time()))
					fpath = 'static/images/'+fname

					print(fpath)
					img.save(fpath)
					imgurl = url_for('static',filename='images/'+fname)
					return render_template("download.html", context=imgurl)
				else:
					error = "Invalid input, try again"
					return render_template("error.html", context=error)
			else:
				error = "filetype not allowed"
				return render_template("error.html", context=error)
	else:
		return render_template("index.html")


if __name__ == '__main__':
	port = int(os.environ.get('PORT', 5000))
	http_server = WSGIServer(('',port),app)
	http_server.serve_forever()