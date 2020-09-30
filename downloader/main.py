""" TODO """
import os
import tarfile
import urllib.parse
from zipfile import ZipFile
from flask import Flask, request, send_file, jsonify, render_template
import requests
from util import check_file, extract_file_number, get_file_name, get_all_file_paths
from pcloud_client import upload_files

app = Flask(__name__)

@app.route('/')
def home():
    """Landing page."""
    return render_template('home.html', title="SantaBanta Bulk Downloader")

@app.route('/process', methods=['GET'])
def process_images():
    """ TODO """
    return downloader(request.args.get('img_url'))

def downloader(file_url):
    """ TODO """
    file_url = str(file_url)
    dir_name = urllib.parse.unquote(file_url.split('/')[5])
    zip_name = '.'.join([dir_name, 'zip'])
    # tar_name = '.'.join([dir_name, 'tar', 'gz'])

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
        result = upload_files(file_paths, dir_name)
        return jsonify(message=result)
    except Exception:
        pass

def archive_directory(dir_name, zip_name):
    """Returns the compressed folder for the `dir_name` in zip format"""
    file_paths = get_all_file_paths(dir_name)
    # create a ZipFile object
    with ZipFile(zip_name, 'w') as z_file:
        # Iterate over all the files in directory
        for file in file_paths:
            z_file.write(file)

def create_tarfile(outfile, dir_name):
    """Returns the compressed folder for the `dir_name` in tar format"""
    file_paths = get_all_file_paths(dir_name)
    try:
        with tarfile.open(outfile, mode="w:gz", compresslevel=9) as tar:
            for infile in file_paths:
                tar.add(infile, arcname=infile.rsplit(os.path.sep, 1)[1])
    except tarfile.CompressionError as c_ex:
        raise c_ex
    except tarfile.TarError as t_ex:
        raise t_ex

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=False, ssl_context='adhoc')
