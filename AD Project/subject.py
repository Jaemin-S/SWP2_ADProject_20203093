from data import Data


class Subject:

    type = ('전공', '교양')

    def __init__(self):
        self.data = Data()
        self.subjectList = self.data.readData()[1]

    def addSubject(self, subject):
        self.subjectList += [subject]

    def getSubjectList(self):
        return self.subjectList

    def getSubjectInfo(self, name):
        for info in self.subjectList:
            if info['name'] == name:
                return info

    def getType(self):
        return self.type
