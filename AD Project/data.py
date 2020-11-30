import pickle


class Data:

    def __init__(self):
        self.todo = []
        self.subject = []
        self.todoFile = 'Todo List.txt'
        self.subjectFile = 'Subject List.txt'

    def readData(self):
        try:
            fT = open(self.todoFile, 'rb')
            fS = open(self.subjectFile, 'rb')
        except FileNotFoundError as e:
            self.todo = []
            self.subject = []
            return

        try:
            self.todo = pickle.load(fT)
            self.subject = pickle.load(fS)
        except:
            pass
        fT.close()
        fS.close()

        return self.todo, self.subject

    def saveData(self, todo, subject):
        fT = open(self.todoFile, 'wb')
        pickle.dump(todo, fT)
        fT.close()

        fS = open(self.subjectFile, 'wb')
        pickle.dump(subject, fS)
        fS.close()
