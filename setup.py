import os

from requests_oauthlib import OAuth1Session

client_key = os.environ['TRIPIT_OAUTH_KEY']
client_secret = os.environ['TRIPIT_OAUTH_SECRET']

request_token_url = 'https://api.tripit.com/oauth/request_token'

oauth = OAuth1Session(client_key, client_secret=client_secret)
fetch_response = oauth.fetch_request_token(request_token_url)

resource_owner_key = fetch_response.get('oauth_token')
resource_owner_secret = fetch_response.get('oauth_token_secret')

base_authorization_url = 'https://www.tripit.com/oauth/authorize'
authorization_url = oauth.authorization_url(base_authorization_url)
print('Please go here and authorize,' + authorization_url)
redirect_response = input('Paste the full redirect URL here: ')
oauth_response = oauth.parse_authorization_response(redirect_response)

access_token_url = 'https://api.tripit.com/oauth/access_token'

oauth = OAuth1Session(client_key,
                      client_secret=client_secret,
                      resource_owner_key=resource_owner_key,
                      resource_owner_secret=resource_owner_secret,
                      verifier='x')

oauth_tokens = oauth.fetch_access_token(access_token_url)
resource_owner_key = oauth_tokens.get('oauth_token')
resource_owner_secret = oauth_tokens.get('oauth_token_secret')

print("key: {}, secret: {}".format(resource_owner_key, resource_owner_secret))

