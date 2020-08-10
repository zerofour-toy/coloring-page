import cv2


class ImageConverter:
	def __init__(self, clip_limits):
		self.clip_limits = clip_limits

	def edged_images(self, image):
		sketch = self._sketch_image(image)
		return self._histogram(sketch, 8)

	def _sketch_image(self, image):
		gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
		gray_inv = 255 - gray
		blur = cv2.GaussianBlur(gray_inv, ksize=(21, 21), sigmaX=0, sigmaY=0)
		return cv2.divide(gray, 255-blur, scale=256)

	def _histogram(self, image, clip_limit):
		clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=(8, 8))
		return clahe.apply(image)
