from copy import deepcopy

class Field:
	def __init__(self, name, listSeasons):
		"""
		:param name: Name of the field
		:param listSeasons:  list of seasons
		"""
		self._name = name
		self._listSeasons = [season for season in listSeasons]
		self._result = None

	def __repr__(self):
		return self._name


	def computeResult(self):
		"""
		:return: result as Image
		"""
		return self._result
