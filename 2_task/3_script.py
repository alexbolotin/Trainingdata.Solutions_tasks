import os
import xml.etree.ElementTree as ET

current_directory = os.path.dirname(os.path.realpath(__file__))

# find all xml file in directory
xml_files = [f for f in os.listdir(current_directory) if f.endswith('.xml')]

# parse xml files:
for xml_file in xml_files:
    xml_file_path = os.path.join(current_directory, xml_file)
    
    # parse xml file
    tree = ET.parse(xml_file_path)
    root = tree.getroot()
     
    # 4 find all unique classes
    elements_tag = {}

    for element in root.iter():
        label = element.get('label')
        if label is not None:
            element_tag = element.tag
            if element_tag not in elements_tag:
                elements_tag[element_tag] = 1
            else:
                elements_tag[element_tag] += 1

    print(f'File: {xml_file}')
    for key, value in elements_tag.items():
        print('Element:', key, ', quantity of elements:', value)
    print('\n\n')