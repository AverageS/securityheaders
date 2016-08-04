import urllib.request
import re
import logging

SECURITY_HEADER_NAMES = ['content-security-policy','strict-transport-security','public-key-pins','x-xss-protection',
                         'x-content-type-options','x-frame-options']

SERVER_NAMES = ['Microsoft-IIS', 'nginx', 'apache']

X_XSS_REGEX = re.compile('^1;(\s?(mode=block)|(report=.*))$')

HTTP_REGEX = re.compile('^http(s)?://.*$')

#TODO УЛучшить систему оценки, добавить Try\except
def check_X_XSS_header(header_data):
    grade_diff = 0
    if X_XSS_REGEX.match(header_data):
        ans = 'X-XSS-Protection is properly configured'
    else:
        ans = 'X-XSS-Protection is misconfigured'
        grade_diff -= 10
    return ans, grade_diff

def checkServer(header_data):
    if header_data in SERVER_NAMES:
        return 'Server is probably disclosing information about itself', -10
    return 'Server has probably changed its name', 0

CHECKING_FUNCTIONS = {
    'x-xss-protection': check_X_XSS_header,
    'server': checkServer,
}

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

def getHeaders(url):
    if not HTTP_REGEX.match(url):
        url = 'http://' + url
    try:
        req =  urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        data = urllib.request.urlopen(req)
    except:
        return None
    else:
        header_names = [header.lower() for header in data.headers]
        headers_dict = {}
        grade = 100
        for header in SECURITY_HEADER_NAMES:
            if not header in header_names:
                headers_dict[header] = 'MISSING'
            else:
                headers_dict[header] = data.getheader(header)
        if 'server' in header_names:
            if data.getheader('Server') in SERVER_NAMES:
                headers_dict['server'] = data.getheader('Server')
                grade -= 10
        logging.info(' '.join([url, 'headers collected']))
        return headers_dict

if __name__ == '__main__':
    t = getHeaders('gosuslugi.ru')
    print(checkHeaders(t))