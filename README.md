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
