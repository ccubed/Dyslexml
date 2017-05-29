import io
import xml.etree.ElementTree as ET


def parse(data):
    """
    Given a file like object or xml string, return a dictionary.

    :param data: File like object or xml string
    :return: Parsed XML as Dictionary
    :rtype: dict
    """
    if isinstance(data, str):
        return __parse(ET.fromstring(data))
    elif isinstance(data, io.IOBase):
        return __parse(ET.fromstring(data.read()))
    else:
        raise TypeError("Dyslexml requires a string or file like object.")


def __parse(root):
    """
    Parse an XML document into a resulting dictionary.

    :param root: The ElementTree Instance
    :return: The Root Element
    :rtype: dict
    """
    if isinstance(root, ET.Element):
        base = root
    else:
        base = root.getroot()

    result = {base.tag: {'type': 'root', 'children': {}, 'attributes': None}}

    if base.attrib:
        result[base.tag]['attributes'] = {}
        for item in base.attrib:
            result[base.tag]['attributes'][item] = base.attrib[item]

    for child in base:
        child_element = build_child(child)
        result[base.tag]['children'][child.tag] = child_element[child.tag]

    return result


def build_child(element):
    """
    Build a resulting child object given the child element.

    :param element: An XML element
    :return: The Child Element
    :rtype: dict
    """
    child_object = {
        element.tag: {'type': 'child', 'children': None, 'attributes': None, 'value': element.text.strip() or None}}

    if element.attrib:
        child_object[element.tag]['attributes'] = {}
        for item in element.attrib:
            if "{" in item:
                child_object[element.tag]['attributes'][item.split("}")[1]] = element.attrib[item]
            else:
                child_object[element.tag]['attributes'][item] = element.attrib[item]

    for child in element:
        add_child(build_child(child), child_object, element.tag)

    return child_object


def add_child(child, dictionary, root_tag):
    """
    Adding a child has some complication to it because we have to dynamically
    change data types in the resulting dictionary depending on the amount of each
    child. That's in addition to building the child object.

    :param child: The parsed Child object from an XML element
    :param dict dictionary: The dictionary so far
    :param str root_tag: The name of the root element
    :return: None
    :rtype: NoneType
    """
    if not dictionary[root_tag]['children']:
        dictionary[root_tag]['children'] = {}
        dictionary[root_tag]['children'][list(child.keys())[0]] = child[list(child.keys())[0]]
    else:
        if list(child.keys())[0] in dictionary[root_tag]['children']:
            if dictionary[root_tag]['children'][list(child.keys())[0]].get('type', None) == "node":
                dictionary[root_tag]['children'][list(child.keys())[0]]['children'].append(child[list(child.keys())[0]])
            else:
                dictionary[root_tag]['children'][list(child.keys())[0]] = {'type': 'node', 'children': [
                    dictionary[root_tag]['children'][list(child.keys())[0]], child[list(child.keys())[0]]]}
        else:
            dictionary[root_tag]['children'][list(child.keys())[0]] = child[list(child.keys())[0]]
