#! /usr/bin/env python3
from argparse import ArgumentParser
from time import sleep

from .projector import ProjectorSerial
from .extron import ExtronSerial

verbose = False


def main():
    parser = ArgumentParser(
        prog="projectorpi", description="A tool that turns the projector on and off."
    )

    parser.add_argument(
        "-v", "--verbose", action="store_true", help="increase output verbosity"
    )

    sleep_or_wake = parser.add_mutually_exclusive_group(required=True)
    sleep_or_wake.add_argument(
        "input",
        nargs="?",
        type=int,
        choices=[1, 2, 3, 4],
        help="wake and select input",
    )
    sleep_or_wake.add_argument("--sleep", action="store_true", help="put in sleep mode")
    args = parser.parse_args()

    verbose = args.verbose

    proj = ProjectorSerial(verbose)
    extr = ExtronSerial(verbose)

    if args.input:
        proj.power_on()
        extr.wake()
        sleep(1)
        extr.change_input(args.input)

    elif args.sleep:
        proj.power_off()
        extr.sleep()
