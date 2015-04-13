# -*- coding: utf8 -*-
import cv2
import numpy as np
from OpenCVTools import OpenCVTools
from ImageField import ImageField
from copy import deepcopy

HOUGH_OFFSET = 6000
MIN_MERGED_LINES = 3
THRESHOLD_THETA = 0.9
THRESHOLD_RHO = 100
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

def computeMean(lines):
	t = 0
	r = 0
	for rt in lines:
		t += rt[1]
		r += rt[0]
	length = len(lines)
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


def houghLinesFiltered(img, listRhoTheta):
	'''
	Le but de cette méthode est de regrouper de manière simple des droites similaires issues d'un HoughLines
	Pour ce faire, on regroupe les rho et les theta dans des classes et on dessine la droite moyenne de ces dernières.
	Les classes n'ayant pas suffisament de droite sont ignorées.
	Les paramètres modifiables sont THRESHOLD_RHO et THRESHOLD_THETA.
	:param img: image sur laquelle afficher les lignes
	:param listRhoTheta: liste des rho et des theta issus d'un HoughLines standard
	:return:
	'''
	listRhoTheta.sort(key=lambda x: x[0])
	sortedTheta = sortIndex(listRhoTheta, THRESHOLD_THETA, 1)
	listGroupLines = []
	for listTheta in sortedTheta:
		listGroupLines.append(sortIndex(listTheta, THRESHOLD_RHO, 0))
	listMeans = []
	for groupLine in listGroupLines:
		for line in groupLine:
			if len(line) > MIN_MERGED_LINES:
				listMeans.append(computeMean(line))
	for mean in listMeans:
		(norm, x1, y1, x2, y2) = getPoints(mean[0], mean[1])
		cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 8)


def main():

	# Exemples utilisés lors de la présentations
	imageField = ImageField("6870221.0", r'data\denens062014_50\6870221.0.jpg', r'data\denens062014_50\6870221.0_mask.jpg', r'data\denens062014_50\6870221.0.txt')
	# imageField = ImageField("6872195.0", r'data\denens062014_50\6872195.0.jpg', r'data\denens062014_50\6872195.0_mask.jpg', r'data\denens062014_50\6872195.0.txt')

	# Même image, autre saison
	# imageField = ImageField("6870221.0", r'data\denens082014_50\6870221.0.jpg', r'data\denens082014_50\6870221.0_mask.jpg', r'data\denens082014_50\6870221.0.txt')
	# imageField = ImageField("6870221.0", r'data\denens102014_50\6870221.0.jpg', r'data\denens102014_50\6870221.0_mask.jpg', r'data\denens102014_50\6870221.0.txt')

	# Images en profondeur
	# imageField = ImageField("6872195.0", r'data\denensprof062014_50\6872195.0.jpg', r'data\denensprof062014_50\6872195.0_mask.jpg', r'data\denensprof062014_50\6872195.0.txt')
	# imageField = ImageField("6870221.0", r'data\denensprof062014_50\6870221.0.jpg', r'data\denensprof062014_50\6870221.0_mask.jpg', r'data\denensprof062014_50\6870221.0.txt')

	img = imageField.realImg
	OpenCVTools.showWindow("original", img)

	# NIVEAUX DE GRIS
	grey = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
	OpenCVTools.showWindow("grey", grey)

	# FLOU GAUSSIEN
	grey = cv2.GaussianBlur(grey, (9,9), 0)
	OpenCVTools.showWindow("gaussian filter", grey)

	# CANNY
	edges = cv2.Canny(grey,CANNY_THRESHOLD,3*CANNY_THRESHOLD)
	OpenCVTools.showWindow("canny", edges)

	# FERMETURE
	kernel = np.ones((10,10),np.uint8)
	edges = cv2.dilate(edges, kernel, iterations=3)
	OpenCVTools.showWindow("dilate", edges)

	kernel = np.ones((12,12), np.uint8)
	edges = cv2.erode(edges, kernel, iterations=2)
	OpenCVTools.showWindow("erode", edges)

	# CANNY 2
	edges = cv2.Canny(edges,40,3*40)
	OpenCVTools.showWindow("canny 2", edges)

	# HOUGH LINES SANS FILTRE
	lines = cv2.HoughLines(edges,1,np.pi/180,120)
	imgHoughLinesNoFilter = deepcopy(img)
	listRhoTheta = []
	for line in lines:
		for rho,theta in line:
			listRhoTheta.append((rho, theta))
			(norm, x1, y1, x2, y2) = getPoints(rho, theta)
			cv2.line(imgHoughLinesNoFilter,(x1,y1),(x2,y2),(0,0,255),8)
	OpenCVTools.showWindow("hough lines nofilter", imgHoughLinesNoFilter)

	# HOUGH LINES EN NE GARDANT QUE LES MEILLEURES LIGNES
	houghLinesFiltered(img, listRhoTheta)

	OpenCVTools.showWindow(imageField.name, img)
	cv2.waitKey(0)

if __name__ == '__main__':
	main()