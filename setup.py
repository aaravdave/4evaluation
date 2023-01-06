from setuptools import setup

setup(
    name='4evaluation',
    version='1.0',
    long_description=__doc__,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=['Flask', 'passlib', 'pymongo']
)
