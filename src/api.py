from flask import Flask, Response, request
from werkzeug.utils import secure_filename
import json
import subprocess
import os

app = Flask(__name__)

@app.route('/listen/<book_name>')
def sendmp3(book_name):
    with open('library.json') as library_fp:
        library = json.loads(library_fp.read())
    
    if book_name not in library:
        return 'Book name \'{}\' not found in library'.format(book_name)
    with open(library[book_name], 'rb') as mp3:
        data = mp3.read()
        return Response(data, mimetype='audio/mpeg')

@app.route('/convert', methods=['POST'])
def convert():
    print('Converting text to speech')
    file_ptr = request.files['file']

    secure_name = secure_filename(file_ptr.filename)
    book_name = ''.join(secure_name.split('.')[:-1])

    secure_name = 'text/' + secure_name
    new_name = 'media/' + book_name + '.mp3'

    file_ptr.save(secure_name)
    
    if book_name is None or book_name.strip() == '':
        return 'Book name cannot be empty'

    subprocess.Popen(['python3', 'text_converter.py', '--infile', secure_name, '--outfile', new_name])
    
    with open('library.json', 'r') as library_fp:
        library = json.loads(library_fp.read())
    library[book_name] = new_name

    with open('library.json', 'w+') as library_fp:
        library_fp.write(json.dumps(library))

    return 'Book processing, check back in a moment at /listen/{}\n'.format(book_name)

if __name__ == '__main__':
    # Start with a default library if none exists yet
    if not os.path.isfile('library.json'):
        with open('library.json', 'w+') as f:
            f.write('{}')

    # Make sure text and media directories are available for saving
    core_dirs = ['text', 'media']
    for dirname in core_dirs:
        if not os.path.isdir(dirname):
            os.mkdir(dirname)
    
    app.run(host='0.0.0.0')
