import urllib
import re

SECURITY_HEADER_NAMES = ['Content-Security-Policy','Strict-Transport-Security','Public-Key-Pins','X-Xss-Protection',
                         'X-Content-Type-Options','X-Frame-Options']

SERVER_NAMES = ['Microsoft-IIS', 'nginx', 'apache']


X_XSS_REGEX = re.compile('^1;(\s?(mode=block)|(report=.*))$')

def checkX_XSS_header(data):
    header_data = data.getheader('X-Xss-Protection')
    if X_XSS_REGEX.match(header_data):
        return True
    return False

def getHeaders(url):
    req =  urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    data = urllib.request.urlopen(req)
    header_names = [header for header in data.headers]
    missing_sec_headers = [t for t in SECURITY_HEADER_NAMES if t not in header_names]
    server_signature_present = False
    if 'Server' in header_names:
        if data.getheader('Server') in SERVER_NAMES: #Может, надо добавить data.getheader().lower() ???
            server_signature_present = True
    if 'X-Xss-Protection' not in missing_sec_headers:
        checkX_XSS_header(data)
    return missing_sec_headers, server_signature_present




if __name__ == '__main__':
    print(getHeaders('http://gosuslugi.ru'))
    getHeaders('https://runbox.com/')
