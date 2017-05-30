from .todict import *
from .toxml import *


class Dyslexml:
    def __init__(self):
        self.toDict = todict.parse
        self.toXml = toxml.translate
