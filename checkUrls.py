import requests # urllib.request
import re
import logging
import time

SECURITY_HEADER_NAMES = ['content-security-policy','strict-transport-security','public-key-pins','x-xss-protection',
                         'x-content-type-options','x-frame-options']

SERVER_NAMES = ['Microsoft-IIS', 'nginx', 'apache']

X_XSS_REGEX = re.compile('^1;(\s?(mode=block)|(report=.*))$')

X_FRAME_OPTIONS_REGEX = re.compile('^(DENY)|(SAMEORIGIN)|(ALLOW-FROM=.*)$')

X_CONTENT_TYPE_REGEX = re.compile('^nosniff$')

HTTP_REGEX = re.compile('^http(s)?://.*$')

TIMEOUT = 5
#TODO УЛучшить систему оценки, добавить Try\except
def check_X_XSS_header(header_data):
    grade_diff = 0
    if X_XSS_REGEX.match(header_data):
        ans = 'X-XSS-Protection is properly configured'
    else:
        ans = 'X-XSS-Protection is misconfigured'
        grade_diff -= 20
    return ans, grade_diff

def checkServer(header_data):
    if header_data in SERVER_NAMES:
        return 'Server is probably disclosing information about itself', -20
    return 'Server has probably changed its name', 0

def check_x_frame(header_data):
    grade_diff = 0
    if X_FRAME_OPTIONS_REGEX.match(header_data):
        ans = 'X-FRAME-OPTIONS are propely configured'
    else:
        ans = 'X-FRAME-OPTIONS are probably misconfigured'
        grade_diff -= 15
    return ans, grade_diff

def check_x_content_type(header_data):
    grade_diff = 0
    if X_CONTENT_TYPE_REGEX.match(header_data):
        ans = 'X_CONTENT TYPE OPTIONS are properly configured'
    else:
        ans = 'X_CONTENT TYPE OPTIONS are probably misconfigured'
        grade_diff -= 15
    return ans, grade_diff

CHECKING_FUNCTIONS = {
    'x-xss-protection': check_X_XSS_header,
    'server': checkServer,
    'x-frame-options': check_x_frame,
    'x-content-type-options': check_x_content_type,
}

def sleeping_decorator(f):
    def wrapper(url):
        for i in range(5):
            try:
                return f(url)
            except requests.ConnectionError:
                time.sleep(0.25)
            except:
                logging.error('Could not get answer from  ' + url)
                return None
        logging.error('Could not get answer from  ' + url)
    return wrapper

def checkHeaders(headers_dict):
    ans_dict = {}
    grade = 100
    for header_name, header_data in headers_dict.items():
        if header_name in CHECKING_FUNCTIONS.keys():
            ans_dict[header_name], grade_diff = CHECKING_FUNCTIONS[header_name](header_data)
            grade += grade_diff
        elif header_data != 'MISSING' and header_name != 'server':
            ans_dict[header_name] = 'header is presented'
        else:
            ans_dict[header_name] = 'header is missing'
            grade -= 15
    ans_dict['grade'] = grade
    return ans_dict

@sleeping_decorator
def getHeaders(url):
    if not HTTP_REGEX.match(url):
        url = 'http://' + url.rstrip().rstrip('.')
    try:
        data =  requests.get(url, verify=False, timeout=TIMEOUT,
                             headers={'User-Agent': 'Mozilla/5.0'},
                             allow_redirects=True)
    except Exception as e:
        raise e
    else:
        header_names = [header.lower() for header in data.headers]
        headers_dict = {}
        grade = 100
        for header in SECURITY_HEADER_NAMES:
            if not header in header_names:
                headers_dict[header] = 'MISSING'
            else:
                headers_dict[header] = data.headers[header]
        headers_dict['server'] = ''
        if 'server' in header_names:
            if data.headers['Server'] in SERVER_NAMES:
                headers_dict['server'] = data.headers['Server']
                grade -= 10
        logging.debug(' '.join([url, 'headers collected']))
        return headers_dict

if __name__ == '__main__':
    'asdg. '.strip().strip('.')
    t = getHeaders('esnsi.gosuslugi.ru ')
    print(checkHeaders(t))