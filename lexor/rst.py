"""XML: RST Writer Style

Simple style to write an xml file into the format needed for this
project.

"""
from lexor import init, load_aux
from lexor.core.writer import NodeWriter
import lexor.core.elements as core


INFO = init(
    version=(0, 0, 1, 'final', 0),
    lang='xml',
    type='writer',
    description='Write rst file.',
    author='Manuel Lopez',
    author_email='jmlopez.rod@gmail.com',
    license='BSD License',
    path=__file__
)


class DefaultNW(NodeWriter):
    """Default way of writing HTML elements in the plain style. """

    def start(self, node):
        if isinstance(node, core.ProcessingInstruction):
            self.write('<%s' % node.name)
            if '\n' in node.data:
                self.write('\n')
            else:
                self.write(' ')
            return
        att = ' '.join(['%s="%s"' % (k, v) for k, v in node.items()])
        self.write('<%s' % node.name)
        if att != '':
            self.write(' %s' % att)
        if isinstance(node, core.Void):
            self.write('/>')
        else:
            self.write('>')

    def end(self, node):
        if node.child is None:
            if isinstance(node, core.ProcessingInstruction):
                self.write('?>')
            elif isinstance(node, core.RawText):
                self.write('</%s>' % node.name)
        else:
            self.write('</%s>' % node.name)

class DocumentNW(NodeWriter):
    """Finish document with a new line character. """

    def end(self, node):
        self.writer.endl(False)


class CDataNW(NodeWriter):
    """TODO"""

    def data(self, node):
        data = node.data.split(']]>')
        for index in xrange(len(data)-1):
            self.write(data[index] + ']]]]><![CDATA[>')
        self.write(data[-1])


class TextNW(NodeWriter):
    """TODO"""

    def data(self, node):
        data = node.data.strip()
        self.write(data)


class InfoNW(NodeWriter):
    """TODO"""

    def start(self, node):
        self.write("Package Details\n")
        self.write("---------------\n\n")

    def child(self, node):
        nodes = node('entry')
        order = [
            ('author', 'Author'),
            ('author_email', 'Contact'),
            ('type', 'Type'),
            ('lang', 'Language'),
            ('style', 'Style'),
            ('ver', 'Version'),
            ('url', 'Download'),
            ('license', 'License'),
        ]
        info = dict()
        for item in nodes:
            info[item['key']] = item.children()
        for key, sub in order:
            self.write(":%s: %s\n" % (sub, info[key]))
        self.write('\n.. meta::\n')
        kws = '%s, %s, %s' % (info['lang'], info['style'], info['type'])
        self.write('    :keywords: %s\n' % kws)
        desc = info['description'].strip()
        self.write('    :description lang=en: %s\n' % desc[9:-3])
        self.writer.endl()

    def end(self, node):
        self.writer.endl(False)


MAPPING = {
    '#document': DocumentNW,
    '#text': TextNW,
    #'#entity': '#text',
    'module': '#document',
    'doc': '#document',
    'info': InfoNW,
    '#cdata-section': CDataNW,
    '__default__': DefaultNW,
}
