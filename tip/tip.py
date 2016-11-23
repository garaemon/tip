#!/usr/bin/env python

import argparse
import logging
import os
import shutil
import sys

import coloredlogs


def build_parser():
    'return ArgumentParser instance'
    parser = argparse.ArgumentParser(description='Show tips')
    parser.add_argument('-d', '--debug', action='store_true', help='Show debug messages')
    parser.add_argument('--files', action='store_true',
                        help='Print files instead of their contents')
    return parser


def get_resource_directories():
    'return list of directories to read tips markdown files'
    current_directory = os.path.dirname(__file__)
    default_directory = os.path.join(current_directory, '..', 'resources')
    # remove directories which do not exist
    return [d for d in [default_directory]
            if os.path.exists(d)]


def get_tips_files_from_directories(resource_dirs):
    'return list of markdown files in specified directories'
    tip_files = []
    for dir in resource_dirs:
        for root, dirs, files in os.walk(dir):
            for file in files:
                # check if suffix of file has '.md'
                if file.endswith('.md'):
                    tip_files.append(os.path.join(root, file))
    return tip_files


def show_file_contents(tip_file):
    with open(tip_file) as f:
        # print contents of the file
        shutil.copyfileobj(f, sys.stdout)


def main():
    'main function for tip command'
    parser = build_parser()
    args = parser.parse_args()
    # Initialize log setting
    if args.debug:
        loglevel = logging.DEBUG
    else:
        loglevel = logging.WARN
    field_styles = coloredlogs.DEFAULT_FIELD_STYLES
    field_styles['levelname'] = {'color': 'white', 'bold': True}
    coloredlogs.install(level=loglevel,
                        fmt='%(asctime)s [%(levelname)s] %(message)s',
                        field_styles=field_styles)
    resource_dirs = get_resource_directories()
    tips_files = get_tips_files_from_directories(resource_dirs)
    if len(tips_files) == 0:
        logging.error('Cannot find any tips file')
        sys.exit(1)
    if args.files:
        for tips_file in tips_files:
            print(tips_file)
    else:
        for tips_file in tips_files:
            show_file_contents(tips_file)


if __name__ == '__main__':
    main()
