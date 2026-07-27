# src/dhrd/cli.py

import argparse
from dhrd.release.build import build_all
from dhrd.release.package import package_release

def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("build")

    package_parser = subparsers.add_parser("package")
    package_parser.add_argument(
        "part",
        choices = ["major","minor","patch"],
        help="Part of the dataset version to implement"
    )
    
    args = parser.parse_args()

    if args.command == "build":
        build_all()
    elif args.command == "package":
        build_all()
        package_release(args.part)