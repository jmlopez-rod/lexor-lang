"""Lexor-Lang Web Module

Collection of functions to build html pages.

"""
import operator
import lexor.core.elements as core


def read_style_urls(path):
    """Read and parse the file specified by path. The format needs to
    be very specific. Each line has to have one of the following:

        lang.type.style: url

    or

        fromlang.converter.tolang.style: url

    """
    lang = dict()
    for line in open(path).readlines():
        name, url = line.strip().split(':', 1)
        name = name.split('-')
        if name[1] == 'converter':
            key = '%s.%s.%s' % (name[0], name[1], name[2])
            style = name[3]
        else:
            key = '%s.%s' % (name[0], name[1])
            style = name[2]
        if key not in lang:
            lang[key] = list()
        lang[key].append((style, url.strip()))
    return lang


def make_lang_node(lang):
    """Create an unordered list element containing a link to all the
    lexor language styles stored in the dictionary lang."""
    lang_node = core.Element('ul', {'id': 'lexor_lang'})
    keys = lang.keys()
    keys.sort()
    for key in keys:
        lang[key].sort(key=operator.itemgetter(0))
        processor = core.Element('li', {'id': key})
        processor.append_child(core.Text(key))
        processor.append_child(core.Element('ul'))
        for style, url in lang[key]:
            processor[-1].append_child(core.Element('li'))
            link = core.Element('a', {'href': url})
            link.append_child(style)
            processor[-1][-1].append_child(link)
        lang_node.append_child(processor)
    return lang_node
