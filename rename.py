import pathlib
import re
import argparse


def main():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('path', type=pathlib.Path)
    args = parser.parse_args()
    with args.path.open(newline='') as source:
        contents = source.read()
    contents = re.sub(r'\bPlugin_FLEP\b', 'Plugin_FlexiblePatcher', contents).replace('https://raw.githubusercontent.com/asasas9500/flep/master/downloads/Manual_FLEP.pdf', 'https://raw.githubusercontent.com/FlexiblePatcher/FlexiblePatcher/master/downloads/Manual_FlexiblePatcher.pdf')
    with args.path.open('w', newline='') as destination:
        destination.write(contents)


if __name__ == '__main__':
    main()
