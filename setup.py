from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))


def readme():
    try:
        with open('README.md') as f:
            return f.read()
    except Exception as e:
        print(e)
        pass


setup(
    name='meme-generator',
    version='1.0',
    description='Generate memes',
    long_description=readme(),
    long_description_content_type='text/markdown',
    author='Subhrajit Prusty',
    author_email='subhrajit1997@gmail.com',
    url='http://github.com/SubhrajitPrusty/meme-generator',
    setup_requires=['setuptools>=40.0'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='meme memes image',
    license='MIT',
    packages=find_packages(),
    install_requires=['click', 'pillow'],
    entry_points="""
    [console_scripts]
        memegen=generate:cli
        """,
)
