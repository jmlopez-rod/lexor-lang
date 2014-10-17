"""
Change the lexor xml language files to a valid rst file.

"""
import os.path as pth
from glob import iglob
import lexor
import lexor.core.elements as core

PY_DIR = pth.dirname(pth.abspath(__file__)) 
LANG_DIR = pth.abspath(pth.join(PY_DIR, '..', 'lang')) 

types = {
    'parser': [],
    'converter': [],
    'writer': [],
}
styles = [x for x in iglob(pth.join(LANG_DIR, '*'))]
for style_file in styles:
    name = pth.basename(style_file).split('-')[0]
    tmp = name.split('.')
    if len(tmp) == 4:
        lang = tmp[1]
        type_ = tmp[2]
        style = tmp[3]
        types[type_].append((lang, style))
    else:
        lang = tmp[1]
        type_ = tmp[2]
        to_lang = tmp[3]
        style = tmp[4]
        types[type_].append((lang, to_lang, style))
    if type_ != 'converter':
        filename = '../source/%s-%s-%s.rst' % (lang, type_, style)
    else:
        filename = '../source/%s-%s-%s-%s.rst' % (
            lang, type_, to_lang, style
        ) 
    doc, lang = lexor.read(style_file)
    doc.style = 'rst'
    print 'writing ', filename
    lexor.write(doc, filename)

with open("../source/index.rst", 'w') as fp:
    fp.write('Lexor Language Styles\n')
    fp.write('=====================\n\n')
    fp.write("Parsers\n")
    fp.write("-------\n\n")
    fp.write('.. toctree::\n')
    fp.write('   :maxdepth: 1\n\n')
    msg = '    {lang}: {style} <{lang}-parser-{style}>\n'
    for item in types['parser']:
        fp.write(msg.format(lang=item[0], style=item[1]))
    fp.write("\n")
    fp.write("Converters\n")
    fp.write("----------\n\n")
    fp.write('.. toctree::\n')
    fp.write('   :maxdepth: 1\n\n')
    msg = '    {lang} to {lang_to}: {style} <{lang}-converter-{lang_to}-{style}>\n'
    for item in types['converter']:
        fp.write(msg.format(lang=item[0], lang_to=item[1], style=item[2]))
    fp.write("\n")
    fp.write("Writers\n")
    fp.write("-------\n\n")
    fp.write('.. toctree::\n')
    fp.write('   :maxdepth: 1\n\n')
    msg = '    {lang}: {style} <{lang}-writer-{style}>\n'
    for item in types['writer']:
        fp.write(msg.format(lang=item[0], style=item[1]))
    fp.write("\n")

