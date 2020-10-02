import os, logging, json
from kloudless import Account, verify_token, exceptions

logging.basicConfig(level=logging.INFO,format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',datefmt='%d-%b-%y %H:%M:%S')
logger = logging.getLogger()

class KloudlessAPI():
    def __init__(self, bearer_token=None, account=None):
        if bearer_token is not None:
            self.bearer_token = bearer_token
        else:
            self.account = account

    def verify_bearer_token(self, bearer_token, app_id):
        """ Verify Kloudless API Bearer Token """
        try:
            token_info = verify_token(app_id, bearer_token)
        except exceptions.TokenVerificationFailed:
            logger.exception("Token:{} does not belong to App:{}".format(bearer_token, app_id))
            return False
        except exceptions.APIException as e:
            # if other API request errors happened
            logger.exception(e.message)
            return False
        else:
            logger.info(token_info)
            return True

    def retrieve_folder(self, account):
        """ Retrieve root folder contents """
        root_folder_contents = account.get('storage/folders/root/contents')
        for resource in root_folder_contents.get_paging_iterator():
            logger.info(resource.data)
            logger.info()

    def download_files(self, root_folder_contents):
        """ Download the file in folder """
        for resource in root_folder_contents:
            if resource.data['type'] == 'file':
                filename = resource.data['name']
                response = resource.get('contents')
                with open(filename, 'wb') as f:
                    f.write(response.content)
                break

    def upload_files(self, file_paths, dir_name):
        """ Upload a file to folder """
        for fp in file_paths:
            pass
            file_name = 'FILE_NAME_TO_UPLOAD'
            headers = {
                'X-Kloudless-Metadata': json.dumps(
                    {'parent_id': 'root', 'name': file_name}
                )
            }
            with open(file_name, 'rb') as f:
                file_resource = account.post('storage/files', data=f, headers=headers)

    def retrieve_calendar(self, account):
        """ Retrieve primary calendar """
        calendar = account.get('cal/calendars/primary')
        print('Primary Calendar: {}'.format(calendar.data['name']))
        return calendar.data

if __name__ == "__main__":
    app_id = os.environ.get('KLOUDLESS_APP_ID')
    bearer_token = os.environ.get('KLOUDLESS_BEARER_TOKEN')
    client = KloudlessAPI()
    verified = client.verify_bearer_token(bearer_token, app_id)
    if verified == True:
        account = Account(token=bearer_token)
        # account.headers['X-Kloudless-Raw-Data'] = 'true'
        client.retrieve_folder(account)
