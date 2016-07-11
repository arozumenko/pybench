#!env python
from setuptools import setup

INSTALL_REQUIREMENTS = [
    'argparse'
]

VERSION = '1.0.0a'

setup(name='pybench',
      version=VERSION,
      packages=[
          'pybench',
      ],
      install_requires=INSTALL_REQUIREMENTS,
      include_package_data=True,
      # Metadata.
      description='lightweight HTTP/HTTPS benchmark tool written on Python',
      author='arozumenko',
      entry_points={
          'console_scripts': ['pybench=pybench.pybench:main'],
      },
      author_email='artem.rozumenko@gmail.com',
      url='https://github.com/arozumenko/pybench',
      license='MIT')
