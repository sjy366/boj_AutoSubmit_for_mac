from setuptools import setup

py_modules = [
    'requests',
    'bs4'
]

setup(name='BOJ_Code_Downloader',
      version='1.0',
      description='This is BOJ_Code_Downloader.',
      author='Jungyeon Sohn (sjy366)',
      author_email='sjy20131565@gmail.com',
      install_requires=py_modules)
      