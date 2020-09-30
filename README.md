# SantaBanta Bulk Downloader

![GitHub issues](https://img.shields.io/github/issues/shortthirdman/SantaBantaDownloader)
![GitHub](https://img.shields.io/github/license/shortthirdman/SantaBantaDownloader)
![GitHub Pipenv locked Python version](https://img.shields.io/github/pipenv/locked/python-version/shortthirdman/SantaBantaDownloader)
![CodeFactor Grade](https://img.shields.io/codefactor/grade/github/shortthirdman/SantaBantaDownloader)

## Prerequisites

 * Python 3.8

## Installation

```shell
pip install -r requirements.txt --no-cache-dir

pylint -f colorized <file-name>.py --disable=W

python -B main.py
```

```powershell
[Environment]::SetEnvironmentVariable("PYTHONDONTWRITEBYTECODE", "1", "Machine")

$env:FLASK_APP = "main"

$env:FLASK_ENV = "development"

$env:EXPLAIN_TEMPLATE_LOADING = $True

$env:TEMPLATES_AUTO_RELOAD = $True

$env:APPLICATION_ROOT = ""

flask run
```

## Resources

* [Working with zip files in Python](https://www.geeksforgeeks.org/working-zip-files-python/)

* [REST API](https://santabanta-extractor.herokuapp.com/)

* [Heroku Git](https://git.heroku.com/santabanta-extractor.git)

* [Compress and Decompress Files](https://www.thepythoncode.com/article/compress-decompress-files-tarfile-python)

* [Python gzip.GzipFile() Examples](https://www.programcreek.com/python/example/252/gzip.GzipFile)

* [Rendering Pages in Flask Using Jinja](https://hackersandslackers.com/flask-jinja-templates/)

* [Flask - Templates](https://flask.palletsprojects.com/en/1.1.x/tutorial/templates/)

* [Serving HTML files | Learning Flask Ep. 3](https://pythonise.com/series/learning-flask/rendering-html-files-with-flask)

* [Encoding and Decoding Base64 Strings in Python](https://stackabuse.com/encoding-and-decoding-base64-strings-in-python/)

* [Kloudless Python SDK](https://github.com/Kloudless/kloudless-python)

* [The Kloudless API](https://developers.kloudless.com/docs/latest/core)
