.. _readthedocs.org: http://www.readthedocs.org
.. _sphinx_rtd_theme: https://github.com/snide/sphinx_rtd_theme
.. _bower: http://www.bower.io
.. _sphinx: http://www.sphinx-doc.org
.. _compass: http://www.compass-style.org
.. _sass: http://www.sass-lang.com
.. _wyrm: http://www.github.com/snide/wyrm/
.. _grunt: http://www.gruntjs.com
.. _node: http://www.nodejs.com
.. _demo: http://docs.readthedocs.org
.. _hidden: http://sphinx-doc.org/markup/toctree.html

****************
Lexor Lang Theme
****************

The contents in this directory are a modification of the
sphinx_rtd_theme_ project. Please check the original source for the
original README file. The content that follows has been modified from
its original source to reflect how the read the docs theme is used in
this project. This directory is mainly concern with the modification
of the theme, in other words, the objective of this directory is to
obtain the css files that will be used.

Set up your environment
-----------------------

1. Install sphinx_ into a virtual environment::

    pip install sphinx

2. Install sass::

    gem install sass

2. Install node, bower and grunt::

    // Install node
    brew install node

    // Install bower and grunt
    npm install -g bower grunt-cli

    // Install the theme dependecies.
    npm install

Now that our environment is set up, make sure you're in your virtual
environment, go to this repository in your terminal and run grunt::

    grunt

This default task will do the following **very cool things that make
it worth the trouble**.

1. It'll install and update any bower dependencies.
2. It'll run sphinx and build new docs.
3. It'll watch for changes to the sass files and build css from the
   changes.
4. It'll rebuild the sphinx docs anytime it notices a change to .rst,
   .html, .js or .css files.
