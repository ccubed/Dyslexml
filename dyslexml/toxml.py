import decimal
import xml.etree.ElementTree as ET
from fractions import Fraction


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
    if any([isinstance(thing, x) for x in [list, tuple, bytes, bytearray, set, frozenset]]):
        return _lists(thing, encoding)
    elif isinstance(thing, str):
        return _strs(thing, encoding)
    elif isinstance(thing, int):
        return _ints(thing)
    elif isinstance(thing, float):
        return _floats(thing)
    elif isinstance(thing, type(None)):
        return _nonetype(thing)
    elif isinstance(thing, bool):
        return _bools(thing)
    elif isinstance(thing, dict):
        return _dicts(thing, encoding)
    elif isinstance(thing, complex):
        return _complex(thing)
    elif isinstance(thing, Fraction):
        return _fractions(thing)
    elif isinstance(thing, decimal.Decimal):
        return _decimals(thing)


def _strs(thing, encoding):
    """
    Internal Method for turning Strings into an XML document.
    
    :param thing: the string
    :param encoding: the encoding for strings
    :return: string containing xml
    :rtype: str
    """
    root = ET.Element("Py_Object")
    build_subelement(root, thing, encoding)
    return ET.tostring(root, encoding="unicode")


def _lists(thing, encoding):
    """
    Internal Method for turning lists into an XML document.
    
    :param list thing: the list
    :param str encoding: the encoding for strings 
    :return: string containing xml
    :rtype: str
    """
    root = ET.Element("Py_Object")
    real_root = ET.SubElement(root, thing.__class__.__name__, attrib={"length": str(len(thing))})

    for item in thing:
        build_subelement(real_root, item, encoding)

    return ET.tostring(root, encoding="unicode")


def _ints(thing):
    """
    Internal Method for turning ints into an XML document.
    
    :param thing: the int
    :return: string containing xml
    :rtype: str
    """
    root = ET.Element("Py_Object")
    build_subelement(root, thing, None)
    return ET.tostring(root, encoding="unicode")


def _floats(thing):
    """
    Internal Method for turning floats into an XML document.
    
    :param thing: the float
    :return: string containing xml
    :rtype: str
    """
    root = ET.Element("Py_Object")
    build_subelement(root, thing, None)
    return ET.tostring(root, encoding="unicode")


def _nonetype(thing):
    """
    Internal Method for turning None into an XML document.

    :param thing: the NoneType
    :return: string containing xml
    :rtype: str
    """
    root = ET.Element("Py_Object")
    build_subelement(root, thing, None)
    return ET.tostring(root, encoding="unicode")


def _bools(thing):
    """
    Internal Method for turning booleans into an XML document.

    :param thing: the bool
    :return: string containing xml
    :rtype: str
    """
    root = ET.Element("Py_Object")
    build_subelement(root, thing, None)
    return ET.tostring(root, encoding="unicode")


def _dicts(thing, encoding):
    """
    Internal Method for turning dictionaries into an XML document.

    :param thing: the dict
    :return: string containing xml
    :rtype: str
    """
    root = ET.Element("Py_Object")

    master = ET.SubElement(root, "Dict", attrib={'pairs': str(len(thing.keys()))})

    for key in thing.keys():
        kv_pair_node = ET.SubElement(master, "Pair")
        key_node = ET.SubElement(kv_pair_node, "Key")
        build_subelement(key_node, key, encoding)
        value_node = ET.SubElement(kv_pair_node, "Value")
        build_subelement(value_node, thing[key], encoding)

    return ET.tostring(root, encoding="unicode")


def _complex(thing):
    """
    Internal Method for turning complex numbers into an XML document.

    :param thing: the complex object
    :return: string containing xml
    :rtype: str
    """
    root = ET.Element("Py_Object")
    build_subelement(root, thing, None)
    return ET.tostring(root, encoding="unicode")


def _fractions(thing):
    """
    Internal Method for turning fractions into an XML document.

    :param thing: the fraction object
    :return: string containing xml
    :rtype: str
    """
    root = ET.Element("Py_Object")
    build_subelement(root, thing, None)
    return ET.tostring(root, encoding="unicode")


def _decimals(thing):
    """
    Internal Method for turning decimals into an XML document.

    :param thing: the decimal object
    :return: string containing xml
    :rtype: str
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
    if any([isinstance(item, x) for x in [list, tuple, bytes, bytearray, set, frozenset]]):
        return _lists__se(root, item, encoding)
    elif isinstance(item, str):
        return _strs__se(root, item, encoding)
    elif isinstance(item, int):
        return _ints__se(root, item)
    elif isinstance(item, float):
        return _floats__se(root, item)
    elif isinstance(item, type(None)):
        return _nonetype__se(root)
    elif isinstance(item, bool):
        return _bools__se(root, item)
    elif isinstance(item, dict):
        return _dicts__se(root, item, encoding)
    elif isinstance(item, complex):
        return _complex__se(root, item)
    elif isinstance(item, Fraction):
        return _fractions__se(root, item)
    elif isinstance(item, decimal.Decimal):
        return _decimals__se(root, item)


def _lists__se(root, item, encoding):
    """
    list subelement factory
    
    :param root: root element
    :param item: the list
    :param encoding: encoding for strings
    :return: subelement
    :rtype: xml.etree.ElementTree.SubElement
    """
    subroot = ET.SubElement(root, "list", {'length': str(len(item))})

    for obj in item:
        build_subelement(subroot, obj, encoding)


def _strs__se(root, item, encoding):
    """
    string subelement factory.
    
    :param root: root element
    :param item: the string
    :param encoding: encoding for strings
    :return: xml.etree.ElementTree.SubElement
    """
    node = ET.SubElement(root, "Str", attrib={"length": str(len(item)), "encoding": encoding})
    node.text = ".".join([str(x) for x in item.encode(encoding=encoding, errors="strict")])


def _ints__se(root, item):
    """
    int subelement factory.
    
    :param root: root element
    :param item: the int
    :return: xml.etree.ElementTree.SubElement
    """
    node = ET.SubElement(root, "Int")
    node.text = str(item)


def _floats__se(root, item):
    """
    float subelement factory. This uses float.hex.
    
    :param root: root element
    :param item: the float
    :return: xml.etree.ElementTree.SubElement
    """
    node = ET.SubElement(root, "Float")
    node.text = item.hex()


def _nonetype__se(root):
    """
    None subelement factory.

    :param root: root element
    :return: xml.etree.ElementTree.SubElement
    """
    node = ET.SubElement(root, "None")


def _bools__se(root, item):
    """
    boolean subelement factory.

    :param root: root element
    :param item: the boolean
    :return: xml.etree.ElementTree.SubElement
    """
    node = ET.SubElement(root, "Bool")
    node.text = "0" if item else "1"


def _dicts__se(root, item, encoding):
    """
    dictionary subelement factory.

    :param root: root element
    :param item: the dictionary
    :return: xml.etree.ElementTree.SubElement
    """
    subroot_node = ET.SubElement(root, "Dict", attrib={'pairs': str(len(item.keys()))})

    for key in item.keys():
        kv_pair_node = ET.SubElement(subroot_node, "Pair")
        key_node = ET.SubElement(kv_pair_node, "Key")
        build_subelement(key_node, key, encoding)
        value_node = ET.SubElement(kv_pair_node, "Value")
        build_subelement(value_node, item[key], encoding)


def _complex__se(root, item):
    """
    complex object subelement factory.

    :param root: root element
    :param item: the complex number object
    :return: xml.etree.ElementTree.SubElement
    """
    node = ET.SubElement(root, "Complex")
    real = ET.SubElement(node, "Real")
    real.text = item.real.hex()
    imag = ET.SubElement(node, "Imaginary")
    imag.text = item.imag.hex()


def _fractions__se(root, item):
    """
    fraction subelement factory.

    :param root: root element
    :param item: the fraction
    :return: xml.etree.ElementTree.SubElement
    """
    node = ET.SubElement(root, "Fraction")
    numerator = ET.SubElement(node, "Numerator")
    numerator.text = str(item.numerator)
    denominator = ET.SubElement(node, "Denominator")
    denominator.text = str(item.denominator)


def _decimals__se(root, item):
    """
    Decimal subelement factory.

    :param root: root element
    :param item: the decimal
    :return: xml.etree.ElementTree.SubElement
    """
    node = ET.SubElement(root, "Decimal")

    context_node = ET.SubElement(node, "Context")
    precision = ET.SubElement(context_node, "Precision")
    precision.text = str(decimal.getcontext().prec)
    rounding = ET.SubElement(context_node, "Rounding")
    rounding.text = decimal.getcontext().rounding
    emin = ET.SubElement(context_node, "EMin")
    emin.text = str(decimal.getcontext().Emin)
    emax = ET.SubElement(context_node, "EMax")
    emax.text = str(decimal.getcontext().Emax)

    data = item.as_tuple()

    number_node = ET.SubElement(node, "Data")
    sign = ET.SubElement(number_node, "Sign")
    digits = ET.SubElement(number_node, "Digits")
    exponent = ET.SubElement(number_node, "Exponent")
    sign.text = str(data.sign)
    exponent.text = str(data.exponent)

    build_subelement(digits, data.digits, None)