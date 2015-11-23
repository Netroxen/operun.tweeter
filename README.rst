.. This README is meant for consumption by humans and pypi. Pypi can render rst files so please do not use Sphinx features.
   If you want to learn more about writing documentation, please check out: http://docs.plone.org/about/documentation_styleguide_addons.html
   This text does not appear on pypi or github. It is a comment.

==============================================================================
operun.tweeter
==============================================================================

Plone Twitter module which fetches tweets and displays them as tiles.

Features
--------

- Hashtag and multiple search queries possible.
- Error handling and info tool-tips.
- User statistics displayed in tiles.
- Possible to select how many tweets to fetch.

Documentation
-------------

Current implementation for usage works as follows:

1. Start an instance inside the operun.tweeter. [./bin/instance fg]
2. Open your browser and navigate to localhost:8080/Plone/tweeter.

Translations
------------

No translations available currently.
German translation possible.

Installation
------------

Install operun.tweeter by adding it to your buildout::

    [buildout]

    ...

    eggs =
        operun.tweeter


and then running ``bin/buildout``


Contribute
----------

- Issue Tracker: https://github.com/collective/operun.tweeter/issues
- Source Code: https://github.com/collective/operun.tweeter

License
-------

The project is licensed under the GPLv2.
