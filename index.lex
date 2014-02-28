%%!DOCTYPE html%%
%%{html}
%%{head}
    %%{title}Lexor Languages%%
%%%%{body}

Lexor Languages
===============

<?python
import os
mod = import_module('python/web_module')
lang = mod.read_style_urls('%s/lexor-lang.url' % __DIR__)
node = mod.make_lang_node(lang)
echo(node)
?>

%%%%
