from PIL import Image, ImageDraw
import xml.etree.ElementTree as ET
import os

def load_image_with_mask(image_file_path, xml_file_path):
    # Load image
    image = Image.open(image_file_path).convert("RGBA")

    # Load XML file with mask data
    tree = ET.parse(xml_file_path)
    root = tree.getroot()

    # Find the corresponding mask by image name
    mask = None
    for image_element in root.findall(".//image"):
        image_name = image_element.get("name").rsplit('/', 1)[1]
        if image_name == os.path.basename(image_file_path):
            mask = Image.new("RGBA", image.size, (0, 0, 0, 0))
            draw = ImageDraw.Draw(mask)
            for polygon_element in image_element.findall(".//polygon"):
                points_str = polygon_element.get("points").split(";")
                points = [(float(coord.split(",")[0]), float(coord.split(",")[1])) for coord in points_str]
                # polygon color
                mask_color = (255, 255, 255, 255)
                draw.polygon(points, fill=mask_color)
    return image, mask

def mask_apply():
    folder_with_images = 'images'
    directory = os.path.dirname(os.path.realpath(__file__))
    current_directory = os.path.join(directory, folder_with_images)

    image_files = [f for f in os.listdir(current_directory) if f.endswith('.jpg')]
    xml_file = os.path.join(directory, 'masks.xml')
    
    # iterate through all images
    for image_file in image_files:
        image_file_path = os.path.join(current_directory, image_file)
        image, mask = load_image_with_mask(image_file_path, xml_file)

        if mask is not None:
            result = Image.alpha_composite(image, mask)

            # Save result
            target_folder = current_directory
            file_name = os.path.splitext(os.path.basename(image_file_path))[0] + '_copy.png'
            save_path = os.path.join(target_folder, file_name)
            result.save(save_path)
        else:
            print("Mask not found for the image.")


mask_apply()
