from flask import Flask
from flask import redirect, make_response, request
from flask import render_template
from mathreader import api
from mathreader.helpers.exceptions import GrammarError, LexicalError, SintaticError
import os
import inspect
import json
import cv2
import base64
import numpy as np
import re
import time

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))))

# app.config.from_object('config')
# api.config().set_app_debug_mode_image('disabled')
# with open("img.txt", 'w') as f:
#     json.dump(str(data), f)
# # np.savetxt('test.txt', img)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/ajax/recognize', strict_slashes=False, methods = ['POST', 'OPTIONS'])
def recognize():

    latex = ""
    error = False

    try:

        data = request.get_json()
        img_data = data['image']
        img_data = img_data.split(',')[1]

        hme_recognizer = api.HME_Recognizer()
        hme_recognizer.load_image(img_data)
        latex, modified_img = hme_recognizer.recognize()
        hme_recognizer = None

    except Exception as e:
        if hasattr(e, 'data'):
            if 'latex_string_original' in e.data:
                latex = e.data['latex_string_original']
                error = True
            print(e.data)

    return json.dumps({
        'latex': latex,
        'error': error
    })


def write_show_image(img, name):
    cv2.imwrite('%s.jpg' % name, img)
    cv2.imshow('Image', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__=='__main__':    
    app.run(debug=True)
