"For implementing server, I have used Python with Flask"

import re
from collections import Counter
import hashlib
from flask import Flask, request, jsonify


app = Flask(__name__)
file_store = {}


@app.route('/store/add', methods=['POST'])
def add_file():
    "Add files to the store."
    files = request.files.getlist('files')

    for file in files:
        filename = file.filename
        file_hash = calculate_file_hash(file)

        if filename in file_store and file_hash == file_store[filename]['hash']:
            continue

        file_data = {
            'content': file.read(),
            'hash': file_hash
        }

        file_store[filename] = file_data

    return jsonify({'message': 'Files added successfully.'}), 200


def calculate_file_hash(file):
    hasher = hashlib.md5()

    while True:
        chunk = file.read(4096)
        if not chunk:
            break
        hasher.update(chunk)

    file.seek(0)  # Reset file pointer to the beginning
    return hasher.hexdigest()


@app.route('/store/ls', methods=['GET'])
def list_files():
    "List files in the store."
    return jsonify({'files': list(file_store.keys())}), 200


@app.route('/store/rm', methods=['DELETE'])
def remove_file():
    "Remove a file."
    filename = request.args.get('filename')

    if filename not in file_store:
        return jsonify({'message': f'File {filename} does not exist in the store.'}), 400

    del file_store[filename]
    return jsonify({'message': f'File {filename} removed successfully.'}), 200


@app.route('/store/update', methods=['PUT'])
def update_file():
    "Update contents of a file in the store."
    filename = request.args.get('filename')
    file = request.files['file']

    if filename not in file_store:
        return jsonify({'message': f'File {filename} does not exist in the store.'}), 400

    file_store[filename] = file.read()
    return jsonify({'message': f'File {filename} updated successfully.'}), 200


@app.route('/store/wc', methods=['GET'])
def word_count():
    "Returns the number of words in all the files stored in server"
    total_words = 0

    for file_data in file_store.values():
        content = file_data['content'].decode('utf-8')
        words = re.findall(r'\w+', content)
        total_words += len(words)

    return jsonify({'word_count': total_words}), 200


@app.route('/store/freq-words', methods=['GET'])
def frequent_words():
    "Returns the 10 most frequent words in all the files combined."
    limit = int(request.args.get('limit', 10))
    order = request.args.get('order', 'dsc')

    word_counter = Counter()

    for file_data in file_store.values():
        content = file_data['content'].decode('utf-8')
        words = re.findall(r'\w+', content)
        word_counter.update(words)

    sorted_words = sorted(word_counter.items(), key=lambda x: x[1], reverse=(order == 'dsc'))
    frequent_words = [{'word': word, 'count': count} for word, count in sorted_words[:limit]]

    return jsonify({'frequent_words': frequent_words}), 200


if __name__ == '__main__':
    app.run()
