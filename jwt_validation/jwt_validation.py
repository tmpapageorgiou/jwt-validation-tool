#!/usr/bin/env python2

import jwt
import requests
import sys

from cryptography.x509 import load_pem_x509_certificate
from cryptography.hazmat.backends import default_backend


def get_public_key(access_token):
    token_header = jwt.get_unverified_header(access_token)

    res = requests.get('https://login.microsoftonline.com/common/.well-known/openid-configuration')
    jwk_uri = res.json()['jwks_uri']

    res = requests.get(jwk_uri)
    jwk_keys = res.json()

    x5c = None
    # Iterate JWK keys and extract matching x5c chain
    for key in jwk_keys['keys']:
        if key['kid'] == token_header['kid']:
            x5c = key['x5c']
            break
    else:
        raise Exception('Certificate not found in {}'.format(jwk_uri))

    cert = ''.join([
        '-----BEGIN CERTIFICATE-----\n',
        x5c[0],
        '\n-----END CERTIFICATE-----\n',
    ])
    try:
        public_key =  load_pem_x509_certificate(cert.encode(), default_backend()).public_key()
    except Exception as error:
        raise Exception('Failed to load public key:', error)

    return public_key, key['kid']

def main():
    print '\n'
    if len(sys.argv) < 2 or '-h' in sys.argv:
        print 'Run it again passing acces token:\n\tpython jwt_validation.py <access_token>'
        sys.exit(1)

    access_token = sys.argv[1]
    audience = 'https://graph.microsoft.com'

    public_key, kid = get_public_key(access_token)

    try:
        jwt.decode(
            access_token,
            public_key,
            algorithms='RS256',
            audience=audience,
        )
    except Exception as error:
        print 'key {} did not worked, error:'.format(kid), error
        sys.exit(1)

    print('Key worked!')

if __name__ == '__main__':
    main()
