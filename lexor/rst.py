"""XML: RST Writer Style

Simple style to write an xml file into the format needed for this
project.

"""
import re
import json
from lexor import init
from lexor.core.writer import NodeWriter
import lexor.core.elements as core


RE = re.compile("<module '(?P<name>.*?)' from '(?P<path>.*?)'>")
RE2 = re.compile("<(?P<name>.*?) object at (?P<id>.*?)>")
RE3 = re.compile("<class '(?P<name>.*?)'>")
RE4 = re.compile("<(?P<name>.*?) instance at (?P<id>.*?)>")


INFO = init(
    version=(0, 0, 1, 'final', 0),
    lang='xml',
    type='writer',
    description='Write rst file for the lexor-lang project.',
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
        string = ''
        for index in xrange(len(data)-1):
            string += data[index] + ']]]]><![CDATA[>'
        string += data[-1]
        if node.parent.parent.name != 'module':
            if node.parent.parent.name == 'function':
                indent = '    '*2
            else:
                indent = '    '
            data = string.splitlines(True)
            string = indent.join(data)
            if node.index in [0, 1]:
                string = indent + string
        self.write(string)


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


class MappingNW(NodeWriter):
    """TODO"""

    def start(self, node):
        self.write("Mapping\n")
        self.write("-------\n\n")

    def child(self, node):
        pass

    def end(self, node):
        self.writer.endl(False)


class ImportsNW(NodeWriter):
    """TODO"""

    def start(self, node):
        pass

    def child(self, node):
        pass

    def end(self, node):
        pass


class ClassesNW(NodeWriter):
    """TODO"""

    def start(self, node):
        pass

    def end(self, node):
        pass


class FunctionsNW(NodeWriter):
    """TODO"""

    def start(self, node):
        pass

    def end(self, node):
        pass


class ModuleNW(NodeWriter):
    """Supports cross referencing for modules. """

    def start(self, node):
        self.write('\n.. _%s:\n' % node["name"])

    def end(self, node):
        self.writer.endl(False)


class ClassNW(NodeWriter):
    """Declares the class. """

    def start(self, node):
        self.writer.crt_class = node['name']
        functions = node('function')
        init_function = None
        for func in functions:
            if func['name'] == '__init__':
                init_function = func
        if init_function:
            argspecs = init_function("argspec")[0]
            arg = argspecs("arg")
            args = ''
            index = 1
            while index < len(arg) - 1:
                args += arg[index]["name"] + ', '
                index += 1
            if index < len(arg):
                args += arg[index]["name"]
            if args != '':
                args = '(' + args + ')'
            self.write('.. class:: %s%s\n\n' % (node["name"], args))
        else:
            self.write('.. class:: %s\n\n' % node["name"])


class BasesNW(NodeWriter):
    """TODO"""

    def start(self, node):
        self.write('    Bases ')

    def child(self, node):
        classes = [
            ':class:`%s`' % x['name'] for x in node.iter_child_elements()
        ]
        self.write(", ".join(classes))
        self.write("\n\n")


class MRONW(NodeWriter):
    """TODO"""

    def start(self, node):
        pass

    def child(self, node):
        pass

    def end(self, node):
        pass


class MethodBlockNW(NodeWriter):
    """TODO"""

    def start(self, node):
        pass

    def child(self, node):
        if not node["from"].startswith('lexor-lang'):
            return None
        for func in node.iter_child_elements():
            if func['name'][0] == '_':
                continue
            self.write('\n    .. method:: %s' % (func['name']))
            argspecs = func("argspec")[0]
            arg = argspecs("arg")
            args = '('
            index = 1
            while index < len(arg) - 1:
                args += arg[index]["name"] + ', '
                index += 1
            if index < len(arg):
                args += arg[index]["name"]
            args += ')'
            self.write(args + "\n\n")
            docs = func('doc')
            if len(docs) == 0:
                self.write("        ")
                self.write("See base class for method explanation.\n")
            else:
                for node_item in docs[0].child:
                    self.writer[node_item.name].data(node_item)
                self.write('\n')


class MemberBlockNW(NodeWriter):
    """TODO"""

    def start(self, node):
        pass

    def child(self, node):
        pass


class DataBlockNW(NodeWriter):
    """TODO"""

    def start(self, node):
        self.write("\nData\n")
        self.write("++++\n\n.. code::\n\n")

class DataNW(NodeWriter):
    """TODO"""

    def start(self, node):
        self.write('    %s = ' % node['name'])

    def child(self, node):
        data = ''
        for item in node.child:
            if item.name == '#cdata-section':
                data += item.data
        data = RE.sub(r'"\1"', data)
        data = RE2.sub(r'"\1"', data)
        data = RE3.sub(r'"\1"', data)
        data = RE4.sub(r'"\1"', data)
        data = json.dumps(
            eval(data), sort_keys=True, indent=4, separators=(',', ': ')
        )
        if node['name'] == 'MSG_EXPLANATION':
            data = data.replace("\\n", "\n")
            data = data.replace('"', '"""')
        self.write(data.replace('\n', '\n    '))
        self.write('\n\n')


MAPPING = {
    '#document': DocumentNW,
    '#text': TextNW,
    # '#entity': '#text',
    'module': ModuleNW,
    'doc': '#document',
    'info': InfoNW,
    '#cdata-section': CDataNW,
    '__default__': DefaultNW,
    'mapping': MappingNW,
    'imports': ImportsNW,
    'classes': ClassesNW,
    'functions': FunctionsNW,
    'class': ClassNW,
    'bases': BasesNW,
    'mro': MRONW,
    'method_block': MethodBlockNW,
    'member_block': MemberBlockNW,
    'data_block': DataBlockNW,
    'data': DataNW,
}
