from data import Data


class Todo:

    # 변경될 일 없는 순서있는 항목이므로 튜플
    types = ('과제', '시험')
    typeAssign = ('코딩', '보고서', '영상 제작', '문제 풀기', '기타')
    typeTest = ('중간시험', '기말시험', '라이브코딩', '쪽지시험', '기타')
    typeGroup = ('개인', '팀플')

    def __init__(self):
        self.data = Data()
        self.todoList = self.data.readData()[0]  # 구성은 dic

    def addTodo(self, todo):
        self.todoList += [todo]

    def modifyTodo(self, currtodo, newtodo):
        self.todoList[self.todoList.index(currtodo)] = newtodo

    def deleteTodo(self, todo):
        self.todoList.remove(todo)

    def sortTodoList(self):
        self.todoList.sort(key=lambda todo: todo['prior'])
        return self.todoList

    def getTodoList(self):
        return self.todoList

    def getSubjectTodoList(self, subject):
        return list(filter(lambda todo: todo['subject'] == subject, self.todoList))

    def getType(self):
        return self.types, self.typeAssign, self.typeTest, self.typeGroup
