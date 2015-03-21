class Season:
	def __init__(self,name, month, imgColor, imgHeight ):
		self._name = name
		self._month = month
		self._imgColor = imgColor
		self._imgHeight = imgHeight

	def __repr__(self):
		return self._name