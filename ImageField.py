import cv2

class ImageField:
	def __init__(self, name, realImgPath, maskImgPath, textPath):
		self._name = name
		self._realImg = cv2.imread(realImgPath)
		self._maskImg = cv2.imread(maskImgPath)
		self._textPath = textPath

	def __repr__(self):
		return self._name

	@property
	def realImg(self):
		return self._realImg

	@property
	def maskImg(self):
		return self._maskImg
