"""Classes for storing material data."""

import numpy
from matplotlib import pyplot

from serpentTools import messages
from serpentTools.objects import NamedObject, convertVariableName


class DepletedMaterial(NamedObject):
    """
    Class for storing material data from ``_dep.m`` files.

    Parameters
    ----------
    parser: :py:class:`~serpentTools.parsers.depletion.DepletionReader`
        Parser that found this material.
        Used to obtain file metadata like isotope names and burnup
    name: str
        Name of this material

    Attributes
    ----------
    zai: numpy.array or None
        Isotope id's
    names: numpy.array or None
        Names of isotopes
    days: numpy.array or None
        Days over which the material was depleted
    adens: numpy.array or None
        Atomic density over time for each nuclide
    mdens: numpy.array or None
        Mass density over time for each nuclide
    burnup: numpy.array or None
        Burnup of the material over time

    """

    def __init__(self, parser, name):
        NamedObject.__init__(self, name)
        self.data = {}
        self.zai = parser.metadata.get('zai', None)
        self.names = parser.metadata.get('names', None)
        self.days = parser.metadata.get('days', None)
        self.filePath = parser.filePath
        self.__burnup = None
        self.__adens = None
        self.__mdens = None

    def __getitem__(self, item):
        if item not in self.data:
            raise KeyError('Key {} not found on material {}'
                           .format(item, self.name))
        return self.data[item]

    @property
    def burnup(self):
        if 'burnup' not in self.data:
            raise AttributeError('Burnup for material {} has not been loaded'
                                 .format(self.name))
        if self.__burnup is None:
            self.__burnup = self.data['burnup']
        return self.__burnup

    @property
    def adens(self):
        if 'adens' not in self.data:
            raise AttributeError('Atomic densities for material {} have not '
                                 'been loaded'.format(self.name))
        if self.__adens is None:
            self.__adens = self.data['adens']
        return self.__adens

    @property
    def mdens(self):
        if 'mdens' not in self.data:
            raise AttributeError('Mass densities for material {} has not been '
                                 'loaded'.format(self.name))
        if self.__mdens is None:
            self.__mdens = self.data['mdens']
        return self.__mdens

    def addData(self, variable, rawData):
        """
        Add data straight from the file onto a variable.

        Parameters
        ----------
        variable: str
            Name of the variable directly from ``SERPENT``
        rawData: list
            List of strings corresponding to the raw data from the file
        """
        newName = convertVariableName(variable)
        messages.debug('Adding {} data to {}'.format(newName, self.name))
        if isinstance(rawData, str):
            scratch = [float(item) for item in rawData.split()]
        else:
            scratch = []
            for line in rawData:
                if line:
                    scratch.append([float(item) for item in line.split()])
        self.data[newName] = numpy.array(scratch)

    def getValues(self, xUnits, yUnits, timePoints=None, names=None):
        """
        Return material variable data at specified time points and isotopes

        If the quantity ``yUnits`` corresponds to a vector in the ``data``
        dictionary, e.g. ``burnup`` or ``volume``, and not something that
        varies by isotope, then ``names`` does not have to be given

        Parameters
        ----------
        xUnits: str
            name of x value to obtain, e.g. ``'days'``, ``'burnup'``
        yUnits: str
            name of y value to return, e.g. ``'adens'``, ``'burnup'``
        timePoints: list or None
            If given, select the time points according to those specified here.
            Otherwise, select all points
        names: list or None
            If given, return y values corresponding to these isotope names.
            Otherwise, return values for all isotopes.

        Returns
        -------
        numpy.array
            Array of values.

        Raises
        ------
        AttributeError
            If the names of the isotopes have not been obtained and specific
            isotopes have been requested
        KeyError
            If at least one of the days requested is not present
        """
        if timePoints is not None:
            timeCheck = self._checkTimePoints(xUnits, timePoints)
            if any(timeCheck):
                raise KeyError('The following times were not present in file'
                               '{}\n{}'.format(self.filePath,
                                               ', '.join(timeCheck)))
        if names and self.names is None:
            raise AttributeError(
                'Isotope names not stored on DepletedMaterial '
                '{}.'.format(self.name))
        colIndices = self._getColIndices(xUnits, timePoints)
        allY = self.data[yUnits]
        if allY.shape[0] == 1 or len(allY.shape) == 1:  # vector
            yVals = allY[colIndices]
            return yVals
        rowIndices = self._getRowIndices(names)
        return allY[:, colIndices][rowIndices]

    def _checkTimePoints(self, xUnits, timePoints):
        """Return a list of all requested points in time not stored."""
        valid = self.days if xUnits == 'days' else self.data[xUnits]
        badPoints = [str(time) for time in timePoints if time not in valid]
        return badPoints

    def _getColIndices(self, xUnits, timePoints):
        """Return row and column indices corresponding to isotopes and times"""
        allX = self.days if xUnits == 'days' else self.data[xUnits]
        if timePoints is None:
            return numpy.arange(len(allX), dtype=int)
        colIndices = [indx for indx, xx in enumerate(allX) if xx in timePoints]
        return colIndices

    def _getRowIndices(self, isotopes):
        """
        Return the indices in ``names`` that correspond to specific isotopes.
        """
        if not isotopes:
            return numpy.arange(len(self.names), dtype=int)
        isoList = [isotopes] if isinstance(isotopes, (str, int)) else isotopes
        rowIDs = numpy.empty_like(isoList, dtype=int)
        for indx, isotope in enumerate(isoList):
            rowIDs[indx] = self.names.index(isotope)
        return rowIDs

    def plot(self, xUnits, yUnits, timePoints=None, names=None, ax=None,
             legend=True, label=True, xlabel=None, ylabel=None):
        """
        Plot some data as a function of time for some or all isotopes.

        Parameters
        ----------
        xUnits: str
            name of x value to obtain, e.g. ``'days'``, ``'burnup'``
        yUnits: str
            name of y value to return, e.g. ``'adens'``, ``'burnup'``
        timePoints: list or None
            If given, select the time points according to those
            specified here. Otherwise, select all points
        names: list or None
            If given, return y values corresponding to these isotope
            names. Otherwise, return values for all isotopes.
        ax: None or matplotlib.pyplot.axes
            If given, add the data to this plot.
            Otherwise, create a new plot
        legend: bool
            Automatically add the legend
        label: bool
            Automatically label the axis
        xlabel: None or str
            If given, use this as the label for the x-axis.
            Otherwise, use xUnits
        ylabel: None or str
            If given, use this as the label for the y-axis.
            Otherwise, use yUnits

        Returns
        -------
        matplotlib.pyplot.axes
            Axes corresponding to the figure that was plotted

        See Also
        --------
        :py:func:`~serpentTools.objects.materials.DepletedMaterial.getValues`

        """
        xVals = timePoints or self.days
        yVals = self.getValues(xUnits, yUnits, xVals, names)
        ax = ax or pyplot.axes()
        labels = names or ['']
        for row in range(yVals.shape[0]):
            ax.plot(xVals, yVals[row], label=labels[row])

        # format the plot
        if legend:
            ax.legend()
        if label:
            ax.set_xlabel(xlabel or xUnits)
            ax.set_ylabel(ylabel or yUnits)
        return ax
