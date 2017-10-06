from serpentTools.settings import rc


class BaseReader(object):
    """Parent class from which all parsers will inherit.

    Parameters
    ----------
    filePath: str
        path pointing towards the file to be read
    readerSettingsLevel: str
        type of reader. Determines which settings to obtain
    """

    def __init__(self, filePath, readerSettingsLevel):
        self.filePath = filePath
        self.metadata = {}
        self.settings = rc.getReaderSettings(readerSettingsLevel)

    def __repr__(self):
        return '<{} reading {}>'.format(self.__class__.__name__, self.filePath)

    def read(self):
        """Read the file and store the data.

        :note:

          This must be overwritten by each subclass of parser

        """
        raise NotImplementedError


class MaterialReader(BaseReader):
    """Parent class for files that store materials."""

    def __init__(self, filePath, readerSettingsLevel):
        BaseReader.__init__(self, filePath, readerSettingsLevel)
        self.materials = {}

    def read(self):
        raise NotImplementedError