=================
gitlab-clone
=================


Tool for easy cloning whole gitlab structure to your local machine.


* Free software: MIT license



Requirements
------------

* Requests



Installation
------------

You can install "gitlab-clone" via `pip`_::

    $ pip install gitlab-clone


Usage
-----


>>> gitlab-clone:
  optional arguments:
  -h, --help           show this help message and exit
  --group_id group_id  Id of a group in gitlab
  --token token        Gitlab Token
  --branch branch      Branch to clone in all repos [by default master]
  --gitlab-url gitlab  Gitlab address [by default gitlab.com]


Example
-------

    $  gitlab-clone --group=123 --token=MySecretToken --gitlab-url=gitlab.organization.com

    For example if you clone this group https://gitlab.com/lmaolmaolmao which id is 6849299

    you will have absolutely the same structure locally:

    .. image:: https://github.com/ArseniyAntonov/gitlab-group-clone/raw/master/img/tree.png

>>> tree
   .
    └── lmaolmaolmao
        └── subgroup1
            └── subgroup2
                └── subgroup3



.. _`pip`: https://pypi.python.org/pypi/pip/
