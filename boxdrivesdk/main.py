import requests, os, logging
from boxsdk import Client, OAuth2
from boxsdk.network.default_network import DefaultNetwork
from boxsdk.exception import BoxAPIException
from pprint import pformat
from StringIO import StringIO

# Define client ID, client secret, and developer token.
CLIENT_ID = None
CLIENT_SECRET = None
ACCESS_TOKEN = None

class LoggingNetwork(DefaultNetwork):
    def request(self, method, url, access_token, **kwargs):
        """ Base class override. Pretty-prints outgoing requests and incoming responses. """
        print '\x1b[36m{} {} {}\x1b[0m'.format(method, url, pformat(kwargs))
        response = super(LoggingNetwork, self).request(method, url, access_token, **kwargs)
        if response.ok:
            print '\x1b[32m{}\x1b[0m'.format(response.content)
        else:
            print '\x1b[31m{}\n{}\n{}\x1b[0m'.format(response.status_code, response.headers, pformat(response.content),)
        return response

def refresh_access_token(client_id, client_secret, access_token):
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    data = {
      'client_id': client_id,
      'client_secret': client_secret,
      'refresh_token': access_token,
      'grant_type': 'refresh_token'
    }

    response = requests.post('https://api.box.com/oauth2/token', headers=headers, data=data)
    return response

if __name__ == "__main__":
	# Read app info from text file
	with open('app.cfg', 'r') as app_cfg:
		CLIENT_ID = app_cfg.readline()
		CLIENT_SECRET = app_cfg.readline()
		ACCESS_TOKEN = app_cfg.readline()
    
    try:
        # Create OAuth2 object. It's already authenticated, thanks to the developer token.
        oauth2 = OAuth2(CLIENT_ID, CLIENT_SECRET, access_token=ACCESS_TOKEN)

        # Create the authenticated client
        client = Client(oauth2, LoggingNetwork())
        my = client.user(user_id='me').get()
        root_folder = client.folder('0')
        root_folder_with_info = root_folder.get()
    except:
        refresh_access_token(CLIENT_ID, CLIENT_SECRET, ACCESS_TOKEN)
        pass