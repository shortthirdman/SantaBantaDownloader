import os, logging, shutil, base64
from boxsdk import JWTAuth, Client
from boxsdk.object.folder import Folder
from boxsdk.exception import BoxOAuthException, BoxException

logging.basicConfig(level=logging.DEBUG)
logging.getLogger().setLevel(logging.DEBUG)

CLIENT_ID = 'olw7s02jud3fez911erigdt410blyi1s'
CLIENT_SECRET = 'BBYlsrI0qFvmom6kPu4nL6Bc8BE2SWLv'
BOX_USER_ID = '13840317060'
BOX_ENTERPRISE_ID = '683350295'

def decode_string(base64_message):
    """ Decode Byte64 meesage """
    base64_bytes = base64_message.encode('ascii')
    message_bytes = base64.b64decode(base64_bytes)
    message = message_bytes.decode('ascii')
    return message

def upload_files(file_paths, dir_name):
    """ TODO """
    config = JWTAuth.from_settings_file('static/secrets/config.json')

    try:
        client = Client(config)
        content = Folder(client.folder('0'))
        user = client.user().get()
        print(content)
        print(content.get_items())
        print('The current user ID is {0}'.format(user.id))
    except (BoxOAuthException, BoxException) as e:
        # logging.warn()
        raise e
