""" TODO """
import os, urllib.parse, requests, ftplib, logging, ftputil
from flask import Flask, request, send_file, jsonify, render_template
from downloader.utility import check_file, extract_file_number, get_file_name, get_all_file_paths

logging.basicConfig(level=logging.INFO,format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',datefmt='%d-%b-%y %H:%M:%S')
logger = logging.getLogger()

app = Flask(__name__)

ftp_port = os.environ.get('BOX_FTP_PORT')
ftp_server = os.environ.get('BOX_FTP_SERVER')
ftp_username = os.environ.get('BOX_FTP_USERNAME')
ftp_password = os.environ.get('BOX_FTP_PASSWORD')

def upload_directory(local_dir, ftp_dir):
    file_list = os.listdir(local_dir)
    try:
        with ftputil.FTPHost(ftp_server, ftp_username, ftp_password) as ftp_host:
            for fname in file_list:
                if os.path.isdir(local_dir + fname):             
                    if(ftp_host.path.exists(ftp_dir + fname) != True):                   
                        ftp_host.mkdir(ftp_dir + fname)
                        logger.info("{0}{1} is created.".format(ftp_dir, fname))
                    upload_directory(local_dir + fname + "/", ftp_dir + fname + "/")
                else:               
                    if (ftp_host.upload_if_newer(local_dir + fname, ftp_dir + fname)):
                        logger.info("{0}{1} is uploaded.".format(ftp_dir, fname))
                    else:
                        logger.info("{0}{1} has already been uploaded.".format(local_dir, fname))
    except (Exception, OSError, ftplib.error_reply, ftplib.error_temp, ftplib.error_perm) as e:
        logger.exception(e)

def post_to_ftp(file_paths,dir_name):
    """ Upload directory to Box Drive using FTP """
    try:
        with ftplib.FTP_TLS(ftp_server) as ftps:
            ftps.login(user=ftp_username, passwd=ftp_password)
            ftps.set_debuglevel(1)
            ftps.set_pasv(True)
            ftps.dir()
            logger.info("{0}".format(ftps.getwelcome()))
    except (ftplib.error_reply, ftplib.error_temp, ftplib.error_perm) as e:
        logger.exception(e)

def downloader(file_url):
    """ Process bulk download """
    file_url = str(file_url)
    dir_name = urllib.parse.unquote(file_url.split('/')[5])

    try:
        if not os.path.exists(dir_name):
            os.mkdir(dir_name)

        file_num = extract_file_number(get_file_name(file_url))
        for i in range(int(file_num), -1, -1):
            web_url = file_url[0:(file_url.rindex('-') + 1)] + str(i) + 'a.jpg'

            if not check_file(web_url):
                web_url = file_url[0:(file_url.rindex('-') + 1)] + str(i) + 'v.jpg'

            file_object = requests.get(web_url, allow_redirects=True)
            download_location = os.path.sep.join([os.getcwd(), dir_name, get_file_name(web_url)])

            with open(download_location, 'wb') as image:
                image.write(file_object.content)

        file_paths = get_all_file_paths(dir_name)
        upload_directory(dir_name, dir_name)
        result = "Success"
        return result
    except Exception:
        pass

@app.route('/')
def home():
    """Landing page."""
    return render_template('home.html', title="SantaBanta Bulk Downloader")

@app.route('/process', methods=['GET'])
def process_images():
    """ TODO """
    return downloader(request.args.get('img_url'))

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=False, ssl_context='adhoc')
