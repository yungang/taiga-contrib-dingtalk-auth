#!/usr/bin/env python
# -*- coding: utf-8 -*-

import versiontools_support
from setuptools import setup, find_packages

setup(
    name = 'taiga-contrib-dingtalk-auth',
    version = ":versiontools:taiga-contrib-dingtalk-auth:",
    description = "The Taiga plugin for dingtalk authentication",
    long_description = "",
    keywords = 'taiga, dingtalk, auth, plugin',
    author = 'Zang Yun-gang',
    author_email = 'zangyungang@gmail.com',
    url = 'https://github.com/yungang/taiga-contrib-dingtalk-auth',
    license = 'AGPL',
    include_package_data = True,
    packages = find_packages(),
    install_requires=[],
    setup_requires = [
        'versiontools >= 1.9',
    ],
    classifiers = [
        "Programming Language :: Python",
        'Development Status :: 4 - Beta',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
    ]
)
