import logging
import sys
import os
import subprocess
from logging import Formatter, FileHandler
import gridfs
import pymongo
from pymongo import MongoClient, TEXT
from flask import Flask, request, jsonify, render_template, redirect
from ocr import process_image


app = Flask(__name__)
_VERSION = 1
UPLOAD_FOLDER = '../PICTURES_LATEX'

@app.route("/")
def hello():
    return render_template("layout.html")


@app.route("/send-image", methods=["POST"])
def sendImage():
    print "hit hit"
    title = request.form['title']
    userid = request.form['userId']
    print title
    print userid
    request.files['file'].save('abc.jpg')
    return "send image endpoint hit"


@app.route('/v{}/ocr'.format(_VERSION), methods=["POST"])
def ocr():
    try:
        url = request.json['image_url']
        if 'jpg' in url:
            output = process_image(url)
            return jsonify({"output": output})
        else:
            return jsonify({"error": "only .jpg files, please"})
    except IOError as e:
        print e
        return jsonify(
            {"error": "IO PROBLEMS"}
        )
    except:
        print "Unexpected error:", sys.exc_info()[1]
        return jsonify(
            {"error": "Did you mean to send: {'image_url': 'some_jpeg_url'}"}
        )


def textProcessing(text):
    return text.replace('\n', '\\')


@app.route('/get-tex', methods=["POST"])
def toTex():
    body = request.form['data']
    title = "Today I win"
    print('beginning')
    print(body)
    text = textProcessing(body)
    print('with replacement')
    print(text)
    return tex(title, text)


def tex(title, bdy):
    latexFile = render_template("general.tex", title=title, body=bdy)
    titleNoSpace=title.replace(' ', '')
    fileDir = "static/static/"
    latexFileName = titleNoSpace + ".tex"
    latexFileWithDir = fileDir + latexFileName
    with open(latexFileWithDir, "wb") as fh:
        fh.write(latexFile)
    failure = subprocess.call(['pdflatex', '-interaction=nonstopmode', latexFileWithDir], shell=False)
    os.rename(titleNoSpace + ".pdf", fileDir + titleNoSpace + ".pdf")
    addToDB(titleNoSpace, bdy)
    if (not failure):
        os.remove(latexFileName)
        os.remove(titleNoSpace + ".log")
        os.remove(titleNoSpace + ".aux")
        return "yay"
    else:
        return "no"


def addToDB(title, data):
    collection = db['test-collection']
    post = {"author": "Rose",
            "title": title,
            "data": data}
    collection.insert_one(post)
    collection.create_index([('data', TEXT)], default_language='english')
    return "ok"


@app.route('/get-my-pdf')
def redirectToPDF():
    fileName = request.args['fileName']
    fileDir = "static/static/"

    return redirect(fileDir + fileName + ".pdf")


# @app.errorhandler(500)
# def internal_error(error):
#     print str(error)
#     return 'ok'
#
#
# @app.errorhandler(404)
# def not_found_error(error):
#     print str(error)
#     return 'ok'@app.errorhandler(500)
# def internal_error(error):
#     print str(error)
#     return 'ok'
#
#
# @app.errorhandler(404)
# def not_found_error(error):
#     print str(error)
#     return 'ok'

client = MongoClient('mongodb://rose:admin@ds041571.mongolab.com:41571/latex-my-notes')
db = client['latex-my-notes']

if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: \
            %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
