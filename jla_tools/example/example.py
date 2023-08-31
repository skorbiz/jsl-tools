import argparse


def script_wrapper(args):
    if not args.as_script:
        from .print_chart import print_chart
        print_chart(args.numbers)
    else:
        import os                           # Import inside functions to save type
        path = os.path.split(__file__)[0]   # Do something
        os.system("python3 {}/print_chart.py {}".format(path, " ".join(str(n) for n in args.numbers)))



def MyCompleter(**kwargs):
    return "🌿 🍀 🐌 🐣 🐙 🐢 🐋 🐸 🐧 🐬 🐲 🐀 🐘 🐝 🐥".split()


def add_parsers(parser):
    test_parser = parser.add_parser(
        'test', help="run unittests, integration tests", description=""" This command runs various test related tools
""", formatter_class=argparse.RawTextHelpFormatter)
    test_parser.add_argument('args', nargs=argparse.REMAINDER, help="The following targets are supported [{}]".format(", ".join(get_test_targets()))).completer = MyTestCompleter




def add_parsers(parser):
    example_parser = parser.add_parser('example', help='A helpfull text', formatter_class=argparse.RawTextHelpFormatter)
    example_parser.set_defaults(func=lambda x: example_parser.print_help())
    sub_parser = example_parser.add_subparsers()

    script_parser = sub_parser.add_parser('call_scritp', help="more help text.")
    script_parser.add_argument('-s', '--as_script', action='store_true')
    script_parser.add_argument('numbers', nargs='+', type=int)
    script_parser.set_defaults(func=script_wrapper)

    comp_parser = sub_parser.add_parser('completion', help="text")
    comp_parser.add_argument('args', nargs=argparse.REMAINDER, 
        help="The following tags are supported [{}]".format(", ".join(MyCompleter()))).completer = MyCompleter
    comp_parser.set_defaults(func=print)