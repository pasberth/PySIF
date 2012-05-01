from setuptools import setup, find_packages

setup( name = "pysif",
       author = 'pasberth',
       author_email = 'pasberth@gmail.com',
       url = 'https://github.com/pasberth/PySIF',
       packages = find_packages('src'),
       package_dir = {'':'src'},
       entry_points = {
        'console_scripts': [ 'sif.py = sif.cli:main', 'mmf.py = mmf.cli:main' ],
       }, )