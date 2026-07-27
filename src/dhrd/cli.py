# src/dhrd/cli.py

import argparse
from dhrd.release.build import build_all

def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("build")

    args = parser.parse_args()

    if args.command == "build":
        build_all()