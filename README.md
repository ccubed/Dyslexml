# Dyslexml
# Thanks to Devon [Ikusaba-san](https://github.com/Ikusaba-san) for the name
Do you hate XML with a passion? Don't worry, I do too. Sadly, working with XML is a requirement foisted upon many of us.
This used to be a painful task, but not anymore. Now you have Dyslexml. Dyslexml is the Utility Knife for general purpose XML parsing.

# Features
## XML to Dictionary
Why work with XML when you can convert absolutely any valid (and hell, even some invalid) XML document into a Dictionary!
Want an example? Well step right up my friend! I have got you covered.
### Example
#### XML Document
This will be our document for the run.
```xml
<?xml version="1.0" encoding="UTF-8"?>
<animetitles>
	<anime aid="1">
		<title xml:lang="en" type="short">CotS</title>
		<title xml:lang="fr" type="official">Crest of the Stars</title>
		<title xml:lang="en" type="official">Crest of the Stars</title>
		<title type="official" xml:lang="pl">Crest of the Stars</title>
		<title type="syn" xml:lang="cs">HvÄzdnĂ˝ erb</title>
		<title xml:lang="x-jat" type="main">Seikai no Monshou</title>
		<title xml:lang="x-jat" type="short">SnM</title>
		<title type="syn" xml:lang="zh-Hans">ćçäšçşšçŤ </title>
		<title xml:lang="ja" type="official">ćçăŽç´çŤ </title>
	</anime>
  ...
</animetitles>
```
#### Dictionary
And behold, our beautiful dictionary. You'll notice some things which I will explain a little below and further in the docs.
Also, this dictionary was printed by converting it to json, because pprint is awful and the json printer is much nicer.
```python
{
   "animetitles": {
      "children": {
         "anime": [
            {
               "value": null,
               "children": {
                  "title": {
                     "children": [
                        {
                           "value": "CotS",
                           "children": null,
                           "type": "child",
                           "attributes": {
                              "lang": "en",
                              "type": "short"
                           }
                        },
                        {
                           "value": "Crest of the Stars",
                           "children": null,
                           "type": "child",
                           "attributes": {
                              "lang": "fr",
                              "type": "official"
                           }
                        }
```
To see the full example, go look check out the [gist](https://gist.github.com/ccubed/781dafce4c4d17474cf31a39eff29b9a).
### So parsing
The dictionaries are consistent once you understand the process. The root of the dictionary is always the root node of the document - animetitles here.
It then moves down the line and checks each child element to build a tree from that element. If the element has a text value, it is stored in value.
Attributes are stored as dictionaries with their key/value pairs appropriately preserved. At the moment I throw away namespaces, but I intend to provide an option to control that behavior.
There are 3 types: root is the root node, child is any node which contains data and is under root and a node is a special type that holds multiple children.
When any of type, value, children or attributes is empty it will be replaced with None.
#### What about node
In our example, we have many titles. Each anime has around six or more. I could have made a list of title children, but instead I decided to nest them.
This is where the node type comes in. The node type tells you that every child contained in children is of the type that its parent is.
In our example above, the **title** attribute is a node. Each child contained in the children of that dictionary is a title.
I thought this looked better, because you could think of it programmatically as for each title.

# Usage
## XML to Dictionary
```python
import dyslexml
dyslexml.Dyslexml.toDict(my_xml_string)
```

## Python Object to XML
```python
import dyslexml
a = {'a': 1, 'b': 2, 3: 'This is a long key', bytes(10): 'This is a crazy but acceptable key because I'm basically an ascii message'}
dyslexml.Dyslexml.toXml(a)
```

## Typing that out is hard
```python
from dyslexml import Dyslexml
a = Dyslexml()
a.toDict([1,2,3])
a.toXml(my_xml_string)
```
