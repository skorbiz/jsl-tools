import argcomplete
import argparse

from jsl_tools.example.example import add_parsers as add_example_parser
from jsl_tools.terminal_animations.terminal_animations import add_parsers as add_terminal_animation_parser
from jsl_tools.devcontainer.dev import add_parsers as add_dev_parser
from jsl_tools.elastic.elastic import add_parsers as add_elastic_parser

def parsers():
    parser = argparse.ArgumentParser(
        description="""Jla cli tool for whatever"""
    )

    subparsers = parser.add_subparsers(
        help='See the help of individual comands for a more detailed description.')

    add_example_parser(subparsers)
    add_terminal_animation_parser(subparsers)
    add_dev_parser(subparsers)
    add_elastic_parser(subparsers)

    argcomplete.autocomplete(parser)
    return parser


def main():
    parser = parsers()
    args = parser.parse_args()

    if 'func' in args:
        return args.func(args)

    print("""
               ██╗███████╗██╗         ████████╗ ██████╗  ██████╗ ██╗     ███████╗
               ██║██╔════╝██║         ╚══██╔══╝██╔═══██╗██╔═══██╗██║     ██╔════╝
               ██║███████╗██║            ██║   ██║   ██║██║   ██║██║     ███████╗
          ██   ██║╚════██║██║            ██║   ██║   ██║██║   ██║██║     ╚════██║
          ╚█████╔╝███████║███████╗       ██║   ╚██████╔╝╚██████╔╝███████╗███████║
           ╚════╝ ╚══════╝╚══════╝       ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝╚══════╝
                 Welcome to the JSL Tools CLI
          
          """)

    parser.print_usage()

    return 255
