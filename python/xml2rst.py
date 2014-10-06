"""
Change the lexor xml language files to a valid rst file.

"""
import os.path as pth
from glob import iglob
import lexor
import lexor.core.elements as core

PY_DIR = pth.dirname(pth.abspath(__file__)) 
LANG_DIR = pth.abspath(pth.join(PY_DIR, '..', 'lang')) 

styles = [x for x in iglob(pth.join(LANG_DIR, '*'))]
for style_file in styles[0:1]:
    doc, lang = lexor.read(style_file)
    print repr(doc)

