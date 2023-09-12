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
    
    # 7. change id`s to reverse
    images = list(root.findall('.//image'))    
    existing_ids = [image.get('id') for image in images][::-1]

    for image, existing_id in zip(images, existing_ids):
        image.set('id', existing_id)

    # 8. change image extension to png and remove the path
    for image in images:
        name = image.get('name')
        
        # check is there are some '/' in name
        part = name.rsplit('/', 1)
        if len(part)>1:
            new_part = part[1].rsplit('.',1)
        else:
            new_part = part[0].rsplit('.',1)
        
        new_name = new_part[0] + '.png'
        image.set('name', new_name)

    new_file_name = os.path.splitext(xml_file)[0] + '_changed.xml'
    file_path = os.path.join(current_directory, new_file_name)
    tree.write(file_path, encoding='utf-8')