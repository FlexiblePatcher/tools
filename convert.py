import pathlib
import argparse

import custom_patches


def offset_to_address(offset):
    return offset + (0x400000 if offset < 0xC4000 else 0x750000)


def main():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('input_path', type=pathlib.Path)
    parser.add_argument('output_path', type=pathlib.Path)
    args = parser.parse_args()
    patch_set = custom_patches.read_patch_set(args.input_path)
    for current_patch in patch_set.patch:
        current_patch.filename = 'tomb4.exe'
        filtered_data = []
        for current_data in current_patch.data:
            offset = int(current_data.offset, 16)
            if offset >= 0xC3000 and offset < 0xC4000:
                continue
            filtered_data.append(current_data)
            current_data.offset = '{:X}'.format(offset_to_address(offset))
        current_patch.data = filtered_data
        for current_parameter in current_patch.parameter:
            current_parameter.offset = ','.join(['|'.join(['{:X}'.format(offset_to_address(int(nested_offset, 16))) for nested_offset in offset.split('|')]) for offset in current_parameter.offset.split(',')])
    custom_patches.write_patch_set(args.output_path, patch_set)


if __name__ == '__main__':
    main()
