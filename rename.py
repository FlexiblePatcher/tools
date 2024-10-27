import pathlib
import re
import argparse


def main():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('path', type=pathlib.Path)
    args = parser.parse_args()
    with args.path.open(newline='') as source:
        contents = source.read()
    contents = re.sub(r'\bPlugin_FLEP\b', 'Plugin_FlexiblePatcher', contents)
    with args.path.open('w', newline='') as destination:
        destination.write(contents)


if __name__ == '__main__':
    main()
