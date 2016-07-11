#!env python
from setuptools import setup

INSTALL_REQUIREMENTS = [
    'argparse'
]

VERSION = '1.0.0b'

setup(name='webbench',
      version=VERSION,
      packages=[
          'webbench',
      ],
      classifiers=[
          'Development Status :: 4 - Beta',
          'Environment :: Console',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 2.7',
          'Topic :: Internet :: WWW/HTTP',
          'Topic :: Software Development :: Quality Assurance',
          'Topic :: Software Development :: Testing',
          'Topic :: Software Development :: Testing :: Traffic Generation',
          'Topic :: Utilities'
      ],
      install_requires=INSTALL_REQUIREMENTS,
      include_package_data=True,
      # Metadata.
      description='lightweight HTTP/HTTPS benchmark tool written on Python',
      author='Artem Rozumenko',
      entry_points={
          'console_scripts': ['webbench=webbench.webbench:main'],
      },
      author_email='artem.rozumenko@gmail.com',
      url='https://github.com/arozumenko/pybench',
      license='MIT License')
