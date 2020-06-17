from flask import Flask
from flask import redirect, make_response
from flask import render_template
from os import path

app = Flask(__name__)
app.config.from_object('rhme_validation.config')
BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))))
print(BASE_PATH)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/', strict_slashes=False)
def beta_raiz():
    return redirect('/login')

from central_assinante.views.beta import _beta_login
from central_assinante.views.beta import _beta_home

@app.route('/ajax/recognize', strict_slashes=False, methods=['POST', 'OPTIONS'])
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



