import io
import xml.etree.ElementTree as ET


def translate(thing, encoding="utf-8"):
    """
    Given an object, make a corresponding xml document that represents that
    python object. Str types are converted to their byte equivalents
    to preserve their contents over transitions between document and object.

    :param thing: Some python object
    :param str encoding: Encoding for strings
    :return: A str containing the XML document
    :rtype: str
    """
    if isinstance(thing, list):
        return _lists(thing, encoding)
    elif isinstance(thing, str):
        return _strs(thing, encoding)
    elif isinstance(thing, int):
        return _ints(thing)
    elif isinstance(thing, float):
        return _floats(thing)



def _strs(thing, encoding):
    """
    
    :param thing: 
    :param encoding: 
    :return: 
    """
    root = ET.Element("Py_Object")
    build_subelement(root, thing, encoding)
    return ET.tostring(root, encoding="unicode")


def _lists(thing, encoding):
    """
    Internal Method for turning lists in an XML document.
    
    :param list thing: the list
    :param str encoding: the encoding for strings 
    :return: string containing xml
    :rtype: str
    """
    root = ET.Element("Py_Object")
    real_root = ET.SubElement(root, "list", attrib={"length": str(len(thing))})

    for item in thing:
        build_subelement(real_root, item, encoding)

    return ET.tostring(root, encoding="unicode")


def _ints(thing):
    """
    
    :param thing: 
    :return: 
    """
    root = ET.Element("Py_Object")
    build_subelement(root, thing, None)
    return ET.tostring(root, encoding="unicode")


def _floats(thing):
    """
    
    :param thing: 
    :return: 
    """
    root = ET.Element("Py_Object")
    build_subelement(root, thing, None)
    return ET.tostring(root, encoding="unicode")


def build_subelement(root, item, encoding):
    """
    Internal subelement factory method.
    
    :param root: root element
    :param item: some object 
    :param encoding: encoding for strings
    :return: subelement
    :rtype: xml.etree.ElementTree.SubElement
    """
    if isinstance(item, list):
        return _lists__se(root, item, encoding)
    elif isinstance(item, str):
        return _strs__se(root, item, encoding)
    elif isinstance(item, int):
        return _ints__se(root, item)
    elif isinstance(item, float):
        return _floats__se(root, item)


def _lists__se(root, item, encoding):
    """
    
    :param root: root element
    :param item: some python object
    :param encoding: encoding for strings
    :return: 
    """
    subroot = ET.SubElement(root, "list", {'length': str(len(item))})

    for obj in item:
        build_subelement(subroot, obj, encoding)


def _strs__se(root, item, encoding):
    """
    
    :param root: 
    :param item: 
    :param encoding: 
    :return: 
    """
    node = ET.SubElement(root, "Str", attrib={"length": str(len(item)), "encoding": encoding})
    node.text = ".".join([str(x) for x in item.encode(encoding=encoding, errors="strict")])


def _ints__se(root, item):
    """
    
    :param root: 
    :param item: 
    :return: 
    """
    node = ET.SubElement(root, "Int")
    node.text = str(item)


def _floats__se(root, item):
    """
    
    :param root: 
    :param item: 
    :return: 
    """
    node = ET.SubElement(root, "Float")
    node.text = item.hex()