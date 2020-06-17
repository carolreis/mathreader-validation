from flask import Flask
from flask import redirect, make_response, request
from flask import render_template
import os
import inspect
import json
import cv2
import base64
import numpy as np
import re
from PIL import Image
from io import BytesIO
import time

def decode_base64(data, altchars=b'+/'):
    """Decode base64, padding being optional.

    :param data: Base64 data as an ASCII byte string
    :returns: The decoded byte string.

    """
    data = re.sub(rb'[^a-zA-Z0-9%s]+' % altchars, b'', data)  # normalize
    missing_padding = len(data) % 4
    if missing_padding:
        data += b'='* (4 - missing_padding)
    return base64.b64decode(data, altchars)

def data_uri_to_cv2_img(uri):
    # nparr = np.fromstring(uri.decode('base64'), np.uint8)
    img = uri.split(',')[1]
    # img = np.frombuffer(base64.b64decode(img), np.uint8)
    img = np.fromstring(base64.b64decode(img), np.uint8)
    return cv2.imdecode(img, cv2.IMREAD_COLOR)


def getI420FromBase64(codec, image_path):
    base64_data = re.sub('^data:image/.+;base64,', '', codec)
    byte_data = base64.b64decode(base64_data)
    image_data = BytesIO(byte_data)
    img = Image.open(image_data)
    img.save(image_path + '.png', "PNG")

app = Flask(__name__)
app.config.from_object('config')
BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))))
print(BASE_PATH)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/ajax/recognize', strict_slashes=False, methods=['POST', 'OPTIONS'])
def teste():

    # data = request.data
    # img_data = data
    # decoded_image = base64.decodebytes(img_data) # in bytes :^)
    # with open("imageToSave.png", "wb") as fh:
    #     fh.write(decoded_image)
    # return json.dumps({'message': 'ok'})

    data = request.get_json()
    img_data = data['image']
    img_data = img_data.split(',')[1]
    # nparr = np.fromstring(base64.b64decode(encoded_data), np.uint8)
    # img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    # cv2.imshow('abacate', img)

    im_bytes = base64.b64decode(img_data)
    im_arr = np.frombuffer(im_bytes, dtype=np.uint8)  # im_arr is one-dim Numpy array
    img = cv2.imdecode(im_arr, flags=cv2.IMREAD_COLOR)
    cv2.imwrite('%s.jpg' % 'BLABLA', img)
    cv2.imshow('abacate', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    return json.dumps({'latex': "alright"})
'''
@app.route('/', strict_slashes=False)
def beta_raiz():
    return redirect('/login')

from central_assinante.views.beta import _beta_login
from central_assinante.views.beta import _beta_home

def beta_ajax_financial():


    # JSON data received
    data = request.get_json()

    if data is None:
        return to_json(data=data, message='No JSON', status_code=345)  # TODO: definir code




    """ Realiza a busca da saude financeira de um usuario logado """
    username = get_session_logged_user()

    # Get Financial
    account = Helpers.requestDealerApi('account', username, params='adminOnly=true', cache=True)
    financialStatus = Helpers.requestDealerApi('invoice', username, params={'financialStatus': 'true'}, cache=False)

    try:
        statusCustomer = financialStatus and Invoice(financialStatus, account).to_dict()
    except:
        statusCustomer = None

    response = make_response(json.dumps({"statusCustomer": statusCustomer}))

    if response:
        response.headers['Content-Type'] = 'application/json'

    return response


@app.route('/login', strict_slashes=False, methods=['GET'])
def beta_login():
    start_time = datetime.now()

    # Registry EventHub Page Load
    EventHub().registry_page(sys._getframe().f_code.co_name)

    user = User()
    username = ''
    origin = request.args.get('_origem', 'DEFAULT')

    if user.isLoggedIn():
        logger.debug(u'Redireciona usuário para tela inicial, por já estar logado.')
        return redirect('/inicio')

    # Token de seguranca para evitar CSRF nos formularios
    token = uuid.uuid4().hex
    session['token'] = token

    data = {
        "params": {},
        "client": None,
        "data": {},
        "token": token
    }

    data['data']['workspace'] = "Central do Assinante [beta]"
    data['data']['includerPre'] = Helpers.requestIncluder('pre', Helpers.check_tpn_params(), True)
    data['data']['includerPost'] = Helpers.requestIncluder('post', Helpers.check_tpn_params(), True)

    # Querystring params
    for key, value in request.args.iteritems():
        data["params"][key] = value

    data['data']['useCaptchaLogin'] = app.config['USE_CAPTCHA_LOGIN']
    data['data']['captchaKey'] = app.config['INVISIBLE_RECAPTCHA_PUBLIC_KEY']

    pathTemplateCover = 'beta/login.html'
    response = render_template(pathTemplateCover, **data)

    # EventHub para saber o quanto demorou para carregar a pagina
    EventHub().registry_page(sys._getframe().f_code.co_name, end=True, time_spent=get_time_spent(start_time))

    return response
'''

if __name__=='__main__':    
    app.run(debug=True)
