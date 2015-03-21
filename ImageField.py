class ImageField:
	def __init__(self, name, realImg, maskImg, text):
		self._name = name
		self._realImg = realImg
		self._maskImg = maskImg
		self._text = text

	def __repr__(self):
		return self._name