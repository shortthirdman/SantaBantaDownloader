""" TODO """
import os, urllib.parse, requests, ftplib, logging
from flask import Flask, request, send_file, jsonify, render_template
import downloader

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
logger = logging.getLogger()

app = Flask(__name__)

ftp_port = os.environ.get('BOX_FTP_PORT')
ftp_server = os.environ.get('BOX_FTP_SERVER')
ftp_username = os.environ.get('BOX_FTP_USERNAME')
ftp_password = os.environ.get('BOX_FTP_PASSWORD')

def post_to_ftp(local_dir_name):
    """ Upload directory to Box Drive using FTP """
    remote_dir_name = local_dir_name
    try:
        with ftplib.FTP(ftp_server) as ftps:
            ftps.port = ftp_port
            ftps.login(user=ftp_username, passwd=ftp_password)

            ftps.cwd('Wallpapers')
            dir_path = ''

            if remote_dir_name not in ftps.nlst():
                dir_path = ftps.mkd(remote_dir_name)
                logger.info("Directory created successfully at {0}.".format(dir_path))
            else:
                logger.info("Directory already exists.")

            ftps.cwd(remote_dir_name)
            logger.info("Current directory location: {0}".format(ftps.pwd()))

            file_paths = downloader.utility.get_all_file_paths(local_dir_name)

            for afile in file_paths:
                temp_contents = str(afile).rsplit(os.path.sep)
                temp_file = temp_contents[1]
                with open(afile, 'rb') as fr:
                    ftps.storbinary('STOR ' + temp_file, fr)
                    logger.info("{0} uploaded to remote directory.".format(temp_file))
        ftps.quit()
        result_status = "All files for {0} were uploaded successfully.".format(local_dir_name)
    except (ftplib.error_reply, ftplib.error_temp, ftplib.error_perm) as e:
        logger.exception(str(e))
        result_status = str(e)

    return result_status

def downloader(file_url):
    """ Process bulk download """
    file_url = str(file_url)
    dir_name = urllib.parse.unquote(file_url.split('/')[5])

    try:
        if not os.path.exists(dir_name):
            os.mkdir(dir_name)

        file_num = downloader.utility.extract_file_number(downloader.utility.get_file_name(file_url))
        for i in range(int(file_num), -1, -1):
            web_url = file_url[0:(file_url.rindex('-') + 1)] + str(i) + 'a.jpg'

            if not downloader.utility.check_file(web_url):
                web_url = file_url[0:(file_url.rindex('-') + 1)] + str(i) + 'v.jpg'

            file_object = requests.get(web_url, allow_redirects=True)
            download_location = os.path.sep.join([os.getcwd(), dir_name, get_file_name(web_url)])

            with open(download_location, 'wb') as image:
                image.write(file_object.content)

        file_paths = downloader.utility.get_all_file_paths(dir_name)
        task_status = post_to_ftp(dir_name)
    except (Exception) as ex:
        task_status = "Some error occurred. Please try again after sometime."
        logger.error(ex)
    return task_status

@app.route('/')
def home():
    """Landing page."""
    return render_template('home.html', title="SantaBanta Bulk Downloader")

@app.route('/process', methods=['GET'])
def process_images():
    """ TODO """
    result = downloader(request.args.get('img_url'))
    return render_template('home.html', title="SantaBanta Bulk Downloader", message=result)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=False, ssl_context='adhoc')
