import os
import xml.etree.ElementTree as ET
import random

def random_print_image(images, max = False, min = False):
    
    if max:
        print('6. Max image.')
    if min:
        print('6. Min image.')
    if len(images) > 1:
        print('Quantity of images with same size:', len(images))

    id = random.randint(1, len(images))
    print('Information about image:')
    print('Image ID -', images[id-1].get('id'))
    print('Image width -', images[id-1].get('width'))
    print('Image height -', images[id-1].get('height'))

current_directory = os.path.dirname(os.path.realpath(__file__))

# find all xml file in directory
xml_files = [f for f in os.listdir(current_directory) if f.endswith('.xml')]

# parse xml files:
for xml_file in xml_files:
    xml_file_path = os.path.join(current_directory, xml_file)
    
    # parse xml file
    tree = ET.parse(xml_file_path)
    root = tree.getroot()
    
    # 1. find image in file
    images = root.findall('.//image')
    
    # 2,3 find annotation images with 'box'
    annotated_images = [image for image in root.findall('.//image') if image.find('box') is not None]
    
    # 5,5* find all unique classes and elements inside
    element_tags = {}
    counter = 0
    for element in root.iter():
        label = element.get('label')
        if label is not None:
            counter += 1
    
    # 6. find max and min size of image
    max_images, min_images = [], []
    max_sum = 0
    min_sum = float('inf')

    for image in root.findall('.//image'):
        width = int(image.get('width'))
        height = int(image.get('height'))
        sum_params = width * height
        
        if sum_params > max_sum:
            max_sum = sum_params
            max_images = [image]
        elif sum_params == max_sum:
            max_images.append(image)
        
        if sum_params < min_sum:
            min_sum = sum_params
            min_images = [image]
        elif sum_params == min_sum:
            min_images.append(image)

    print(f'File: {xml_file}')
    print(f'1. Quantity of images: {len(images)}')
    if annotated_images:
        print(f'2. Annotated images: {len(annotated_images)}')
        print(f'3. Not annotated images: {len(images) - len(annotated_images)}')
    else:
        print(f'2. Annotated images: {len(annotated_images)}')
    print('5. Quantity of all elements:', counter)

    # random_print_image(max_images, max = True)
    # random_print_image(min_images, min = True)
    print('\n\n')