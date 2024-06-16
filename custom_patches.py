class Data:
    def __init__(self, offset=None, default=None, modified=None, conditional=None):
        self.offset = offset
        self.default = default
        self.modified = modified
        self.conditional = conditional


class Parameter:
    def __init__(self, enabled=None, name=None, offset=None, value=None, type=None, conditional=None):
        self.enabled = enabled
        self.name = name
        self.offset = offset
        self.value = value
        self.type = type
        self.conditional = conditional


class Patch:
    def __init__(self, enabled=None, name=None, description=None, category=None, dependencies=None, filename=None):
        self.enabled = enabled
        self.name = name
        self.description = description
        self.category = category
        self.dependencies = dependencies
        self.filename = filename
        self.data = []
        self.parameter = []


class PatchSet:
    def __init__(self, version=None):
        self.version = version
        self.patch = []


def read_patch_set(path):
    patch_set = PatchSet()
    with path.open(newline='\r\n') as source:
        current_patch = None
        for line in source:
            key, separator, value = line.strip().partition('=')
            if not separator:
                continue
            if patch_set.version is None:
                if key == 'patchsetversion':
                    patch_set.version = value
            elif key == 'header':
                current_patch = Patch()
                patch_set.patch.append(current_patch)
            elif key == 'enabled':
                current_patch.enabled = int(value)
            elif key == 'name':
                current_patch.name = value
            elif key == 'description':
                current_patch.description = value
            elif key == 'category':
                current_patch.category = value
            elif key == 'dependencies':
                current_patch.dependencies = value
            elif key == 'filename':
                current_patch.filename = value
            elif key != 'footer':
                _, _, nested_value = value.partition(',')
                if key == 'dataoffset':
                    current_data = Data(nested_value)
                    current_patch.data.append(current_data)
                elif key == 'datadefault':
                    current_data.default = nested_value
                elif key == 'datamodified':
                    current_data.modified = nested_value
                elif key == 'datacondbehave':
                    current_data.conditional = int(nested_value)
                elif key == 'parenabled':
                    current_parameter = Parameter(int(nested_value))
                    current_patch.parameter.append(current_parameter)
                elif key == 'parname':
                    current_parameter.name = nested_value
                elif key == 'paroffset':
                    current_parameter.offset = nested_value
                elif key == 'parvalue':
                    current_parameter.value = nested_value
                elif key == 'partype':
                    current_parameter.type = int(nested_value)
                elif key == 'parcondbehave':
                    current_parameter.conditional = int(nested_value)
    return patch_set


def write_patch_set(path, patch_set):
    with path.open('w', newline='\r\n') as destination:
        destination.write('patchsetversion={}\r\r\n'.format(patch_set.version))
        for number, current_patch in enumerate(patch_set.patch):
            destination.write('  header={}\r\n'.format(number))
            destination.write('      enabled={}\n'.format(current_patch.enabled))
            destination.write('      name={}\n'.format(current_patch.name))
            destination.write('      description={}\n'.format(current_patch.description))
            destination.write('      category={}\n'.format(current_patch.category))
            destination.write('      dependencies={}\n'.format(current_patch.dependencies))
            destination.write('      filename={}\r\n'.format(current_patch.filename))
            for index, current_data in enumerate(current_patch.data):
                destination.write('      dataoffset={},{}\n'.format(index, current_data.offset))
                destination.write('      datadefault={},{}\n'.format(index, current_data.default))
                destination.write('      datamodified={},{}\n'.format(index, current_data.modified))
                destination.write('      datacondbehave={},{}\r\n'.format(index, current_data.conditional))
            for index, current_parameter in enumerate(current_patch.parameter):
                destination.write('      parenabled={},{}\n'.format(index, current_parameter.enabled))
                destination.write('      parname={},{}\n'.format(index, current_parameter.name))
                destination.write('      paroffset={},{}\n'.format(index, current_parameter.offset))
                destination.write('      parvalue={},{}\n'.format(index, current_parameter.value))
                destination.write('      partype={},{}\n'.format(index, current_parameter.type))
                destination.write('      parcondbehave={},{}\r\n'.format(index, current_parameter.conditional))
            destination.write('  footer={}\r\r\n'.format(number))
