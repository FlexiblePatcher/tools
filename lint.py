import pathlib
import argparse
import itertools
import collections

import custom_patches
import memory_regions
import helpers


def main():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('path', type=pathlib.Path)
    parser.add_argument('name_report_path', type=pathlib.Path)
    parser.add_argument('region_report_path', type=pathlib.Path)
    args = parser.parse_args()
    patch_set = custom_patches.read_patch_set(args.path)
    name_list = []
    region_list = []
    for number, current_patch in enumerate(patch_set.patch):
        name_list.append(current_patch.name)
        region_list.extend([memory_regions.Region(int(current_data.offset, 16), len(current_data.modified) // 2, number, current_patch.name, 'data', index) for index, current_data in enumerate(current_patch.data)])
        for index, current_parameter in enumerate(current_patch.parameter):
            offset_list = current_parameter.offset.split(',')
            count = helpers.count_of_type(current_parameter.type)
            for offset in offset_list:
                nested_offset_list = offset.split('|')
                nested_count = count // len(nested_offset_list)
                region_list.extend([memory_regions.Region(int(nested_offset, 16), nested_count, number, current_patch.name, 'parameter', index) for nested_offset in nested_offset_list])
    with args.name_report_path.open('w', newline='\r\n') as destination:
        for name, frequency in collections.Counter(name_list).items():
            if frequency > 1:
                destination.write('{} : {}\n'.format(name, frequency))
    with args.region_report_path.open('w', newline='\r\n') as destination:
        for region, test_region in itertools.combinations(region_list, 2):
            if region.number != test_region.number and region.overlap(test_region):
                destination.write('{} & {}\n'.format(region.to_string(), test_region.to_string()))


if __name__ == '__main__':
    main()
