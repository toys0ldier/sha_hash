#!/usr/bin/python3

import os, hashlib, sys

def progress(fileName, completeNum):
    printWidth = (os.get_terminal_size().columns - 25)
    if len(fileName) < printWidth:
        for _ in range(0, (printWidth - len(fileName))):
            fileName += ' '
    elif len(fileName) > printWidth:
        fileName = '...' + fileName[-(printWidth - 3):]
    else:
        pass
    print("%s [ Progress: %s ] " % (fileName.encode('utf-8', 'ignore').decode('utf-8'), '{:,}'.format(completeNum)), end='\r')

def scanTree(path):
    try:
        for entry in os.scandir(path):
            if entry.is_dir(follow_symlinks=False):
                yield from scanTree(entry)
            else:
                yield entry
    except PermissionError:
        pass
            
def main():
    BUF_SIZE = 1073741824 # read in chunks of 1gb
    SHA1 = hashlib.sha1()
    SHA256 = hashlib.sha256()
    for i, entry in enumerate(scanTree(sys.argv[1]), start=1):
        if entry.is_file():
            try:
                with open(entry.path, 'rb') as f:
                    while True:
                        data = f.read(BUF_SIZE)
                        if not data:
                            break
                        SHA1.update(data)
                        SHA256.update(data)
            except PermissionError:
                pass
            progress(entry.name, i)
    print('')
    print('Results for:\t%s' % sys.argv[1])
    print('SHA1:\t\t%s' % SHA1.hexdigest())
    print('SHA256:\t\t%s' % SHA256.hexdigest())

if __name__ == '__main__':
    
    main()