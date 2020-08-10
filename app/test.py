import os
from PIL import Image, ImageFilter, ImageEnhance
import cv2
import numpy as np

def output(filename):
	fname, ext = os.path.splitext(filename)
	return fname + '-out' + ext


def edge_pil(filename):
	fname, ext = os.path.splitext(filename)
	im = Image.open(filename)
	im = im.filter(ImageFilter.CONTOUR)
	im = im.filter(ImageFilter.SMOOTH_MORE)
# im = im.convert('L')
# im = ImageOps.invert(im)
# im = im.filter(ImageFilter.SMOOTH)
# im = im.convert('L')
# im = ImageEnhance.Contrast(im).enhance(10)
# im = im.filter(ImageFilter.SMOOTH_MORE)
	im.save(fname + '-out' + ext)


def edge1(img):
	img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	# img = cv2.Sobel(img, cv2.CV_8U, 1, 0, ksize=3)
	# img = cv2.Scharr(img, cv2.CV_8U, 1, 0)
	img = cv2.Laplacian(img, cv2.CV_8U, ksize=3)
	# img = cv2.Canny(img, 30, 70)
	img = ~img
	img = cv2_histogram(img)
	# img = cv2.GaussianBlur(img, (5, 5), 0)
	return img

def edge2(img):
	img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	img = cv2.Sobel(img, cv2.CV_8U, 1, 0, ksize=3)
	# img = cv2.Scharr(img, cv2.CV_8U, 1, 0)
	# img = cv2.Laplacian(img, cv2.CV_8U, ksize=3)
	# img = cv2.Canny(img, 30, 70)
	img = ~img
	img = cv2_histogram(img)
	# img = cv2.medianBlur(img, 3)
	# img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 15, 20)
	# img = cv2.GaussianBlur(img, (5, 5), 0)
	return img

def edge3(img):
	img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	img_gray_inv = 255 - img_gray
	img_blur = cv2.GaussianBlur(img_gray_inv, ksize=(21, 21), sigmaX=0, sigmaY=0)
	img = cv2.divide(img_gray, 255-img_blur, scale=256)
	return img


def cv2_histogram(img):
	clahe = cv2.createCLAHE(clipLimit=8.0, tileGridSize=(8, 8))
	return clahe.apply(img)


ifiles = [
	'sample/ferrari.jpg',
	'sample/gunhui.jpg',
	'sample/park.jpg',
	'sample/sebu.jpg',
	'sample/guam.jpg',
	'sample/pool.jpg',
	'sample/car.jpg',
	'D:\car.png',
	]
for ifile in ifiles:
	print('edge: ' + ifile)
	fname, ext = os.path.splitext(ifile)
	img = cv2.imread(ifile)
	img1 = edge1(img)
	img2 = edge2(img)
	img3 = edge3(img)
	img4 = np.mean([img1, img2, img3], axis=0).astype(np.uint8)
	img3 = cv2_histogram(img3)
	# img3 = cv2.GaussianBlur(img3, (1, 1), 0)
	cv2.imwrite(fname + '-out' + ext, img3)



