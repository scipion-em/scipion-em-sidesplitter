===================
SIDESPLITTER plugin
===================

This plugin provide wrappers around `SIDESPLITTER <https://github.com/StructuralBiology-ICLMedicine/SIDESPLITTER>`_ program for mitigating local overfitting.

+------------------+------------------+
| stable: |stable| | devel: | |devel| |
+------------------+------------------+

.. |stable| image:: http://scipion-test.cnb.csic.es:9980/badges/sidesplitter_prod.svg
.. |devel| image:: http://scipion-test.cnb.csic.es:9980/badges/sidesplitter_sdevel.svg


Installation
------------

You will need to use `3.0 <https://github.com/I2PC/scipion/releases/tag/V3.0.0>`_ version of Scipion to be able to run these protocols. To install the plugin, you have two options:

a) Stable version

.. code-block::

    scipion installp -p scipion-em-sidesplitter

b) Developer's version

    * download repository

    .. code-block::

        git clone https://github.com/scipion-em/scipion-em-sidesplitter.git

    * install

    .. code-block::

        scipion installp -p path_to_scipion-em-sidesplitter --devel

SIDESPLITTER sources will be installed automatically with the plugin, but you can also link an existing installation.

    * Default installation path assumed is ``software/em/sidesplitter-1.0``, if you want to change it, set *SIDESPLITTER_HOME* in ``scipion.conf`` file pointing to the folder where the SIDESPLITTER is installed.

To check the installation, simply run one of the following Scipion tests:

.. code-block::

   scipion test sidesplitter.tests.test_protocol_sidesplitter.TestSideSplitter

A complete list of tests can also be seen by executing ``scipion test --show --grep sidesplitter``

Supported versions
------------------

1.0

Protocols
---------

* local filter

References
----------

1. Kailash Ramlaul, Colin M. Palmer and Christopher H. S. Aylett (2020). Mitigating Local Over-fitting During Single Particle Reconstruction with SIDESPLITTER. https://www.biorxiv.org/content/10.1101/2019.12.12.874081v2
