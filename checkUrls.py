import urllib.request
import re
import logging

SECURITY_HEADER_NAMES = ['content-security-policy','strict-transport-security','public-key-pins','x-xss-protection',
                         'x-content-type-options','x-frame-options']

SERVER_NAMES = ['Microsoft-IIS', 'nginx', 'apache']

X_XSS_REGEX = re.compile('^1;(\s?(mode=block)|(report=.*))$')

HTTP_REGEX = re.compile('^http(s)?://.*$')

#TODO УЛучшить систему оценки, добавить Try\except
def check_X_XSS_header(data):
    header_data = data.getheader('X-Xss-Protection')
    result_dict = {}
    if X_XSS_REGEX.match(header_data):
        result_dict['message'] = 'X-XSS-Protection is properly configured'
        result_dict['grade'] = 0
    else:
        result_dict['message'] = 'X-XSS-Protection is misconfigured'
        result_dict['grade'] = -10
    return result_dict


CHECKING_FUNCTIONS = {
    'x-xss-protection': check_X_XSS_header,
}

def check_header(data, header_name):
    if header_name in CHECKING_FUNCTIONS.keys():
        return CHECKING_FUNCTIONS[header_name](data)
    return {'message': 'Header is presented', 'grade': 0}

def getHeadersAndCheck(url):
    if not HTTP_REGEX.match(url):
        url = 'http://' + url
    req =  urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    data = urllib.request.urlopen(req)
    header_names = [header.lower() for header in data.headers]
    result_dict = {}
    grade = 100
    for header in SECURITY_HEADER_NAMES:
        if not header in header_names:
            result_dict[header] = 'MISSING'
            grade -= 10
        else:
            ans =  check_header(data, header)
            result_dict[header] = ans['message']
            grade += ans['grade']
    result_dict['server'] = 'Server signature is missing'
    if 'server' in header_names:
        if data.getheader('Server') in SERVER_NAMES:
            result_dict['server'] = 'Server signature presents'
            grade -= 10
    logging.info('|'.join([url, 'grade', str(grade)]))
    return result_dict, grade

if __name__ == '__main__':
    print(getHeadersAndCheck('https://gosuslugi.ru/'))