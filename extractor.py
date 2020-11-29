import getopt
import os
import sys
import shutil
import sqlite3
import pygtrie as trie


BACKUP_LOCATION = ''


class File(object):
    def __init__(self, name, fhash=None):
        self.name = name
        self.hash = fhash


class Directory(File):
    def __init__(self, name, children):
        super(Directory, self).__init__(name)
        self.c = []
        for child in children:
            self.c.append(child)


def open_db(sqlite_db):
    conn = sqlite3.connect(sqlite_db)
    c = conn.cursor()
    return c


def traverse_callback(path_conv, path, children, is_file=None):
    if is_file is not None and get_loc_actual_blob(is_file) is not None:
        return File(path[-1], is_file)

    children = filter(None, children)
    return Directory(path[-1] if path else '', children)


def get_loc_actual_blob(fhash):
    global BACKUP_LOCATION

    dirs = os.listdir(BACKUP_LOCATION)
    dirs.append(fhash)
    dirs = sorted(dirs)

    f = os.path.join(os.path.join(BACKUP_LOCATION, dirs[dirs.index(fhash) - 1]), fhash)

    if not os.path.isfile(f):
        return None
    else:
        return f


def extract(root, dest):
    for child in root.c:
        name = os.path.join(dest, child.name)

        if isinstance(child, Directory):
            if not os.path.isdir(name):
                print('[i] making directory {0}'.format(name))
                os.makedirs(name)

            extract(child, name)
        else:
            loc = get_loc_actual_blob(child.hash)

            if loc is not None:
                print('[i] found "{0}" at {1}'.format(name, loc))
                shutil.copyfile(loc, name)
            else:
                print('[!] not found: {0}, skipping domain metadata'.format(child.hash))


def main(src, dest):
    global BACKUP_LOCATION

    BACKUP_LOCATION = src
        #'/Users/sokdak/Desktop/36d85d8d2fc0f05b527678702b7f7f1a3ee1a614'
    # dest = '/Users/sokdak/Desktop/tmp'

    c = open_db(os.path.join(BACKUP_LOCATION, 'Manifest.db'))
    t = trie.StringTrie(separator=os.sep)

    for entry in c.execute('SELECT `relativePath`,`domain`,`fileID` from `Files` ORDER BY `relativePath`'):
        path, domain, file_hash = entry
        t[path] = file_hash

    c.close()
    root = t.traverse(traverse_callback)

    os.makedirs(dest, exist_ok=True)
    extract(root, dest)


def usage():
    print('BackupExtractor (iDevice Backup Extractor) by icslab\n\n'
          'Usage:\n\tpython backupextractor.py -s <backup_location> -d <extract_destination>')


if __name__ == '__main__':
    _src = ''
    _dest = ''

    try:
        opts, args = getopt.getopt(sys.argv[1:], "s:d:h", ["source=", "destination=", "help"])
    except getopt.GetoptError as err:
        print(err)
        sys.exit(-1)

    for o, a in opts:
        if o in ("-s", "--source"):
            _src = a
        elif o in ("-d", "--destination"):
            _dest = a
        elif o in ("-h", "--help"):
            usage()
            sys.exit()
        else:
            usage()
            sys.exit(-1)

    argc = len(sys.argv)
    if argc != 5:
        usage()
        sys.exit(-1)

    _src = os.path.expanduser(_src)
    _dest = os.path.expanduser(_dest)
    main(_src, _dest)
