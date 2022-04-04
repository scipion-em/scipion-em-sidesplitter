===================
SIDESPLITTER plugin
===================

This plugin provides a wrapper for `SIDESPLITTER <https://github.com/StructuralBiology-ICLMedicine/SIDESPLITTER>`_ program for mitigating local overfitting.

.. image:: https://img.shields.io/pypi/v/scipion-em-sidesplitter.svg
        :target: https://pypi.python.org/pypi/scipion-em-sidesplitter
        :alt: PyPI release

.. image:: https://img.shields.io/pypi/l/scipion-em-sidesplitter.svg
        :target: https://pypi.python.org/pypi/scipion-em-sidesplitter
        :alt: License

.. image:: https://img.shields.io/pypi/pyversions/scipion-em-sidesplitter.svg
        :target: https://pypi.python.org/pypi/scipion-em-sidesplitter
        :alt: Supported Python versions

.. image:: https://img.shields.io/sonar/quality_gate/scipion-em_scipion-em-sidesplitter?server=https%3A%2F%2Fsonarcloud.io
        :target: https://sonarcloud.io/dashboard?id=scipion-em_scipion-em-sidesplitter
        :alt: SonarCloud quality gate

.. image:: https://img.shields.io/pypi/dm/scipion-em-sidesplitter
        :target: https://pypi.python.org/pypi/scipion-em-sidesplitter
        :alt: Downloads

Installation
------------

You will need to use 3.0+ version of Scipion to be able to run these protocols. To install the plugin, you have two options:

a) Stable version

.. code-block::

    scipion installp -p scipion-em-sidesplitter

b) Developer's version

    * download repository

    .. code-block::

        git clone https://github.com/scipion-em/scipion-em-sidesplitter.git

    * install

    .. code-block::

        scipion installp -p /path/to/scipion-em-sidesplitter --devel

SIDESPLITTER sources will be installed automatically with the plugin, but you can also link an existing installation.

    * Default installation path assumed is ``software/em/sidesplitter-1.2``, if you want to change it, set *SIDESPLITTER_HOME* in ``scipion.conf`` file pointing to the folder where the SIDESPLITTER is installed.

To check the installation, simply run one of the following Scipion tests:

.. code-block::

   scipion test sidesplitter.tests.test_protocol_sidesplitter.TestSideSplitter

A complete list of tests can also be seen by executing ``scipion test --show --grep sidesplitter``

Supported versions
------------------

1.2

Protocols
---------

* local filter

References
----------

1. Kailash Ramlaul, Colin M. Palmer and Christopher H. S. Aylett (2020). Mitigating Local Over-fitting During Single Particle Reconstruction with SIDESPLITTER. https://www.biorxiv.org/content/10.1101/2019.12.12.874081v2
