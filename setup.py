from distutils.core import setup
from os.path import dirname, join

version = '0.1.0'


def read(fname):
    return open(join(dirname(__file__), fname)).read()


with open("requirements.txt", "r'") as f:
    install_reqs = f.readlines()

setup(
    name='pytools',
    version=version,
    packages=['pytools', 'pytools.core', 'pytools.twitter'],
    url='',
    license='',
    author='Chad Dotson',
    author_email='chad@cdotson.com',
    description=''
)
