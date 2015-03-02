import cv2
import numpy as np

WINDOW_SIZE = 500

def showWindow(title, edges):
	cv2.namedWindow(title, 0)
	cv2.resizeWindow(title, WINDOW_SIZE, WINDOW_SIZE)
	cv2.imshow(title, edges)


def main():
	# img = cv2.imread(r'data\temp\sudoku.png')
	img = cv2.imread(r'data\temp\dave.jpg')
	gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
	showWindow("gray", gray)
	gray = cv2.medianBlur(gray, 5)
	showWindow("median", gray)
	edges = cv2.Canny(gray,50,150,apertureSize = 3)

	showWindow("canny", edges)

	lines = cv2.HoughLines(edges,1,np.pi/180,200)
	for line in lines:
		for rho,theta in line:
			a = np.cos(theta)
			b = np.sin(theta)
			x0 = a*rho
			y0 = b*rho
			x1 = int(x0 + 1000*(-b))
			y1 = int(y0 + 1000*(a))
			x2 = int(x0 - 1000*(-b))
			y2 = int(y0 - 1000*(a))

			cv2.line(img,(x1,y1),(x2,y2),(0,0,255),2)

	showWindow("img", img)
	cv2.waitKey(0)

if __name__ == '__main__':
	print "lala"
	main()