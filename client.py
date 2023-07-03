import requests
import argparse

SERVER_URL = 'http://localhost:5000'


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
    response = requests.get(f'{SERVER_URL}/wc')
    if response.status_code == 200:
        count = response.json()['count']
        print(f"Total word count: {count}")
    else:
        print("Failed to retrieve word count.")


def frequent_words(limit=10, order='dsc'):
    params = {
        'limit': limit,
        'order': order
    }
    response = requests.get(f'{SERVER_URL}/freq-words', params=params)
    if response.status_code == 200:
        words = response.json()['words']
        print(f"Most frequent words (limit: {limit}, order: {order}):")
        for word, count in words:
            print(f"{word}: {count}")
    else:
        print("Failed to retrieve frequent words.")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='store', description='File Store Client')
    parser.add_argument('command', choices=['add', 'ls', 'rm', 'update', 'wc', 'freq-words'], help='Command to execute')
    parser.add_argument('arguments', nargs='*', help='Arguments for the command')
    subparsers = parser.add_subparsers(dest='command')
    parser_wc = subparsers.add_parser('wc', help='Word count')
    parser_wc.set_defaults(func=word_count)
    parser_freq_words = subparsers.add_parser('freq-words', help='Frequent words')
    parser_freq_words.add_argument('--limit', '-n', type=int, default=10, help='Limit number of words')
    parser_freq_words.add_argument('--order', choices=['asc', 'dsc'], default='dsc', help='Word order')
    parser_freq_words.set_defaults(func=frequent_words)
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
    elif hasattr(args, 'func'):
        args.func()
    else:
        parser.print_help()
