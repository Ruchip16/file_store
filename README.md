# Backend File Store Service 

To implement the backend file store service that has a simple HTTP server and a command line client that stores plain-text files and the server would receive requests from clients to store,update, delete files & perform operations on files stored in the server. For the server, I used Python with Flask, and for the command line client, I used Python. Let's get started!

- For setting up the server:
  - Installed Flask using pip: `pip install flask`
  - Created the `server.py` file that sets up a basic Flask server with endpoints for adding files, listing files, removing files, and updating files. The files are stored in a dictionary called file_store, where the keys are the filenames and the values are the file contents.
- For command line client: 
  - Created a `client.py` file which uses the requests library to send HTTP requests to the server. It provides functions for adding files, listing files, removing files, and updating files based on the command-line arguments provided.
 
 ## To Run the code:

**Note: both the server and the client should be running simultaneously for the commands to work correctly.**

- Fork and clone the repository
- to start the server: `python server.py`
- to start the client: `python client.py <command> <arguments>`
  - where command represents - `add, ls, rm, update, wc, freq-words`
  - arguments -`(name of text files you want to store) eg:file1.txt,etc`

## The list of operations the file store supports are: 

1. Add files to the store: `python client.py add file1.txt file2.txt`
2. List files in the store: `python client.py ls`
3. Remove a file: `python client.py rm file1.txt`
4. Update contents of a file in the store: `python client.py update file.txt`
5. Word count: returns the number of words in all the files stored in server 
`python client.py wc`
6. Least or most frequent words: should return the 10 most frequent words in all the files combined.
