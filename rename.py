import pathlib
import re
import argparse


def main():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('path', nargs='+', type=pathlib.Path)
    args = parser.parse_args()
    for current_path in args.path:
        with current_path.open(newline='') as source:
            contents = source.read()
        contents = re.sub(r'\bPlugin_FLEP\b', 'Plugin_FlexiblePatcher', contents)
        with current_path.open('w', newline='') as destination:
            destination.write(contents)


if __name__ == '__main__':
    main()
