import pathlib
import argparse
import os

import custom_patches
import external_variables
import helpers


def main():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('input_path', type=pathlib.Path)
    parser.add_argument('plugin_path', type=pathlib.Path)
    parser.add_argument('output_path', type=pathlib.Path)
    args = parser.parse_args()
    patch_set = custom_patches.read_patch_set(args.input_path)
    data_buffer = external_variables.Variable()
    data_address = external_variables.Variable()
    parameter_buffer = external_variables.Variable()
    parameter_address = external_variables.Variable()
    for number, current_patch in enumerate(patch_set.patch):
        current_patch.filename = 'patches.fpd'
        for current_data in current_patch.data:
            data_buffer.initializer.extend(['0x{:02X}'.format(int(current_data.modified[position:position + 2], 16)) for position in range(0, len(current_data.modified), 2)])
            data_buffer.add_segment()
            data_address.initializer.append('0x{:06X}'.format(int(current_data.offset, 16)))
        data_address.add_segment()
        current_patch.data.clear()
        current_patch.data.append(custom_patches.Data('{:X}'.format(number + 2), '', '01', 1))
        for current_parameter in current_patch.parameter:
            offset_list = current_parameter.offset.split(',')
            start = parameter_buffer.next_start()
            count = helpers.count_of_type(current_parameter.type)
            for offset in offset_list:
                nested_offset_list = offset.split('|')
                nested_count = count // len(nested_offset_list)
                for iteration, nested_offset in enumerate(reversed(nested_offset_list)):
                    parameter_buffer.segment.append(external_variables.Segment(start + iteration, nested_count))
                    parameter_address.initializer.append('0x{:06X}'.format(int(nested_offset, 16)))
            current_parameter.offset = '{:X}'.format(start + len(patch_set.patch) + 2)
            current_parameter.conditional = 1
        parameter_address.add_segment()
    parameter_buffer_size = parameter_buffer.next_start()
    version = os.getenv('GITHUB_RUN_NUMBER', '0')
    with args.plugin_path.joinpath('patch_data.cpp').open('w', newline='\r\n') as destination:
        destination.write('#include "patch_data.h"\n\n')
        destination.write('unsigned short version;\n')
        destination.write('bool patch_selected[{}];\n'.format(len(patch_set.patch) if patch_set.patch else 1))
        destination.write('const int patch_selected_size = {};\n'.format(len(patch_set.patch)))
        destination.write(data_buffer.definition('unsigned char', 'data_buffer'))
        destination.write(data_address.definition('unsigned int', 'data_address'))
        destination.write('unsigned char parameter_buffer[{}];\n'.format(parameter_buffer_size if parameter_buffer_size != 0 else 1))
        destination.write('const int parameter_buffer_size = {};\n'.format(parameter_buffer_size))
        destination.write(parameter_buffer.segment_definition('parameter_buffer'))
        destination.write(parameter_address.definition('unsigned int', 'parameter_address'))
    with args.plugin_path.joinpath('version.h').open('w', newline='\r\n') as destination:
        destination.write('#define VERSION {}\n'.format(version))
        destination.write('#define VER_FILEVERSION {},0,0,0\n'.format(version))
        destination.write('#define VER_FILEVERSION_STR "{}.0.0.0\\0"\n'.format(version))
    first_patch = custom_patches.Patch(1, 'Version', 'Writes the version of the Flexible Patcher data file.', '', '', 'patches.fpd')
    first_patch.data.append(custom_patches.Data('0', 'SetFileLength,0', 'SetFileLength,0', 0))
    command = 'Fill,00,{:X}'.format(parameter_buffer_size + len(patch_set.patch) + 2)
    first_patch.data.append(custom_patches.Data('0', command, command, 0))
    header = ''.join(['{:02X}'.format(byte) for byte in int(version).to_bytes(2, 'little')])
    first_patch.data.append(custom_patches.Data('0', header, header, 0))
    patch_set.patch.insert(0, first_patch)
    custom_patches.write_patch_set(args.output_path, patch_set)


if __name__ == '__main__':
    main()
