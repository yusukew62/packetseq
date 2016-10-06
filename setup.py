#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(
    name = 'packetseq',
    version  = '0.1.4',
    description = 'Create packet sequence diagram from pcap format csv file',
    license = 'MIT license',
    author = 'Yusuke Watanabe',
    author_email = 'yusuke.w62@gmail.com',
    url	= 'https://github.com/yusukew62/packetseq.git',
    keywords = 'python seqdiag',
    packages = find_packages(),
    install_requires = ['seqdiag'],
    entry_points = {
        'console_scripts' : [
            'packetseq=packetseq.packetseq:main',
        ],
    },
)
