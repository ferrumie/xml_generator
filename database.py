import logging
from sqlite3 import Connection, connect, Error
from typing import Any

from constants import BASE_URL


def create_connection(db_file: str) -> Connection | None:
    """
    Create db connection with the specified db.
    """
    conn = None
    try:
        conn = connect(db_file)
    except Error as e:
        logging.error('Database connection error: %s', e)

    return conn


def get_product_data(conn: Connection) -> list[Any]:
    """."""

    cursor = conn.cursor()

    # select only active products
    sql_query = '''
        SELECT p.product_id, pd.name, pd.description, m.name, p.quantity, p.price, p.image
        FROM product p
        LEFT JOIN product_description pd ON p.product_id = pd.product_id
        LEFT JOIN manufacturer m ON p.manufacturer_id = m.manufacturer_id
        WHERE p.status = '1'
        '''

    # SQL query to retrieve images for the current product sorted by sort_order
    image_query = '''
            SELECT image
            FROM product_image
            WHERE product_id = ?  -- Bind the product_id as a parameter
            ORDER BY sort_order
        '''

    cursor.execute(sql_query)
    products = cursor.fetchall()

    # Convert the result into a list of dictionaries with custom keys
    product_data = []
    for product in products:
        product_dict = {
            'id': product[0],
            'title': product[1],
            'description': product[2],
            'link': f'{BASE_URL}{product[0]}',
            'brand': product[3],
            'quantity': product[4],
            'price': product[5],
            'image_link': product[6],
            'additional_image_link': [],  # save as list
            'condition': 'new',
        }
        cursor.execute(image_query, (product[0],))
        images = cursor.fetchall()
        product_dict['additional_image_link'] = [
            f'{BASE_URL}{image[0]}' for image in images
        ]  # Append the images to the 'images' list
        product_data.append(product_dict)
    return product_data
