import json

"""Utility to update files when data changes

MAYBE make oop instead of static
MAYBE use multiprocessing

Methods
-------
update_json
    update json file with data from dictionary
write_file
    write file
"""


def update_json(dictionary, file_path):
    """update json file with data from dictionary

    Parameters
    ----------
    dictionary : dict
        dict containing updated data
    file_path : str
        path of file to be updated
    """

    with open(file_path, 'w') as file:
        json.dump(dictionary, file, indent=2)


def write_file(content, file_path):
    """write file

    Parameters
    ----------
    content : str
        content of file
    file_path : str
        relative file path
    """
    with open(file_path, 'w') as file:
        file.write(content)
