#*-* coding:utf-8 *-*
from operator import sub
import ImageField



class FieldFactory:

    DIR_SUFFIX = '_50'
    DIR_PROFILE_INFIX = 'prof'

    @staticmethod
    def createSeason(imgColorDirName, imgHeightDirName, seasonName):

        pass
    @staticmethod
    def createField(imgColorDirName, imgHeightDirName, listSeasonNames):

        pass

    @staticmethod
    def removeDuplicates(listDuplicates):
        """
        /!\ operation with a high cost
        :param listDuplicates: a list from which you want to remove duplicate entries
        :return:
        """
        return list(set(listDuplicates))

    @staticmethod
    def makeListFromFileNames(header, footer, listNames):
        return [header + x + footer for x in listNames]

    @staticmethod
    def makeListFromSeasons(header, footer, listNames):
        pass

    @staticmethod
    def createFieldList(rootDir, regionName):
        # Import the os module, for the os.walk function
        import os
        from ImageField import ImageField
        from Season import Season
        from Field import Field

        listDirs = []
        listFiles = []
        for dirName, subdirList, fileList in os.walk(rootDir):

            if dirName != rootDir:
                print('Found directory: %s' % dirName)
                for fname in fileList:
                    print('\t%s\\%s' % ('', fname))
                    listFiles.append(fname)
            else:
                listDirs = subdirList
            print(subdirList)
        print (listDirs)

        listSeasonNames = [x[len(regionName):-len(FieldFactory.DIR_SUFFIX)] for x in listDirs if FieldFactory.DIR_PROFILE_INFIX not in x]
        print (listSeasonNames)
        listFiles = sorted(FieldFactory.removeDuplicates(listFiles))
        import re
        patternMatch = r'\d*[.]\d.*'
        patternSearch = patternMatch[:-2]
        #removing extension and _mask + filtering the other useless files
        listFiles = [re.search(patternSearch, x, re.M).group() for x in listFiles if re.match(patternMatch, x)]
        listFiles = FieldFactory.removeDuplicates(listFiles)
        print(listFiles)
        print(len(listFiles))
        backslash = r"\n"[0] #this is ugly but pycharm sucks dicks

        headerRoot = rootDir +backslash

        field = "Field n°"
        during = " during "
        profile = " profile "
        mask = "_mask"
        jpg = ".jpg"
        txt = ".txt"
        mapHeaderSeason = {season: (headerRoot + regionName + season +FieldFactory.DIR_SUFFIX + backslash) for season in listSeasonNames}

        mapHeaderSeasonProfile = {season: (headerRoot + regionName +FieldFactory.DIR_PROFILE_INFIX + season +FieldFactory.DIR_SUFFIX + backslash) for season in listSeasonNames}
        imgColor = None
        imgHeight = None
        listFields = []
        for fileName in listFiles:
            listSeasons =[]
            for season in listSeasonNames:
                print (season)
                header = mapHeaderSeason[season]  #+ fileName
                imgColor = ImageField(field + fileName + during + season, header+ jpg, header + mask + jpg, header + txt )
                header = mapHeaderSeasonProfile[season] + fileName
                imgHeight = ImageField(field + fileName +profile + during + season, header+ jpg, header + mask + jpg, header + txt )
                listSeasons.append(Season(season, int(season[:-4]), imgColor, imgHeight))
            listFields.append(Field(fileName, listSeasons))
        print (listFields)

if __name__ == "__main__":
    FieldFactory.createFieldList("data", 'denens')