
.. _main:

HTML: default
=============

This style attempts to follow all the HTML rules. It captures all the
information in the file. This includes all the extra spaces, new
lines and tab characters the file might contain.

Package Details
---------------

:Author: Manuel Lopez
:Contact: jmlopez.rod@gmail.com
:Type: parser
:Language: html
:Style: default
:Version: 0.0.1
:Download: http://jmlopez-rod.github.io/lexor-lang/html-parser-default
:License: BSD License

.. meta::
    :keywords: html, default, parser
    :description lang=en: Parse HTML files using all the valid rules.

Mapping
-------

.. container:: mapping

    .. list-table::
       :widths: 25 75
       :header-rows: 1

       * - Node Name
         - Node Parsers
       * - **__default__**
         - ``<&\\\\`\'\"*_{}[\\]()#+-.!%$:\n``
            #. :class:`CDataNP`
            #. :class:`ProcessingInstructionNP`
       * - **#document**
         -  #. :class:`CDataNP`
            #. :class:`CDataNP`
            #. :class:`ProcessingInstructionNP`
       * - **p**
         - ``'<&\\\\`\'\"*_{}[\\]()#+-.!%$:\n'``
            #. :class:`CDataNP`
            #. :class:`ProcessingInstructionNP`

Data
++++

.. code::

    MOD = {
        "cdata": "lexor-lang_html_parser_default_cdata",
        "comment": "lexor-lang_html_parser_default_comment",
        "doctype": "lexor-lang_html_parser_default_doctype",
        "element": "lexor-lang_html_parser_default_element",
        "entity": "lexor-lang_html_parser_default_entity",
        "pi": "lexor-lang_html_parser_default_pi"
    }


.. _lexor-lang_html_parser_default_cdata:

CData
-----

``CData`` nodes are enclosed within ``<![CDATA[`` and ``]]>``. These
type of nodes are useful because no parsing takes place inside the
content. The only restriction involved with these nodes is that the
character sequence ``]]>`` must not appear in the content.

In case there is a need to write ``]]>`` inside the character data
then you have to split the content into two ``CData`` nodes:

The correct way to write the following ::

    <![CDATA[Cannot have ``]]>`` inside.]]>

is ::

    <![CDATA[Cannot have ``]]]]><![CDATA[>`` inside.]]>

.. class:: CDataNP(parser)

    Bases :class:`lexor.core.parser.NodeParser`

    Retrives the data enclosed within ``<![CDATA[`` and ``]]>``
    and returns a ``CData`` node. 

    .. method:: make_node()

        See base class for method explanation.

Data
++++

.. code::

    MSG = {
        "E100": "``]]>`` not found"
    }

    MSG_EXPLANATION = [
        """
        - The terminating character sequence for the ``CData`` node was
          not found.
    
        Okay: <![CDATA[We can write a < b and M&Ms.]]>
    
        E100: <![CDATA[We can write a < b and M&Ms.
    """
    ]


.. _lexor-lang_html_parser_default_pi:

Processing Instruction
----------------------

An HTML processing instruction is enclosed within ``<?`` and ``?>``.
It contains a target and optionally some content. The content is the
node data and it cannot contain the sequence ``?>``. A valid
processing instruction is of the form ::

    <?PITarget*PIContent?>

where ``*`` is a space character (this includes tabs and new lines).

.. class:: ProcessingInstructionNP(parser)

    Bases :class:`lexor.core.parser.NodeParser`

    Parses content enclosed within ``<?PITarget`` and ``?>``. Note
    that the target of the ``ProcessingInstruction`` object that it
    returns has ``?`` preappended to it. 

    .. method:: make_node()

        See base class for method explanation.

Data
++++

.. code::

    RE = ".*?[ \t\n\r\f\u000b]"

    MSG = {
        "E100": "ignoring processing instruction",
        "E101": "`<{0}` was started but `?>` was not found"
    }

    MSG_EXPLANATION = [
        """
        - A processing instruction must have a target and must be
          enclosed within `<?` and `?>`.
    
        - If there is no space following the target of the processing
          instruction, that is, if the file ends abrutly, then the
          processing instruction will be ignored.
    
        Okay: <?php echo '<p>Hello World</p>'; ?>
    
        E100: <?php
        E101: <?php echo '<p>Hello World</p>';
    """
    ]


.. _lexor-lang_html_parser_default_doctype:
HTML: DOCTYPE NodeParser

DOCTYPE is case insensitive in HTML. The following forms are valid:

    <!doctype html>
    <!DOCTYPE html>
    <!DOCTYPE HTML>
    <!DoCtYpE hTmL>

See: <http://stackoverflow.com/a/9109157/788553>

.. class:: DocumentTypeNP(parser)

    Bases :class:`lexor.core.parser.NodeParser`

    Obtains the content enclosed within `<!doctype` and `>`. 

    .. method:: make_node()

        See base class for method explanation.

Data
++++

.. code::

    MSG = {
        "E100": "`>` not found"
    }

    MSG_EXPLANATION = [
        """
        - A `doctype` element starts with `<!doctype` and it is
          terminated by `>`.
    
        Okay: <!doctype html>
        Okay: <!DOCTYPE html>
    
        E100: <!doctype html
    """
    ]


.. _lexor-lang_html_parser_default_comment:

Comment
-------

An HTML comment is enclosed within ``<!--`` and ``-->``. The string
``--`` (double-hyphen) **MUST NOT** occur within comments. If the
string starts with ``<!`` then it is still a comment but a warning
will be issued.

See: http://www.w3.org/TR/REC-xml/#sec-comments

.. class:: CommentNP(parser)

    Bases :class:`lexor.core.parser.NodeParser`

    Creates :class:`~lexor.core.elements.Comment` nodes from
    comments written in HTML. 

    .. method:: make_node()

        See base class for method explanation.

Data
++++

.. code::

    MSG = {
        "E100": "bogus comment started",
        "E200": "`-->` not found",
        "E201": "`>` not found",
        "E300": "`>` found",
        "E301": "`--` in comment opened at {0}:{1:2}"
    }

    MSG_EXPLANATION = [
        """
        - Bogus comments are detected when the parser reads `<!` and
          the next sequence of characters is not `--`.
    
        - Always start comments with `<!--`.
    
        Okay: <!--simple comment-->
    
        E100: <!simple comment-->
        E100: <!-simple comment-->
        E100: <!- -simple comment-->
    """,
        """
        - Comments end with the character sequence `-->`.
    
        - The parser will assume that the termination of the comment is
          at the end of the file.
    
        Okay: <!--x -> y-->
    
        E200: <!--x -> y
        E200: <!--x -> y-- >
        E200: <!--x -> y ->
    """,
        """
        - When a bogus comment is started, the parser is forced to look
          for the character `>` as its termination sequence instead of
          `-->`.
    
        - The original message informs you if `>` was found or not.
    
        Okay: <!-- comment -->
        E300: <! comment >
        E201: <! comment
    """,
        """
        - The character sequence `--` must not appear within a comment.
    
        - This sequence will be interpreted as `- `.
    
        Okay: <!-- 1 - 2 - 3 - 4 - 5 -->
        E301: <!-- 1 -- 2 -- 3 -- 4 -- 5 -->
    """
    ]


.. _lexor-lang_html_parser_default_entity:
HTML: ENTITY NodeParser

Some characters are reserved in HTML: `<` and `&`. To be able
to display them we need to use HTML entities. The parser defined
in this module looks for such entities.

.. class:: EntityNP(parser)

    Bases :class:`lexor.core.parser.NodeParser`

    Processes `<` and `&` characters. This parser needs to be
    called only after all the other parsers have attempted to decide
    what to do with `<` and `&`.

    .. method:: make_node()

        See base class for method explanation.

Data
++++

.. code::

    RE = ".*?[ \t\n\r\f\u000b;]"

    MSG = {
        "E100": "stray `{0}` found",
        "E101": "ignoring stray end tag `{0}`"
    }

    MSG_EXPLANATION = [
        """
        - HTML has `<` and `&` as reserved characters. To be able to
          display `<` you must write the entity `&lt;` or `&#60;`. To
          write `&` you can use the entity `&amp;`
    
        Okay: a &lt; b
        Okay: I like M&amp;Ms
    
        E100: a < b
        E100: I like M&Ms
    """,
        """
        - Stray end tags are usually an indication of an error. The short
          message tells you the location of the stray end tag but there
          is nothing that can be said about the possible error.
    
        Okay: <apples><bananas></bananas></apples>
        E101: <apples></bananas></apples>
    """
    ]


.. _lexor-lang_html_parser_default_element:

Element
-------

Handles all ``Elements`` in the form ::

    <tagname att1="val1" att2="val2">
        ...
    </tagname>

.. class:: ElementNP(parser)

    Bases :class:`lexor.core.parser.NodeParser`

    Parses all html elements. 

    .. method:: close(node)

        Return the position where the element was closed. 

    .. method:: get_raw_text(parser, tagname, pos)

        Return the data content of the RawText object and update
        the caret. 

    .. method:: is_element(parser)

        Check to see if the parser's caret is positioned in an
        element and return the index where the opening tag ends. 

    .. method:: is_empty(parser, index, end, tagname)

        Checks to see if the parser has reached '/'. 

    .. method:: make_node()

        See base class for method explanation.

    .. method:: read_attributes(parser, node, end, tname)

        Parses the string
        
            parser.text[parser.caret:end]
        
        and writes the information in node.
        
            att1="val1" att2="val2" ...
        
        This function returns True if the opening tag ends with `/`. 

    .. method:: read_prop(parser, node, end, tagname)

        Return [prop, prop_index, implied, empty]. 

    .. method:: read_val(parser, end, tagname)

        Return the attribute value. 

Data
++++

.. code::

    RAWTEXT_ELEMENT = [
        "script",
        "style",
        "textarea",
        "title"
    ]

    AUTO_CLOSE = {
        "a": [
            "a"
        ],
        "p": [
            "address",
            "article",
            "aside",
            "blockquote",
            "dir",
            "div",
            "dl",
            "fieldset",
            "footer",
            "form",
            "h1",
            "h2",
            "h3",
            "h4",
            "h5",
            "h6",
            "header",
            "hgroup",
            "hr",
            "main",
            "menu",
            "nav",
            "ol",
            "p",
            "pre",
            "section",
            "table",
            "ul"
        ]
    }

    RE_NOSPACE = "\\s*"

    RE_NEXT = ".*?[ \\t\\n\\r\\f\\v/>=]"

    MSG_EXPLANATION = [
        """
        - The opening tag of an element cannot contain `<`. This means
          that attributes cannot contain `<` in them.
    
        Okay: <apple att1=\"""val1\"""></apple>
    
        E100: <apple att1=\"""a < b\"""></apple>
    """,
        """
        - `RawText` elements are terminated when the appropiate closing
          tag is found. Make sure to provide its proper closing tag.
    
        Okay: <title>My awesome website</title>
        Okay: <script>a < b && b > c</script>
    
        E110: <title>My sheetie website</title >
        E110: <title>My sheetie website< / title >
        E110: <title>My sheetie website
        E110: <script>a < b && b > c
    """,
        """
        - A `Void` Element's opening tag must end with `/>`. Anything in
          between the characters `/` and `>` will be ignored.
    
        - Non-void elements whose opening tag start with `/>` will be
          also be interpreted correctly a message will be issued.
    
        Okay: <img href=\"""/path/to/image.png\"""/>
        Okay: <p>starting a new paragraph</p>
    
        E120: <img href=\"""/path/to/image.png\"""/  >
        E121: <p />starting a new paragraph</p>
    """,
        """
        - Attributes need to be separated by one space.
    
        - Do not repeat attributes since the values will only get
          overwritten.
    
        Okay: <tag att1=\"""val1\""" att2=\"""val2\""">content</tag>
        Okay: <tag att1='1' att2='2'></tag>
    
        E130: <tag att1=\"""val1\"""att2=\"""val2\""">content</tag>
        E160: <tag att1='1' att1='2'></tag>
    """,
        """
        A few attributes rules:
    
        - There is a risk of joining attributes together when using
          unquoted attribute values. This may result in having a quote or
          equal sign inside the unquoted attribute value. [E140]
    
        - If your attribute contains `/` then the attribute should be
          quoted. [E141]
    
        - Quoted attributes need to be finished by its starting quotation
          character. [E150]
    
        Okay: <tag att1=val1 att2=\"""val2\""">content</tag>
        E140: <tag att1=val1att2=\"""val2\""">content</tag>
    
        Okay: <img href=\"""path/to/image.png\""" />
        E141: <img href=path/to/image.png />
    
        Okay: <tag att1=\"""num\"""></tag>
        Okay: <tag att1='num'></tag>
    
        E150: <tag att1=\"""num></tag>
        E150: <tag att1='num></tag>
    """
    ]

    VOID_ELEMENT = [
        "area",
        "base",
        "basefont",
        "br",
        "col",
        "frame",
        "hr",
        "img",
        "input",
        "isindex",
        "link",
        "meta",
        "param",
        "command",
        "embed",
        "keygen",
        "source",
        "track",
        "wbr"
    ]

    MSG = {
        "E100": "element discarted due to `<` at {0}:{1:2}",
        "E110": "`RawText` closing tag `</{0}>` not found",
        "E120": "`/` not immediately followed by `>`",
        "E121": "self-closing syntax (`/>`) used in non-void element",
        "E130": "no space between attributes",
        "E140": "`{0}` found in unquoted attribute value",
        "E141": "`/` found in unquoted attribute value",
        "E150": "assuming quoted attribute to close at {0}:{1:2}",
        "E160": "attribute name \"{0}\" has already been declared"
    }

    AUTO_CLOSE_FIRST = {
        "dd": [
            "dt",
            "dd"
        ],
        "dt": [
            "dt",
            "dd"
        ],
        "li": [
            "li"
        ],
        "optgroup": [
            "optgroup"
        ],
        "option": [
            "optgroup",
            "option"
        ],
        "rp": [
            "rt",
            "rp"
        ],
        "rt": [
            "rt",
            "rp"
        ],
        "tbody": [
            "tbody",
            "tfoot"
        ],
        "td": [
            "td",
            "th"
        ],
        "tfoot": [
            "tbody"
        ],
        "th": [
            "td",
            "th"
        ],
        "thead": [
            "tbody",
            "tfoot"
        ],
        "tr": [
            "tr"
        ]
    }

    RE = ".*?[ \\t\\n\\r\\f\\v/>]"

