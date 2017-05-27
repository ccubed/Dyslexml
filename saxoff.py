import io
import xml.etree.ElementTree as ET


class Saxoff:
    def __init__(self):
        pass
    
    def parse(self, data):
        """
        Start a Saxoff session and return a dict.
        
        :param data: File like object or xml string
        """
        if isinstance(data, str):
            return self.__parse(ET.fromstring(data))
        elif isinstance(data, io.IOBase):
            return self.__parse(ET.fromstring(data.read()))
        else:
            raise StandardError("Saxoff requires a string or file like object.")
            
    def __parse(self, root):
        """
        Parse an XML document into a resulting dictionary.
        
        :param root: The ElementTree Instance
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
            child_element = self.build_child(child)
            result[base.tag]['children'][child.tag] = child_element[child.tag]
            
        return result
        
    def build_child(self, element):
        """
        Build a resulting child object given the child element.
        
        :param element: An XML element
        """
        child_object = {element.tag: {'type': 'child', 'children': None, 'attributes': None, 'value': element.text.strip() or None}}
        
        if element.attrib:
            child_object[element.tag]['attributes'] = {}
            for item in element.attrib:
                if "{" in item:
                    child_object[element.tag]['attributes'][item.split("}")[1]] = element.attrib[item]
                else:
                    child_object[element.tag]['attributes'][item] = element.attrib[item]
                
        for child in element:
            self.add_child(self.build_child(child), child_object, element.tag)
        
        return child_object
        
    def add_child(self, child, dictionary, root_tag):
        """
        Adding a child has some complication to it because we have to dynamically
        change data types in the resulting dictionary depending on the amount of each
        child. That's in addition to building the child object.
        
        :param child: The parsed Child object from an XML element
        :param dictionary dict: The dictionary so far
        :param root_tag str: The name of the root element
        """
        if not dictionary[root_tag]['children']:
            dictionary[root_tag]['children'] = {}
            dictionary[root_tag]['children'][list(child.keys())[0]] = child[list(child.keys())[0]]
        else:
            if list(child.keys())[0] in dictionary[root_tag]['children']:
                if dictionary[root_tag]['children'][list(child.keys())[0]].get('type', None) == "node":
                    dictionary[root_tag]['children'][list(child.keys())[0]]['children'].append(child[list(child.keys())[0]])
                else:
                    dictionary[root_tag]['children'][list(child.keys())[0]] = {'type': 'node', 'children': [dictionary[root_tag]['children'][list(child.keys())[0]], child[list(child.keys())[0]]]}
            else:
                dictionary[root_tag]['children'][list(child.keys())[0]] = child[list(child.keys())[0]]