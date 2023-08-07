
from xml.etree import cElementTree as ET
from xml.sax.saxutils import unescape
from constants import DB_FILE

from database import create_connection, get_product_data

def generate_xml_file()-> None:
    """Generate XML file."""    
    # create db connection
    conn = create_connection(db_file=DB_FILE)
    with conn:
        product_data = get_product_data(conn=conn)

     # Create the root element of the XML feed using cElementTree
    root = ET.Element('product')
    root.set('xmlns:g', 'http://base.google.com/ns/1.0')
    channel = ET.SubElement(root, 'channel')
    for product in product_data:
        item = ET.SubElement(channel, 'item')

        ET.SubElement(item, 'g:id').text = product['id']
        ET.SubElement(item, 'g:title').text = product['title']
        ET.SubElement(item, 'g:description').text = unescape(product['description'])  # Unescape xml entities
        ET.SubElement(item, 'g:link').text = product['link']
        ET.SubElement(item, 'g:brand').text = product['brand']
        ET.SubElement(item, 'g:availability').text = 'in_stock' if int(product['quantity']) > 0 else 'out of stock'
        ET.SubElement(item, 'g:price').text = f'{product["price"]} HUF'  # Price in Hungarian Forints (HUF)
        ET.SubElement(item, 'g:image_link').text = product['image_link']
        # Additional image links
        for image_link in product['additional_image_link']:
            ET.SubElement(item, 'g:additional_image_link').text = image_link.strip()
        ET.SubElement(item, 'g:condition').text = product['condition']  # All products are sold as new

    # Create the ElementTree and write it to a file named feed.xml using cElementTree
    tree = ET.ElementTree(root)
    tree.write('feed.xml', encoding='utf-8', xml_declaration=True)

if __name__ == '__main__':
    generate_xml_file()