""" TODO """
import os
import tarfile
import requests
from tqdm import tqdm

def check_file(web_url):
    """ Check if file path exists """
    res = requests.head(web_url)
    if res.headers is None:
        return False
    return True

def extract_file_number(file_name):
    """ Extract the file number from a file name """
    file_name = str(file_name)
    dot_contents = file_name.split('.')
    hyp_contents = dot_contents[0].split('-')
    base_name = hyp_contents[len(hyp_contents) - 1]
    return int(base_name[:-1])

def get_all_file_paths(directory):
    """ Get all file paths from a directory """
    # initializing empty file paths list
    file_paths = []

    # crawling through directory and subdirectories
    for root, files in os.walk(directory):
        for filename in files:
            # join the two strings in order to form the full filepath.
            filepath = os.path.join(root, filename)
            file_paths.append(filepath)

    # returning all file paths
    return file_paths

def compress(tar_file, members):
    """
    Adds files (`members`) to a tar_file and compress it
    """
    # open file for gzip compressed writing
    tar = tarfile.open(tar_file, mode="w:gz")
    # with progress bar
    # set the progress bar
    progress = tqdm(members)
    for member in progress:
        # add file/folder/link to the tar file (compress)
        tar.add(member)
        # set the progress description of the progress bar
        progress.set_description(f"Compressing {member}")
    # close the file
    tar.close()

def decompress(tar_file, path, members=None):
    """
    Extracts `tar_file` and puts the `members` to `path`.
    If members is None, all members on `tar_file` will be extracted.
    """
    tar = tarfile.open(tar_file, mode="r:gz")
    if members is None:
        members = tar.getmembers()
    # with progress bar
    # set the progress bar
    progress = tqdm(members)
    for member in progress:
        tar.extract(member, path=path)
        # set the progress description of the progress bar
        progress.set_description(f"Extracting {member.name}")
    # or use this
    # tar.extractall(members=members, path=path)
    # close the file
    tar.close()

def get_file_name(file_url):
    """ Extracts file name from the file path url """
    file_name = None
    if file_url.find('/'):
        file_name = file_url.rsplit('/', 1)[1]
    return file_name
