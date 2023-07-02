import requests
import argparse

BASE_URL = 'http://localhost:5000/store'


def add_files(filenames):
    files = [('files', open(filename, 'rb')) for filename in filenames]
    response = requests.post(f'{BASE_URL}/add', files=files)
    print(response.json())


def list_files():
    response = requests.get(f'{BASE_URL}/ls')
    print(response.json())


def remove_file(filename):
    response = requests.delete(f'{BASE_URL}/rm?filename={filename}')
    print(response.json())


def update_file(filename):
    files = {'file': open(filename, 'rb')}
    response = requests.put(f'{BASE_URL}/update?filename={filename}', files=files)
    print(response.json())


def word_count():
    response = requests.get(f'{BASE_URL}/wc')
    data = response.json()
    print(f"Total word count: {data['word_count']}")


def frequent_words(limit=10, order='dsc'):
    params = {'limit': limit, 'order': order}
    response = requests.get(f'{BASE_URL}/freq-words', params=params)
    data = response.json()
    frequent_words = data['frequent_words']

    print(f"{'Word': <15} {'Count': <10}")
    print("---------------------------")
    for word_data in frequent_words:
        print(f"{word_data['word']: <15} {word_data['count']: <10}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='File Store Command Line Client')
    parser.add_argument('command', choices=['add', 'ls', 'rm', 'update', 'wc', 'freq-words'], help='Command to execute')
    parser.add_argument('arguments', nargs='*', help='Arguments for the command')
    args = parser.parse_args()

    command = args.command

    if command == 'add':
        add_files(args.arguments)
    elif command == 'ls':
        list_files()
    elif command == 'rm':
        remove_file(args.arguments[0])
    elif command == 'update':
        update_file(args.arguments[0])
    elif command == 'wc':
        word_count()
    elif command == 'freq-words':
        frequent_words(*args.arguments)