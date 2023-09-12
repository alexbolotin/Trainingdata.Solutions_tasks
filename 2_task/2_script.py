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
    class_counters = {}

    for element in root.iter():
        label = element.get('label')
        if label is not None:
            if label not in class_counters:
                class_counters[label] = 1
            else:
                class_counters[label] += 1

    print(f'File: {xml_file}')
    for key, value in class_counters.items():
        print('Class:', key, ', quantity of elements:', value)