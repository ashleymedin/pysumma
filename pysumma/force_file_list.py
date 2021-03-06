import os
import xarray as xr

from .option import BaseOption
from .option import OptionContainer


class ForceFileListOption(BaseOption):

    def __init__(self, name):
        super().__init__(name)
        self.set_value(xr.open_dataset(name))

    def set_value(self, new_value):
        self.value = new_value

    @property
    def path(self):
        return self.name.replace("'", "")

    @path.setter
    def path(self, value):
        self.set_value(value)

    def __str__(self):
        return "'{}'".format(self.name.split('/')[-1])


class ForceFileList(OptionContainer):

    prefix: str = ''

    def __init__(self, dirpath, filepath, force_file_prefix_path):
        self.prefix = force_file_prefix_path
        super().__init__(ForceFileListOption, dirpath, filepath)

    def set_option(self, key, value):
        o = self.get_option(key)
        o.set_value(value)

    def get_constructor_args(self, line):
        file_name = line.replace("'", "")
        return (os.path.join(self.prefix, file_name.strip()), )

    @property
    def forcing_paths(self):
        return [o.path for o in self.options]

    @property
    def forcing_data(self):
        return [o.value for o in self.options]
