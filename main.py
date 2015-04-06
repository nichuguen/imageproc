import cv2
import numpy as np
from OpenCVTools import OpenCVTools
from ImageField import ImageField

HOUGH_OFFSET = 6000

def main():
	#imageField = ImageField("6872195.0", r'data\denens062014_50\6872195.0.jpg', r'data\denens062014_50\6872195.0_mask.jpg', r'data\denens062014_50\6872195.0.txt')
	imageField = ImageField("6870221.0", r'data\denens062014_50\6870221.0.jpg', r'data\denens062014_50\6870221.0_mask.jpg', r'data\denens062014_50\6870221.0.txt')
	img = imageField.realImg

	grey = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
	OpenCVTools.showWindow("grey", grey)

	#grey = cv2.GaussianBlur(grey, (3,3), 0)
	grey = cv2.GaussianBlur(grey, (9,9), 0)
	# grey = cv2.bilateralFilter(grey, 4, 120,120)

	OpenCVTools.showWindow("bilateralfilter", grey)
	edges = cv2.Canny(grey,40,3*40)
	canny = edges
	OpenCVTools.showWindow("canny", edges)

	# th2 = cv2.adaptiveThreshold(grey,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)
	# OpenCVTools.showWindow("th2", th2)

	kernel = np.ones((10,10),np.uint8)
	#edges = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel, iterations=2)
	edges = cv2.dilate(edges, kernel, iterations=3)
	OpenCVTools.showWindow("dilate", edges)

	kernel = np.ones((12,12), np.uint8)
	edges = cv2.erode(edges, kernel, iterations=2)
	OpenCVTools.showWindow("erode", edges)

	edges = cv2.Canny(edges,40,3*40)
	OpenCVTools.showWindow("canny 2", edges)



	lines = cv2.HoughLines(edges,1,np.pi/180,100)

	#lines = sorted(lines, key=lambda x : getPoints(x.rho, x.theta)[0])[:10]

	listRhoTheta = []
	for line in lines:
		for rho,theta in line:
			listRhoTheta.append((rho, theta))
			(norm, x1, y1, x2, y2) = getPoints(rho, theta)
			cv2.line(img,(x1,y1),(x2,y2),(0,0,255),2)

	listRhoTheta.sort(key= lambda x: x[0])

	for x in listRhoTheta:
		print(x[0])
		print(x[1])

	OpenCVTools.showWindow(imageField.name, img)
	cv2.waitKey(0)

def getPoints(rho, theta):
	a = np.cos(theta)
	b = np.sin(theta)
	x0 = a*rho
	y0 = b*rho
	x1 = int(x0 + HOUGH_OFFSET*(-b))
	y1 = int(y0 + HOUGH_OFFSET*(a))
	x2 = int(x0 - HOUGH_OFFSET*(-b))
	y2 = int(y0 - HOUGH_OFFSET*(a))

	norm = (x1* x2)**2 + (y1* y2)**2
	return (norm, x1, y1, x2, y2)

if __name__ == '__main__':
	main()