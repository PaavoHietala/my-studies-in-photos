import os

def list_files(dir):
    '''
    List all filepaths in given directory and its subdirectories.

    Parameters
    ----------
    dir : str
        Base directory for the search

    Returns
    -------
    [str]
        List of full file paths in dir
    '''

    return [os.path.join(path, name) for path, subdirs, files in os.walk(dir) for name in files]