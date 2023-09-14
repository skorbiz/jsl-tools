import argparse


def pipes(args):
    import subprocess
    import os
    
    opts = ["-p", "10"]
    if args.args:
        opts = args.args[1::] 

    cmd = os.path.expanduser("~/Apps/pipes.sh/pipes.sh")
    subprocess.run([cmd]+opts) 

def spinner(args):
    import itertools
    import time
    # Lots of cool spinners in libraries: 
    moon = itertools.cycle(["🌑", "🌒", "🌓", "🌔", "🌕", "🌖", "🌗", "🌘"])
    dots = itertools.cycle(["⠋","⠙","⠹","⠸","⠼","⠴","⠦","⠧","⠇","⠏"])
    ball = itertools.cycle(["( ●    )", "(  ●   )", "(   ●  )", "(    ● )", "(     ●)", "(    ● )", "(   ●  )", "(  ●   )", "( ●    )", "(●     )"])
    colors = itertools.cycle(['\033[0m', '\033[31m', '\033[32m', '\033[33m', '\033[34m', '\033[35m', '\033[36m', '\033[93m', '\033[95m'])

    try:
        while True:
            print(next(colors), end = "\r")
            for i in range(1, 10): 
                print(" ", next(moon), " ", next(dots), " ", next(ball), " Ctrl+c to quit", end="\r")
                time.sleep(.1)
    except KeyboardInterrupt:
        pass


def draw_menu(stdscr):
    # Curses example from:
    # https://gist.github.com/claymcleod/b670285f334acd56ad1c

    import curses
    import sys,os
    k = 0
    cursor_x = 0
    cursor_y = 0

    # Clear and refresh the screen for a blank canvas
    # stdscr.clear()
    # stdscr.refresh()

    # Start colors in curses
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)

    # Makes getch() none blocking
    # curses.halfdelay(1)


    # Loop where k is the last character pressed
    while (k != ord('q')):

        # Initialization
        stdscr.clear()
        height, width = stdscr.getmaxyx()

        if k == curses.KEY_DOWN:
            cursor_y = cursor_y + 1
        elif k == curses.KEY_UP:
            cursor_y = cursor_y - 1
        elif k == curses.KEY_RIGHT:
            cursor_x = cursor_x + 1
        elif k == curses.KEY_LEFT:
            cursor_x = cursor_x - 1

        cursor_x = max(0, cursor_x)
        cursor_x = min(width-1, cursor_x)

        cursor_y = max(0, cursor_y)
        cursor_y = min(height-1, cursor_y)

        # Declaration of strings
        title = "Curses example"[:width-1]
        subtitle = "Written by Clay McLeod"[:width-1]
        keystr = "Last key pressed: {}".format(k)[:width-1]
        statusbarstr = "Press 'q' to exit | STATUS BAR | Pos: {}, {}".format(cursor_x, cursor_y)
        if k == 0:
            keystr = "No key press detected..."[:width-1]

        # Centering calculations
        start_x_title = int((width // 2) - (len(title) // 2) - len(title) % 2)
        start_x_subtitle = int((width // 2) - (len(subtitle) // 2) - len(subtitle) % 2)
        start_x_keystr = int((width // 2) - (len(keystr) // 2) - len(keystr) % 2)
        start_y = int((height // 2) - 2)

        # Rendering some text
        whstr = "Width: {}, Height: {}".format(width, height)
        stdscr.addstr(0, 0, whstr, curses.color_pair(1))

        # Render status bar
        stdscr.attron(curses.color_pair(3))
        stdscr.addstr(height-1, 0, statusbarstr)
        stdscr.addstr(height-1, len(statusbarstr), " " * (width - len(statusbarstr) - 1))
        stdscr.attroff(curses.color_pair(3))

        # Turning on attributes for title
        stdscr.attron(curses.color_pair(2))
        stdscr.attron(curses.A_BOLD)

        # Rendering title
        stdscr.addstr(start_y, start_x_title, title)

        # Turning off attributes for title
        stdscr.attroff(curses.color_pair(2))
        stdscr.attroff(curses.A_BOLD)

        # Print rest of text
        stdscr.addstr(start_y + 1, start_x_subtitle, subtitle)
        stdscr.addstr(start_y + 3, (width // 2) - 2, '-' * 4)
        stdscr.addstr(start_y + 5, start_x_keystr, keystr)
        stdscr.move(cursor_y, cursor_x)


        # Refresh the screen
        stdscr.refresh()

        # Wait for next input
        k = stdscr.getch()

def curses(args):
    import curses
    curses.wrapper(draw_menu)



def add_parsers(parser):
    log_parser = parser.add_parser('terminal-animations', help='Various terminal animations', formatter_class=argparse.RawTextHelpFormatter)
    log_parser.set_defaults(func=lambda x: log_parser.print_help())
    sub_build_parser = log_parser.add_subparsers()

    pipes_parser = sub_build_parser.add_parser('pipes')
    pipes_parser.add_argument('args', nargs=argparse.REMAINDER, help= "Parse args directly to script using --, e.g. -- -p1 -t9")
    pipes_parser.set_defaults(func=pipes)

    spinner_parser = sub_build_parser.add_parser('spinner')
    spinner_parser.set_defaults(func=spinner)

    curses_parser = sub_build_parser.add_parser('curses')
    curses_parser.set_defaults(func=curses)
