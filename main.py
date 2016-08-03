import urllib.request
import re

SECURITY_HEADER_NAMES = ['content-security-policy','strict-transport-security','public-key-pins','x-xss-protection',
                         'x-content-type-options','x-frame-options']

SERVER_NAMES = ['Microsoft-IIS', 'nginx', 'apache']

X_XSS_REGEX = re.compile('^1;(\s?(mode=block)|(report=.*))$')

def check_X_XSS_header(data):
    header_data = data.getheader('X-Xss-Protection')
    if X_XSS_REGEX.match(header_data):
        return 'X-XSS-Protection is properly configured'
    return 'X-XSS-Protection is misconfigured'

CHECKING_FUNCTIONS = {
    'x-xss-protection': check_X_XSS_header,
}

def check_header(data, header_name):
    if header_name in CHECKING_FUNCTIONS.keys():
        return CHECKING_FUNCTIONS[header_name](data)
    return 'Header is presented'

def getHeadersAndCheck(url):
    req =  urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    data = urllib.request.urlopen(req)
    header_names = [header.lower() for header in data.headers]
    result_dict = {}
    for header in SECURITY_HEADER_NAMES:
        if not header in header_names:
            result_dict[header] = 'MISSING'
        else:
            result_dict[header] = check_header(data, header)
    result_dict['server'] = 'Server signature is missing'
    if 'Server' in header_names:
        if data.getheader('Server') in SERVER_NAMES:
            result_dict['server'] = 'Server signature presents'
    return result_dict


if __name__ == '__main__':
    print(getHeadersAndCheck('https://github.com/'))