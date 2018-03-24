#!/usr/bin/env python3

import argparse
import os


def main(args):
    """ Main entry point of the app """
    pass


if __name__ == "__main__":
    """ This is executed when run from the command line """
    parser = argparse.ArgumentParser()

    parser.add_argument("-f", "--file", action="append")

    # Optional argument which requires a parameter (eg. -d test)
    parser.add_argument("-p", "--path", action="store")

    args = parser.parse_args()
    main(args)