import os, logging
from kloudless import Account, verify_token, exceptions

logging.basicConfig(level=logging.INFO,format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',datefmt='%d-%b-%y %H:%M:%S')
logger = logging.getLogger()

app_id = os.environ.get('KLOUDLESS_BOX_APP_ID')
bearer_token = os.environ.get('KLOUDLESS_BOX_BEARER_TOKEN')
account = Account(token=bearer_token)
account.headers['X-Kloudless-Raw-Data'] = 'true'

def verify_bearer_token():
    """ """
    try:
        token_info = verify_token(app_id, bearer_token)
    except exceptions.TokenVerificationFailed:
        logger.exception("Token:{} does not belong to App:{}".format(bearer_token, app_id))
    except exceptions.APIException as e:
        # if other API request errors happened
        logger.exception(e.message)
    else:
        logger.info(token_info)

def retrieve_folder():
    """ Retrieve root folder contents """
    root_folder_contents = account.get('storage/folders/root/contents')
    for resource in root_folder_contents.get_paging_iterator():
        print(resource.data)

def download_files(root_folder_contents):
    """ Download the file in folder """
    for resource in root_folder_contents:
        if resource.data['type'] == 'file':
            filename = resource.data['name']
            response = resource.get('contents')
            with open(filename, 'wb') as f:
                f.write(response.content)
            break

def upload_file():
    """ Upload a file to folder """
    file_name = 'FILE_NAME_TO_UPLOAD'
    headers = {
        'X-Kloudless-Metadata': json.dumps(
            {'parent_id': 'root', 'name': file_name}
        )
    }
    with open(file_name, 'rb') as f:
        file_resource = account.post('storage/files', data=f, headers=headers)

def retrieve_calendar():
    """ Retrieve primary calendar """
    calendar = account.get('cal/calendars/primary')
    print('Primary Calendar: {}'.format(calendar.data['name']))
    return calendar.data