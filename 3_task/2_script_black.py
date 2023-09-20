from PIL import Image, ImageDraw
import xml.etree.ElementTree as ET
import os

# black background
def create_black_background(image):

    background_color = (0, 0, 0, 255)
    background = Image.new("RGBA", image.size, background_color)
    return background

# find color in skins
def get_color_by_label(label_elements, label_name):

    # if Ignore - then no color
    if label_name.lower() == 'ignore':
        return (0, 0, 0, 255)

    for label_element in label_elements:
        if label_name == label_element.find("name").text:
            color_hex = label_element.find("color").text
            return tuple(int(color_hex[i:i+2], 16) for i in (1, 3, 5))

    return (0, 0, 0, 0)

def load_image_with_mask(image_file_path, xml_file_path):
    # Load image
    image = Image.open(image_file_path).convert("RGBA")

    # Load XML file with mask data
    tree = ET.parse(xml_file_path)
    root = tree.getroot()

    mask = None

    image_name = os.path.basename(image_file_path)

    # Find the corresponding mask by image element name
    for image_element in root.findall(".//image"):
        if image_element.get("name").rsplit('/', 1)[1] == image_name:
            
            mask = create_black_background(image)
            # mask = Image.new("RGBA", image.size, (0, 0, 0, 0))
            draw = ImageDraw.Draw(mask)

            polygon_elements = image_element.findall(".//polygon")
            polygon_elements.sort(key=lambda elem: int(elem.get("z_order")))

            label_elements = root.findall(".//labels/label")

            for polygon in polygon_elements:
                polygon_label = polygon.get("label")

                # find color in skins
                mask_color = get_color_by_label(label_elements, polygon_label)

                points_str = polygon.get("points").split(";")
                points = [(float(coord.split(",")[0]), float(coord.split(",")[1])) for coord in points_str]
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
