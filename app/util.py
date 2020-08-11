import base64
import cv2
import numpy as np


def create_image(image_bytes):
	encoded_image = np.fromstring(image_bytes, dtype=np.uint8)
	return cv2.imdecode(encoded_image, cv2.IMREAD_COLOR)


def meta_raw_image(image_bytes, name, content_type):
	return {
		"name": name,
		"contentType": content_type,
		"content": base64.b64encode(image_bytes).decode('utf-8')
	}


def meta_image(image, name, content_type):
	success, encoded_image = cv2.imencode(name, image)
	return meta_raw_image(encoded_image, name, content_type)
