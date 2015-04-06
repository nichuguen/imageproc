import cv2
import numpy as np
from OpenCVTools import OpenCVTools
from ImageField import ImageField

HOUGH_OFFSET = 6000
MIN_MERGED_LINES = 3
THRESHOLD = 0.9
CANNY_THRESHOLD = 40

def isSameTheta(listClasses, rt, threshold, index):
	mean = 0
	for _rt in listClasses[-1]:
		mean += _rt[index]
	mean /= len(listClasses[-1])
	return (mean - rt[index])**2 < threshold **2


def sortIndex(listRhoTheta, threshold, index):
	if len(listRhoTheta) > 0:
		listClasses = [[listRhoTheta.pop()]]
		for rt in listRhoTheta:
			if isSameTheta(listClasses, rt, threshold, index):
				listClasses[-1].append(rt)
			else:
				listClasses.append([rt])
		return listClasses
	else:
		raise

def computeMean(truc2):
	t = 0
	r = 0
	for rt in truc2:
		t += rt[1]
		r += rt[0]
	length = len(truc2)
	if length > 0:
		return (r / length, t/length)
	return (0,0)

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


def main():
	#imageField = ImageField("6872195.0", r'data\denens062014_50\6872195.0.jpg', r'data\denens062014_50\6872195.0_mask.jpg', r'data\denens062014_50\6872195.0.txt')
	imageField = ImageField("6870221.0", r'data\denens062014_50\6870221.0.jpg', r'data\denens062014_50\6870221.0_mask.jpg', r'data\denens062014_50\6870221.0.txt')

	#imageField = ImageField("6872195.0", r'data\denensprof062014_50\6872195.0.jpg', r'data\denensprof062014_50\6872195.0_mask.jpg', r'data\denensprof062014_50\6872195.0.txt')
	# imageField = ImageField("6870221.0", r'data\denensprof062014_50\6870221.0.jpg', r'data\denensprof062014_50\6870221.0_mask.jpg', r'data\denensprof062014_50\6870221.0.txt')
	img = imageField.realImg

	grey = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
	OpenCVTools.showWindow("grey", grey)

	grey = cv2.GaussianBlur(grey, (9,9), 0)
	# grey = cv2.bilateralFilter(grey, 4, 120,120)

	OpenCVTools.showWindow("gaussian filter", grey)
	edges = cv2.Canny(grey,CANNY_THRESHOLD,3*CANNY_THRESHOLD)
	OpenCVTools.showWindow("canny", edges)

	kernel = np.ones((10,10),np.uint8)
	edges = cv2.dilate(edges, kernel, iterations=3)
	OpenCVTools.showWindow("dilate", edges)

	kernel = np.ones((12,12), np.uint8)
	edges = cv2.erode(edges, kernel, iterations=2)
	OpenCVTools.showWindow("erode", edges)

	edges = cv2.Canny(edges,40,3*40)
	OpenCVTools.showWindow("canny 2", edges)

	lines = cv2.HoughLines(edges,1,np.pi/180,120)

	listRhoTheta = []
	for line in lines:
		for rho,theta in line:
			listRhoTheta.append((rho, theta))
			(norm, x1, y1, x2, y2) = getPoints(rho, theta)

	listRhoTheta.sort(key= lambda x: x[0])

	sortedTheta = sortIndex(listRhoTheta, THRESHOLD, 1)
	listMalentendu = []
	for listTheta in sortedTheta:
		listMalentendu.append(sortIndex(listTheta, 100, 0))

	listMeans = []
	for truc in listMalentendu:
		for truc2 in truc:
			if len(truc2) > MIN_MERGED_LINES:
				listMeans.append(computeMean(truc2))

	for mean in listMeans:
		(norm, x1, y1, x2, y2) = getPoints(mean[0], mean[1])
		cv2.line(img,(x1,y1),(x2,y2),(0,0,255),8)

	OpenCVTools.showWindow(imageField.name, img)
	cv2.waitKey(0)

if __name__ == '__main__':
	main()