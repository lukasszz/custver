"""
    Based on sphinx.ext.ifconfig

    Provides the ``custver`` directive that allows to write documentation
    and the generate different content depending on configuration variables.


    Usage::

        1. Include  section for certain clients
        General remarks.

        .. custver::  client in ('Company A', 'Company B')

           This stuff is only included for client 'Company A', 'Company B'

        2. Include  section for everyone except certain clients
        General remarks.

        .. custver::  client not in ('Company B')

           This stuff is included for everyone beside 'Company B'


        3. Include the whole article for certain clients
         .. toctree::

            MOD/description.rst

        .. custver:: client in ('Company A')

            .. toctree::

                MOD/dedicated.rst


    The argument for ``custver`` is a plain Python expression, evaluated in the
    namespace of the project configuration (that is, all variables from
    ``conf.py`` are available.)
    However this extension provides dedicated variable: client. If it is set tu **None**
    then Sphinx will generate the documentation with information when specific section will be included.

    :license: MIT, see LICENSE for details.
"""

from docutils import nodes
from docutils.parsers.rst import Directive

import sphinx
from sphinx.util.nodes import set_source_info

if False:
    # For type annotation
    from typing import Any, Dict, List  # NOQA
    from sphinx.application import Sphinx  # NOQA


class custver(nodes.Element):
    pass


class CustVer(Directive):
    has_content = True
    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = True
    option_spec = {}  # type: Dict

    def run(self):
        # type: () -> List[nodes.Node]
        node = custver()
        node.document = self.state.document
        set_source_info(self, node)
        node['expr'] = self.arguments[0]
        self.state.nested_parse(self.content, self.content_offset,
                                node, match_titles=1)
        return [node]


def process_custver_nodes(app, doctree, docname):
    # type: (Sphinx, nodes.Node, unicode) -> None
    ns = dict((confval.name, confval.value) for confval in app.config)  # type: ignore
    ns.update(app.config.__dict__.copy())
    ns['builder'] = app.builder.name

    for node in doctree.traverse(custver):
        if app.config['client'] is None:
            newnode = nodes.subscript('', node['expr'])

            node.parent.append(newnode)

            for n in node.children:
                node.parent.append(n)
            node.replace_self([])
            continue

        try:
            res = eval(node['expr'], ns)
        except Exception as err:
            # handle exceptions in a clean fashion
            from traceback import format_exception_only
            msg = ''.join(format_exception_only(err.__class__, err))
            newnode = doctree.reporter.error('Exception occured in '
                                             'custver expression: \n%s' %
                                             msg, base_node=node)
            node.replace_self(newnode)
        else:
            if not res:
                node.replace_self([])
            else:
                node.replace_self(node.children)


def setup(app):
    # type: (Sphinx) -> Dict[unicode, Any]
    app.add_node(custver)
    app.add_directive('custver', CustVer)
    app.connect('doctree-resolved', process_custver_nodes)
    app.add_config_value('client', None, True)
    return {'version': sphinx.__display_version__, 'parallel_read_safe': True}
