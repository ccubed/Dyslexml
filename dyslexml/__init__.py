import .todict
import .toxml
import .toobject

class Dyslexml:
    def __init__(self):
        self.toDict = todict.parse
        self.toXml = toxml.translate
        #self.toObject =
