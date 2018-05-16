"""Test the container object. """

import unittest
from itertools import product

from six import iteritems
from numpy import array, arange
from numpy.testing import assert_allclose

from serpentTools.settings import rc
from serpentTools.objects.containers import HomogUniv
from serpentTools.parsers import DepletionReader

NUM_GROUPS = 5


class _HomogUnivTestHelper(unittest.TestCase):
    """Class that runs the tests for the two sub-classes
    
    Subclasses will differ in how the ``mat`` data
    is arranged. For one case, the ``mat`` will be a 
    2D matrix.
    """

    def setUp(self):
        self.univ, vec, mat = self.getParams()
        # Data definition
        rawData = {'B1_1': vec, 'B1_AS_LIST': list(range(NUM_GROUPS)),
                  'INF_1': vec, 'INF_S0': mat}
        meta = {'MACRO_E': vec}
        # Partial dictionaries
        self.b1Unc = self.b1Exp = {'b11': vec}
        self.infUnc = self.infExp = {'inf1': vec, 'infS0': mat}
        self.meta = {'macroE': vec}

        # Use addData
        for key, value in iteritems(rawData):
            self.univ.addData(key, value, uncertainty=False)
            self.univ.addData(key, value, uncertainty=True)
        for key, value in iteritems(meta):
            self.univ.addData(key, value)

    def test_getB1Exp(self):
        """ Get Expected vales from B1 dictionary"""
        d = {}
        # Comparison
        for kk in self.univ.b1Exp:
            d[kk] = self.univ.get(kk, False)
        compareDictOfArrays(self.b1Exp, d, 'b1 values')
        
    def test_getB1Unc(self):
        """ Get Expected vales and associated uncertainties from B1 dictionary
        """
        d = {}
        # Comparison
        for kk in self.univ.b1Exp:
            d[kk] = self.univ.get(kk, True)[1]
        compareDictOfArrays(self.b1Unc, d, 'b1 uncertainties')

    def test_getInfExp(self):
        """ Get Expected vales from Inf dictionary"""
        d = {}
        # Comparison
        for kk in self.univ.infExp:
            d[kk] = self.univ.get(kk, False)
        compareDictOfArrays(self.infExp, d, 'infinite values')

    def test_getInfUnc(self):
        """ Get Expected vales and associated uncertainties from Inf dictionary
        """
        d = {}
        # Comparison
        for kk in self.univ.infUnc:
            d[kk] = self.univ.get(kk, True)[1]
        compareDictOfArrays(self.infUnc, d, 'infinite uncertainties')

    def test_getMeta(self):
        """ Get metaData from corresponding dictionary"""
        d = {}
        # Comparison
        for kk in self.univ.metadata:
            d[kk] = self.univ.get(kk, False)
        compareDictOfArrays(self.meta, d, 'metadata')

    def test_getBothInf(self):
        """
        Verify that the value and the uncertainty are returned if the
        flag is passed.
        """
        expected, uncertainties = {}, {}
        for key in self.infExp.keys():
            value, unc = self.univ.get(key, True)
            expected[key] = value
            uncertainties[key] = unc
        compareDictOfArrays(self.infExp, expected, 'infinite values')
        compareDictOfArrays(self.infUnc, uncertainties, 
                            'infinite uncertainties')


class VectoredHomogUnivTester(_HomogUnivTestHelper):
    """Class for testing HomogUniv that does not reshape scatter matrices"""

    def getParams(self):
        univ, vec, mat = getParams()
        self.assertFalse(univ.reshaped)
        return univ, vec, mat


class ReshapedHomogUnivTester(_HomogUnivTestHelper):
    """Class for testing HomogUniv that does reshape scatter matrices"""

    def getParams(self):
        from serpentTools.settings import rc
        with rc:
            rc.setValue('xs.reshapeScatter', True)
            univ, vec, mat = getParams()
            univ.numGroups = NUM_GROUPS
            self.assertTrue(univ.reshaped)
        return univ, vec, mat.reshape(NUM_GROUPS, NUM_GROUPS)


def getParams():
    """Return the universe, vector, and matrix for testing."""
    univ = HomogUniv(300, 0, 0, 0)
    vec = arange(NUM_GROUPS)
    mat = arange(NUM_GROUPS ** 2)
    return univ, vec, mat


def compareDictOfArrays(expected, actualDict, dataType):
    for key, value in iteritems(expected):
        actual = actualDict[key]
        assert_allclose(value, actual, 
                err_msg="Error in {} dictionary: key={}"
                .format(dataType, key))

del _HomogUnivTestHelper

class UnivTruthTester(unittest.TestCase):
    """Class that tests the various boolean evaluations for HomogUniv"""

    def setUp(self):
        """Verify that an empty universe evalutes to False."""
        self.assertFalse(self.getUniv())

    def test_loadedUnivTrue(self):
        """Verify that universes with some data evalue to True."""
        keys = {"INF_TOT", "B1_TOT", "CMM_TRANSP_X"}
        data = arange(NUM_GROUPS)
        for uflag, key in product((True, False), keys):
            univ = self.getUniv()
            univ.addData(key, data, uflag)
            self.evalUniv(univ, msg="Key = {}, Uflag={}".format(key, uflag))
        univ = self.getUniv()
        univ.addData("MACRO_E", data)
        self.evalUniv(univ, msg="Key = MACRO_E")

    @staticmethod
    def getUniv():
        return HomogUniv('truth', 0, 0, 0)

    def evalUniv(self, univ, msg):
        """Shortcut for testing the truth of a universe."""
        self.assertTrue(univ, msg=msg)
        self.assertTrue(univ.hasData, msg=msg)



if __name__ == '__main__':
    unittest.main()
