from setuptools import setup

setup(
    name='clean_folder',
    version='1.0',
    packages=['clean_folder'],
    entry_points={
        'console_scripts': [
            'clean-folder = clean_folder.clean:main',
        ],
    },
)
