from setuptools import setup, find_packages

setup(name='FormatJSONBib',
      version='0.1',
      description='Format JSON bibliography as HTML for static website',
      url='',
      author='Michael Dunn',
      author_email='michael.dunn@lingfil.uu.se',
      license='MIT',
      packages=['FormatJSONBib'],
      scripts=['bin/jsonbib']
      )
