import pathlib
import re
import argparse


def main():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('path', type=pathlib.Path)
    args = parser.parse_args()
    with args.path.open(newline='\r\n') as source:
        contents = source.read()
    with args.path.open('w', newline='\r\n') as destination:
        destination.write(re.sub(r'\bPlugin_FLEP\b', 'Plugin_FlexiblePatcher', contents))


if __name__ == '__main__':
    main()
