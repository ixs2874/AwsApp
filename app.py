"""
This module uses Chalice serverless microframework to build a simple
publishing service with 3 functions:service should do three things:
1. /status: Return a status message from the server.
2. /post/img: accept an image upload, store it on S3, and returns URL of the image.
3. /process/api: Consume a publicly available feed. ToDo
"""

import boto3
import base64
import logging
import requests
from chalice import (Chalice, NotFoundError, BadRequestError)

app = Chalice(app_name='talon')
app.log.setLevel(logging.DEBUG)
app.debug = True

OBJ = {}
S3 = boto3.client('s3', region_name='us-east-1')
BUCKET = {'bucket': 'ixs2874'}


@app.route('/set/bucket/{bucket}', methods=['GET'])
def set_bucket(bucket):

    BUCKET['bucket'] = str(bucket)
    return BUCKET


@app.route('/get/bucket', methods=['GET'])
def get_bucket():

    return BUCKET


@app.route('/status')
def status():
    """This endpoint returns timestamp and some information about the server.

    :return: Returns status of the system.
    """
    from time import gmtime, strftime
    import platform
    import os
    return {'1: status': 'OK',
            '2: time': strftime("%Y-%m-%d %H:%M:%S", gmtime()),
            '3: system': platform.system(),
            '4: version': platform.version(),
            '5: machine': platform.machine(),
            '6: processor': platform.processor(),
            '7: uname': os.uname()
            }


@app.route('/post/img', methods=['POST'])
def post_image():
    """This endpoint uploads an image to ixs2874 S3 bucket on AWS.

    :return: Returns URL of the image on S3.
    """
    from subprocess import Popen, PIPE
    import uuid

    body = app.current_request.json_body
    image = base64.b64decode(body['data'])
    img_format = {'jpg': 'jpeg', 'png': 'png'}[body.get('format', 'jpg').lower()]
    mode = {'max': '', 'min': '^', 'exact': '!'}[body.get('mode', 'max').lower()]
    width = int(body.get('width', 128)) + 256
    height = int(body.get('height', 128)) + 256

    cmd = [
        'convert',  # ImageMagick Convert
        '-',  # Read original picture from stdin
        '-auto-orient',  # Detect picture orientation from metadata
        '-thumbnail', '{}x{}{}'.format(width, height, mode),  # Thumbnail size
        '-extent', '{}x{}'.format(width, height),  # Fill if original picture is smaller than thumbnail
        '-gravity', 'Center',  # Extend (fill) from the thumbnail middle
        '-unsharp', ' 0x.5',   # Un-sharpen slightly to improve small thumbnails
        '-quality', '100%',    # Thumbnail JPG quality
        '{}:-'.format(img_format),  # Write thumbnail with `format` to stdout
    ]

    p = Popen(cmd, stdout=PIPE, stdin=PIPE)
    thumbnail = p.communicate(input=image)[0]

    if not thumbnail:
        raise BadRequestError('Image format not supported. > {}'.format(body['data']))

    filename = 'talon/homer_{}_{}x{}.{}'.format(uuid.uuid4(), width, height, img_format)
    S3.put_object(
            Bucket=BUCKET['bucket'],
            Key=filename,
            Body=thumbnail,
            ACL='public-read',
            ContentType='image/{}'.format(img_format),
    )
    return {
        'image url': 'https://s3.amazonaws.com/{}/{}'.format(BUCKET['bucket'], filename)
    }


@app.route('/', cors=True)
def index():
    """Index endpoint defaults to status()

    :return: Returns status
    """
    return status()


@app.route('/rates', methods=['GET'])
def get_eur_rates():
    return get_forex_rates('EUR')


@app.route('/rates/{base}', methods=['GET'])
def get_forex_rates(base):
    """Fixer.io is a free JSON API for current and historical foreign exchange rates.
       It relies on daily feeds published by the European Central Bank.

    :type base: str
    :param base: base currency
    :return: dictionary of major currencies with rates to base currency.
    """

    url = 'http://api.fixer.io/latest?base={}'.format(base.upper())
    try:
        response = requests.get(url)
        stat = response.status_code
        if stat != 200:

            return {
                'Public API Access Error': 'api.fixer.io get request returned status: {}'.format(stat)
            }
        else:
            rates = response.json()['rates']
            return {
                'base currency': base,
                'rates': rates
            }
    except requests.ConnectionError as err:
        raise BadRequestError('Public APIs Connection Error > {}'.format(err))


@app.route('/rates/convert/{fromm}/to/{to}/amount/{amount}', methods=['GET'])
def forex_convert(from_x, to_x, amount):
    """Converts currencies

    :param from_x: from currency label
    :param to_x: to currency label
    :param amount: amount to convert
    :return: converted amount
    """

    url = 'http://api.fixer.io/latest'
    try:
        response = requests.get(url)
        if response.status_code != 200:
            return {
                'API Access Error': 'api.fixer.io get request returned with status: {}'.format(response.status_code)
            }
        else:
            fr = response.json()['rates'][from_x.upper()]
            to = response.json()['rates'][to_x.upper()]
            result = float(to) / float(fr) * float(amount)
            from_key = 'from {} {} at {} per EUR'.format(amount, from_x.upper(), fr)
            return {
                from_key: 'to {} at {} per EUR'.format(to_x.upper(), to),
                'result': '{} {}'.format(float("{0:.2f}".format(result)), to_x.upper())
            }
    except requests.ConnectionError as err:
        raise BadRequestError('Public APIs Connection Error > {}'.format(err))


@app.route('/objects/{key}', methods=['GET', 'PUT'])
def dobjects(key):
    """This endpoint adds and retrieves objects from the dictionary OBJ.

    :param key: value of the key in dictionary
    :return: if PUT method then status: OK, if GET method, then object for given key.
    """
    request = app.current_request
    if request.method == 'PUT':
        OBJ[key] = request.json_body
        return {'status': 'OK'}

    elif request.method == 'GET':
        try:
            return {key: OBJ[key]}
        except KeyError:
            raise NotFoundError(key)
