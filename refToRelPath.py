#!/usr/bin/env python3

import argparse, glob, os, re, sys

def pathtorelative(basePath,absPath):
    if(os.path.isfile(absPath)):
        return '\"'+os.path.relpath(absPath,basePath)+'\"'
    return '\"'+absPath+'\"'

def main(args):
    """ Main entry point of the app """
    
    _path = ""
    _files = []

    # Validate path argument

    if(args.path != None):
        if(not (os.path.exists(args.path) and os.path.isdir(args.path))):
            raise ValueError("Invalid path")
        _path = os.path.normpath(args.path)
    else:
        _path = os.curdir

    # Validate files

    if (args.file != None):
        for f in args.file:
            # Verify file existence and correct extensions
            if( not os.path.exists(f)):
                raise ValueError("File does not exist.")
            if( not os.path.isfile(f)):
                raise ValueError("Supplied path is not a file")
            if( not os.path.splitext(f)[1] != ".ma"):
                raise ValueError("File must be a Maya ASCII file.")
            _files.append(os.path.normpath(f))
    else:
        _files = glob.glob(os.path.join(_path,"**/*.ma"), recursive=True)

    print("Files: "+str(_files))

    for fp in _files:
        bak = os.path.splitext(fp)[0]+"ma.bak"
        os.rename(fp, bak)
        newFile = open(fp, 'w')
        with open(bak, 'r') as f:
            for line in f:
                if line.startswith("file "):
                    newFile.write(re.sub(r'\"([^\"]*)\"', lambda x: pathtorelative(_path,x[1]),line))
                else:
                    newFile.write(line)
                
        os.remove(bak)

    return

if sys.version_info[0] < 3:
    print("This script requires Python 3 or greater")
    sys.exit(1)

if __name__ == "__main__":
    """ This is executed when run from the command line """
    parser = argparse.ArgumentParser()

    parser.add_argument("-f", "--file", action="append")

    # Optional argument which requires a parameter (eg. -d test)
    parser.add_argument("-p", "--path", action="store")

    args = parser.parse_args()
    main(args)