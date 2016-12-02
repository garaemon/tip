#!/usr/bin/env python
# -*- coding: utf-8 -*-

# system libraries
import argparse
import curses
import logging
import os
import re
import shutil
import sys

# 3rdparty libraries
import coloredlogs

HIGHLIGHT_FG_COLOR = curses.COLOR_WHITE
HIGHLIGHT_BG_COLOR = curses.COLOR_MAGENTA


def build_parser():
    'return ArgumentParser instance'
    parser = argparse.ArgumentParser(description='Show tips')
    parser.add_argument('-d', '--debug', action='store_true', help='Show debug messages')
    parser.add_argument('--files', action='store_true',
                        help='Print files instead of their contents')
    parser.add_argument('-i', '--interactive', action='store_true',
                        help='Show tips with interactive search')
    return parser


def get_resource_directories():
    'return list of directories to read tips markdown files'
    current_directory = os.path.dirname(__file__)
    default_directory = os.path.join(current_directory, '..', 'resources')
    user_directory = os.path.expanduser('~/.tips')
    # remove directories which do not exist
    return [d for d in [default_directory, user_directory]
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
    'show contents of tip_file'
    with open(tip_file) as f:
        # print contents of the file
        shutil.copyfileobj(f, sys.stdout)


def addstr_with_highlight(stdscr, line, key_search_regexp, highlight_line):
    'Show a line with highlighting keyword.'
    search_result = key_search_regexp.search(line)
    if highlight_line:
        default_attribute = curses.color_pair(1)
        whitespace_attribute = curses.color_pair(2) | curses.A_UNDERLINE
    else:
        default_attribute = 0
        whitespace_attribute = 0
    if search_result:
        start_pos = 0
        for m in key_search_regexp.finditer(line):
            # m.start -- m.end should be highlighted
            # start_pos -- m.start() -> normal color
            stdscr.addstr(0, start_pos, line[start_pos:m.start()], default_attribute)
            # m.start() -> m.end() -> highlighted
            stdscr.addstr(0, m.start(), line[m.start():m.end()],
                          curses.A_UNDERLINE | curses.A_BOLD | default_attribute)
            # update srtart_pos for next loop
            start_pos = m.end()
        stdscr.addstr(0, start_pos, line[start_pos:], default_attribute)
    else:
        stdscr.addstr(0, 0, line, default_attribute)
    # when highlighting equals to True, add space until the end of the terminal
    if highlight_line:
        (window_y, window_x) = stdscr.getmaxyx()
        if window_x > len(line) + 1:
            # Print '-' with same foreground and background color because
            # curses cannot colorize white spaces.
            stdscr.addstr(0, len(line), ' ' * (window_x - len(line) - 1), whitespace_attribute)


class TextBlock(object):
    'Block of markdown'

    def __init__(self, content, filename, block_index):
        'Constructor of TextBlock retrieves content string'
        self.content = content
        self.filename = filename
        self.index = block_index
        self.matched_index = None
        self.page = None
        self.first_line_pos = None

    def show_with_curses(self, stdscr, keys=[], key_search_regexp=None, highlight=False):
        '''Show content of TextBlock with curses. key_search_regexp is a regular
        expression object to search keywords with OR condition.

        key_search_regexp is a regular expression object to search keywords with OR condition.
        '''
        lines = self.content.split('\n')
        lines.reverse()         # reverse lines
        for line, i in zip(lines, range(len(lines))):
            if i == len(lines) - 1:
                # last line should have '##' as prefix.
                addstr_with_highlight(stdscr, '##' + line, key_search_regexp, highlight)
            else:
                addstr_with_highlight(stdscr, line, key_search_regexp, highlight)
            stdscr.clrtoeol()
            stdscr.insertln()
        # Add separator with file name
        (window_y, window_x) = stdscr.getmaxyx()
        separator_string = '-({})'.format(self.filename) + '-' * (window_x - 1 - len(self.filename))
        # separator_string = '-({}/{} - {})'.format(self.first_line_pos, self.page, self.filename)
        stdscr.addstr(0, 0, separator_string[:window_x - 1])
        stdscr.clrtoeol()
        stdscr.insertln()

    def show(self, keys=[]):
        'Show content to stdout'
        print('##' + self.content)

    def search(self, key_regexp):
        'Return true if content includes any of keys.'
        return key_regexp.search(self.content)

    def get_lines_to_show(self):
        'Return the number of lines to show block'
        # +1 comes from file name
        return len(self.content.split('\n')) + 1


class TextBlockContainer(object):
    'Container of TextBlock class'

    def __init__(self, blocks):
        'blocks is a list of TextBlock instance'
        self.blocks = blocks

    def build_regexp_and_search(self, search_keywords):
        'Build regular expression fod AND search'
        return re.compile(''.join(
            ['(?=.*{})'.format(key) for key in search_keywords]), re.IGNORECASE | re.DOTALL)

    def build_regexp_or_search(self, search_keywords):
        'Build regular expression fod OR search'
        return re.compile('({})'.format('|'.join(search_keywords)),
                          re.IGNORECASE)

    def show_with_curses(self, stdscr, search_string, active_block_index):
        'Show blocks which mach search_string'
        search_keywords = search_string.split()
        search_keywords_and_regexp = self.build_regexp_and_search(search_keywords)
        search_keywords_or_regexp = self.build_regexp_or_search(search_keywords)
        matched_blocks = [block for block in self.blocks
                          if block.search(search_keywords_and_regexp)]
        reversed_active_block_index = len(matched_blocks) - active_block_index - 1
        if reversed_active_block_index < 0:
            reversed_active_block_index = 0
        # compute pages
        (window_y, window_x) = stdscr.getmaxyx()
        needed_lines = [block.get_lines_to_show() for block in matched_blocks]
        # +2 = +1
        first_line_pos = [sum(needed_lines[i + 1:]) + 2 for i in range(len(matched_blocks))]
        for block, i in zip(matched_blocks, range(len(matched_blocks))):
            block.first_line_pos = first_line_pos[i]
            block.page = first_line_pos[i] / window_y
            block.matched_index = i
        active_page = matched_blocks[reversed_active_block_index].page
        active_blocks = [block for block in matched_blocks if block.page == active_page]
        for block in active_blocks:
            block.show_with_curses(stdscr, search_keywords, search_keywords_or_regexp,
                                   block.matched_index == reversed_active_block_index)

    def echo_active_block(self, search_string, active_block_index):
        'Echo content of specified active block without curses'
        search_keywords_and_regexp = self.build_regexp_and_search(search_string.split())
        matched_blocks = [block for block in self.blocks
                          if block.search(search_keywords_and_regexp)]
        if len(matched_blocks) == 0:
            # no matching blocks
            return
        # normalize active_block_index
        reversed_active_block_index = len(matched_blocks) - active_block_index - 1
        if reversed_active_block_index < 0:
            reversed_active_block_index = 0
        matched_blocks[reversed_active_block_index].show()


def display_contents_with_incremental_search(stdscr, search_string, active_block_index,
                                             block_container):
    'Display file contents with incremental searching'
    stdscr.erase()
    # Show results first because `insertln` insert a line upwords.
    # We need to print content in reversed order.
    block_container.show_with_curses(stdscr, search_string, active_block_index)
    # Show prompt.
    stdscr.addstr(0, 0, 'Query: ' + search_string)
    stdscr.clrtoeol()
    stdscr.refresh()


def show_file_contents_with_incremental_search(tips_files):
    'Show file contnts with incremental searching'
    # First read all the contents and separate into few blocks
    blocks = []
    for tips_file in tips_files:
        with open(tips_file) as f:
            # Each markdown file should have second level blocks which start with
            # '##'.
            content_string = f.read()
            blocked_contents_string = content_string.split('##')
            counter = 0
            for blocked_content in blocked_contents_string:
                if len(blocked_content) != 0:
                    # Do not show empty content
                    block = TextBlock(blocked_content, tips_file, counter)
                    blocks.append(block)
                    counter = counter + 1
    block_container = TextBlockContainer(blocks)
    # to debug key input
    # block_container = TextBlockContainer([])
    stdscr = curses.initscr()
    curses.start_color()
    curses.init_pair(1, HIGHLIGHT_FG_COLOR, HIGHLIGHT_BG_COLOR)
    curses.init_pair(2, HIGHLIGHT_BG_COLOR, HIGHLIGHT_BG_COLOR)
    curses.noecho()
    curses.cbreak()             # Do not wait for enter key
    stdscr.keypad(True)
    stdscr.clear()
    try:
        search_string = ''
        active_block_index = 0
        display_contents_with_incremental_search(stdscr, search_string, active_block_index,
                                                 block_container)
        # flag which will be True only if Enter key is pressed.
        finish_normally = False
        while True:
            c = stdscr.getch()
            if c == curses.KEY_ENTER or c == 10 or c == 13:
                # enter key
                finish_normally = True
                # exit from while loop
                break
            elif (c == curses.KEY_BACKSPACE or c == 8 or
                  c == curses.KEY_DL or c == 127):
                # backspace, remove one character from search_string
                search_string = search_string[:-1]
                active_block_index = 0
            elif c == 21:
                # Ctrl-U, clear all the string
                search_string = ""
                active_block_index = 0
            elif c == 14 or c == curses.KEY_DOWN:
                # C-n or down
                active_block_index = active_block_index + 1
            elif c == 16 or c == curses.KEY_UP:
                # C-p or up
                active_block_index = active_block_index - 1
            elif 0 <= c and c < 256:
                # ascii character
                search_string = search_string + chr(c)
                active_block_index = 0
            # chop active_block_index
            if active_block_index < 0:
                active_block_index = 0
            display_contents_with_incremental_search(stdscr, search_string, active_block_index,
                                                     block_container)
            # debug key input
            # stdscr.addstr(0, 0, "current format: {}".format(c))
            # stdscr.clrtoeol()
            # stdscr.insertln()
    finally:
        curses.nocbreak()
        stdscr.keypad(0)
        curses.echo()
        curses.endwin()
    if finish_normally:
        block_container.echo_active_block(search_string, active_block_index)


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
        if args.interactive:
            show_file_contents_with_incremental_search(tips_files)
        else:
            for tips_file in tips_files:
                show_file_contents(tips_file)


if __name__ == '__main__':
    main()
