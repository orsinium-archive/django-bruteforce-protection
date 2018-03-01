#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from setuptools import setup


setup(
    name='djbrut',
    version='0.8.0',

    author='orsinium',
    author_email='master_fess@mail.ru',

    description='Framework for views in big projects on Django.',
    long_description=open('README.rst').read(),
    keywords='djbrut django bruteforce protection security redis',

    packages=['djbrut'],
    requires=['django', 'redis'],

    url='https://github.com/orsinium/django-bruteforce-protection',
    download_url='https://github.com/orsinium/django-bruteforce-protection/tarball/master',

    license='GNU Lesser General Public License v3.0',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Plugins',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)',
        'Programming Language :: Python',
    ],
)
