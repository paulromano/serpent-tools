.. |homogUniv| replace:: :py:class:`~serpentTools.objects.containers.HomogUniv`

.. _changelog:

*********
Changelog
*********

.. _vNext:

Next
====

* :pull:`131` Updated variable groups between ``2.1.29`` and ``2.1.30`` - include
  poison cross section, kinetic parameters, six factor formula (2.1.30 exclusive),
  and minor differences
* :pull:`141` - Setting :ref:`xs-reshapeScatter` can be used to reshape scatter
  matrices on |homogUniv|
  objects to square matrices
* :pull:`145` - :py:meth:`~serpentTools.objects.containers.HomogUniv.hasData` 
  added to check if |homogUniv| 
  objects have any data stored on them
* :pull:`146` - |homogUniv| object
  stores group structure on the object. New dictionaries for storing group constant
  data that is not ``INF`` nor ``B1`` - 
  :py:attr:`~serpentTools.objects.containers.HomogUniv.gc` and 
  :py:attr:`~serpentTools.objects.containers.HomogUniv.gcUnc` 
* :pull:`130` Added the ability to read results file
* :pull:`149` - Add the ability to read sensitivity files
   
.. _vAPI-changes:

API Changes
-----------

* :pull:`146` removed ``metadata`` dictionaries on |homogUniv| objects.

.. _vDeprecated:

Deprecation
-----------

* Variable group ``xs-yields`` will be removed. Use ``poisons`` instead
* Branches of a single name will only be accessible through 
  ``branches['nom']``, not ``branches[('nom'), ]`` as per :pull:`114`

.. _v0.4.0:

:release-tag:`0.4.0`
====================

* :pull:`95` Add ``xsplot`` file reader
* :pull:`121` Samplers will raise more warnings/errors if no files are loaded
  from ``*`` wildcards
* :pull:`122` Better detector labeling
* :pull:`135` Added instructions for better converting Jupyter notebooks to 
  ``.rst`` files. Plotting guidelines

.. _v0.3.1:

:release-tag:`0.3.1`
====================

* :pull:`118` - Support for ``SERPENT`` 2.1.30
* :issue:`119` - SampledDepletedMaterial now respects the value of `xUnits` 
  - :pull:`120`
* :pull:`114` - Standalone branches in the coefficient files are stored
  and accessed using a single string, rather than a single-entry tuple
  ``branches['myBranch']`` vs. ``branches[('myBranch', )]``

    
.. _v0.3.0:

:release-tag:`0.3.0`
====================

* :pull:`109` - Capability to read history files
* :pull:`107` - DepletionReader can now plot data for some or all materials

.. _v0.2.2:

:release-tag:`0.2.2`
====================

* :pull:`82` - Command line interface and some sub-commands
* :pull:`88` - Pre- and post-check methods for readers
* :pull:`93` - Detector and Depletion Samplers
* :pull:`96` - Better mesh plotting for detector
* :issue:`99` - Negative universe burnup with branching reader - :pull:`100`
* :py:attr:`serpentTools.objects.containers.Detector.indexes` are now zero-indexed
* The PDF manual is no longer tracked in this repository

