#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

requirements = ['requests']

test_requirements = ['pytest', ]

setup(
    author="Arseniy Antonov",
    author_email='arseny.antonov@gmail.com',
    classifiers=[
        'Framework :: Pytest',
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    description="Gitlab tool for recursive clone",
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n',
    include_package_data=True,
    keywords=[
        'gitlab', 'gitlab-api',
    ],
    name='gitlab-clone',
    packages=find_packages(include=['gitlab_clone']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/ArseniyAntonov/gitlab-group-clone',
    version='0.1.3',
    entry_points={
        "console_scripts": [
            "gitlab-clone=gitlab_clone.clonner:main",
        ]
    },
    zip_safe=False,
)
