
HTML: DEFAULT Parsing Style
===========================

This style attempts to follow all the HTML rules. It captures all the
information in the file. This includes all the extra spaces, new
lines and tab characters the file might contain.

Package Details
---------------

:Author: Manuel Lopez
:Contact: jmlopez.rod@gmail.com
:Type: Parser
:Language: html
:Style: default
:Version: 0.0.1
:URL: http://jmlopez-rod.github.io/lexor-lang/html-parser-default
:License: BSD License

.. meta::
   :keywords: html, default, parser
   :description lang=en: Parse HTML files using all the valid rules.


Mapping
-------

:__default__: Checks at ``'<&'``.

    #. ``ElementNP``
    #. ``CDataNP``
    #. ``DocumentTypeNP``

:p:

    afdfadf


CDataNP
-------

.. py:function:: spam(eggs)
                 ham(eggs)

   Spam or ham the foo.

Great