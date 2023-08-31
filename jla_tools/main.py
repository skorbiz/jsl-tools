import argcomplete
import argparse

from jla_tools.example.example import add_parsers as add_example_parser
from jla_tools.terminal_animations.terminal_animations import add_parsers as add_terminal_animation_parser
from jla_tools.devcontainer.dev import add_parsers as add_dev_parser

def parsers():
    parser = argparse.ArgumentParser(
        description="""Jla cli tool for whatever"""
    )

    subparsers = parser.add_subparsers(
        help='See the help of individual comands for a more detailed description.')

    add_example_parser(subparsers)
    add_terminal_animation_parser(subparsers)
    add_dev_parser(subparsers)

    argcomplete.autocomplete(parser)
    return parser
