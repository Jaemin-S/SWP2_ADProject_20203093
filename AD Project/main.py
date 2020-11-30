from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QScrollArea
from PyQt5.QtWidgets import QLayout, QGridLayout, QHBoxLayout, QVBoxLayout, QTabWidget
from PyQt5.QtWidgets import QLabel, QComboBox, QTextEdit, QLineEdit, QToolButton, QSlider
from PyQt5.QtGui import QIntValidator
#import copy

from todo import Todo
from subject import Subject
from data import Data


class ToDoList(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.todo = Todo()
        self.subject = Subject()
        self.data = Data()

        self.todoList = self.todo.getTodoList()
        self.subjectList = self.subject.getSubjectList()
        self.layout = {}
        self.listButtonRow = {}
        self.listLineRow = {}
        self.initUI()

        self.subjectCredit.setValidator(QIntValidator(self))

        self.subjectAddButton.clicked.connect(lambda: self.subjectAddButtonClicked(self.getSubjectInfo()))
        self.todoAddButton.clicked.connect(lambda: self.todoAddButtonClicked(self.getTodoInfo()))

        self.todoTypeMajor.currentIndexChanged.connect(self.todoTypeMajorChanged)

        self.todoProgValue = 0
        self.todoProg.valueChanged[int].connect(self.todoProgChanged)

    def closeEvent(self, event):
        self.data.saveData(self.todoList, self.subjectList)

    def initUI(self):
        # subjectLayout
        self.subjectType = QComboBox()
        for types in self.subject.getType():
            self.subjectType.addItem(types)
        self.subjectCredit = QLineEdit()
        self.subjectCredit.setAlignment(Qt.AlignRight)
        self.subjectCreditLabel = QLabel('학점')
        self.subjectProf = QLineEdit()
        self.subjectProf.setAlignment(Qt.AlignRight)
        self.subjectProfLabel = QLabel('교수님')
        self.subjectAddButton = QToolButton()
        self.subjectAddButton.setText('추가')

        self.subjectLayout = QHBoxLayout()
        self.subjectLayout.addWidget(self.subjectType)
        self.subjectLayout.addWidget(self.subjectCredit)
        self.subjectLayout.addWidget(self.subjectCreditLabel)
        self.subjectLayout.addWidget(self.subjectProf)
        self.subjectLayout.addWidget(self.subjectProfLabel)
        self.subjectLayout.addWidget(self.subjectAddButton)

        # listLayout
        self.listLayout = QGridLayout()
        self.listLayoutLines = QGridLayout()

        # todoLayout
        # Line 1
        self.todoSubjectLabel = QLabel('과목')
        self.todoSubjectLabel.setAlignment(Qt.AlignCenter)
        self.todoSubject = QComboBox()

        self.todoTypeLabel = QLabel('유형')
        self.todoTypeLabel.setAlignment(Qt.AlignCenter)
        self.todoTypeMajor = QComboBox()
        for types in self.todo.getType()[0]:
            self.todoTypeMajor.addItem(types)

        self.todoType = QComboBox()
        for types in self.todo.getType()[1]:
            self.todoType.addItem(types)

        self.todoTypeGroup = QComboBox()
        for types in self.todo.getType()[3]:
            self.todoTypeGroup.addItem(types)

        # Line 2
        self.todoNameLabel = QLabel('이름')
        self.todoNameLabel.setAlignment(Qt.AlignCenter)
        self.todoName = QLineEdit()

        # Line 3
        self.todoDateLabel = QLabel('기한')
        self.todoDateLabel.setAlignment(Qt.AlignCenter)
        self.todoDateMonth = QComboBox()
        for month in range(1, 13):
            self.todoDateMonth.addItem(str(month))
        self.todoMonthLabel = QLabel('월')
        self.todoDateDay = QComboBox()
        for day in range(1, 32):
            self.todoDateDay.addItem(str(day))
        self.todoDayLabel = QLabel('일')
        self.todoPriorLabel = QLabel('우선순위')
        self.todoPriorLabel.setAlignment(Qt.AlignCenter)
        self.todoPrior = QComboBox()
        for num in range(1, len(self.todoList)+2):
            self.todoPrior.addItem(str(num))

        # Line 4
        self.todoMemoLabel = QLabel('메모')
        self.todoMemoLabel.setAlignment(Qt.AlignCenter)
        self.todoMemo = QTextEdit()

        # Line 5
        self.todoProgLabel = QLabel('진행도')
        self.todoProg = QSlider(Qt.Horizontal, self)
        self.todoProg.setRange(0, 100)
        self.todoProgNum = QLabel()

        self.todoAddButton = QToolButton()
        self.todoAddButton.setText('추가')

        self.todoLayout = QGridLayout()
        self.todoLayout.addWidget(self.todoSubjectLabel, 0, 0)
        self.todoLayout.addWidget(self.todoSubject, 0, 1, 1, 2)
        self.todoLayout.addWidget(self.todoTypeLabel, 0, 3)
        self.todoLayout.addWidget(self.todoTypeMajor, 0, 4)
        self.todoLayout.addWidget(self.todoType, 0, 5)
        self.todoLayout.addWidget(self.todoTypeGroup, 0, 6)

        self.todoLayout.addWidget(self.todoNameLabel, 1, 0)
        self.todoLayout.addWidget(self.todoName, 1, 1, 1, 6)

        self.todoLayout.addWidget(self.todoDateLabel, 2, 0)
        self.todoLayout.addWidget(self.todoDateMonth, 2, 1)
        self.todoLayout.addWidget(self.todoMonthLabel, 2, 2)
        self.todoLayout.addWidget(self.todoDateDay, 2, 3)
        self.todoLayout.addWidget(self.todoDayLabel, 2, 4)
        self.todoLayout.addWidget(self.todoPriorLabel, 2, 5)
        self.todoLayout.addWidget(self.todoPrior, 2, 6)

        self.todoLayout.addWidget(self.todoMemoLabel, 3, 0)
        self.todoLayout.addWidget(self.todoMemo, 3, 1, 1, 6)

        self.todoLayoutUnder = QHBoxLayout()
        self.todoLayoutUnder.addWidget(self.todoProgLabel)
        self.todoLayoutUnder.addWidget(self.todoProg)
        self.todoLayoutUnder.addWidget(self.todoProgNum)
        self.todoLayoutUnder.addWidget(self.todoAddButton)
        self.todoLayoutUnder.stretch(1)

        self.todoLayout.addLayout(self.todoLayoutUnder, 4, 0, 1, 7)

        # tabLayout
        self.subjectTabs = QTabWidget()

        self.tabAll = QWidget()
        self.subjectTabs.addTab(self.tabAll, '전체')
        self.tabAll.setLayout(self.addScroll(self.listLayout))

        self.tabAdd = QWidget()
        self.subjectTabs.addTab(self.tabAdd, '과목 추가')

        self.subjectNameLabel = QLabel('이름')
        self.subjectName = QLineEdit()
        self.tabAddSubject = QHBoxLayout()
        self.tabAddSubject.addWidget(self.subjectNameLabel)
        self.tabAddSubject.addWidget(self.subjectName)
        self.tabAddLayout = QVBoxLayout()
        self.tabAddLayout.addLayout(self.tabAddSubject)
        self.tabAddLayout.addLayout(self.subjectLayout)
        self.tabAdd.setLayout(self.tabAddLayout)

        # 파일에 있는 과목탭 만들기
        for i in range(len(self.subjectList)):
            self.subjectAddButtonClicked(self.subjectList[i])

        self.subjectTabsLayout = QVBoxLayout()
        self.subjectTabsLayout.addWidget(self.subjectTabs)

        # mainLayout
        self.mainLayout = QGridLayout()
        self.mainLayout.setSizeConstraint(QLayout.SetFixedSize)
        self.mainLayout.addLayout(self.subjectTabsLayout, 0, 0)
        self.mainLayout.addLayout(self.todoLayout, 1, 0)

        self.setLayout(self.mainLayout)

        self.setWindowTitle('TODO LIST')

        # 파일에 있는 TODO 불러오기
        for i in range(len(self.todoList)):
            self.todoAddButtonClicked(self.todoList[i])

    # 탭 레이아웃
    # 스크롤 되는 레이아웃 만드는 함수
    def addScroll(self, layout):
        listLayoutScroll = QScrollArea()
        widget = QWidget()
        layout.setSizeConstraint(QLayout.SetMinAndMaxSize)
        widget.setLayout(layout)
        listLayoutScroll.setWidgetResizable(True)
        listLayoutScroll.setFixedHeight(150)
        listLayoutScroll.setWidget(widget)
        listLayout = QGridLayout()
        listLayout.addWidget(listLayoutScroll, 0, 0)
        return listLayout

    # 추가한 TODO의 정보를 보여주는 HBoxLayout. addTabTodoLayout 함수에 인자로 넘어감.
    def getListLayoutLine(self, info, row):
        listPrior = QLabel(info['prior'])
        listPrior.setAlignment(Qt.AlignCenter)
        listDate = QLabel(info['dateMonth'] + '월 ' + info['dateDay'] + '일')
        listDate.setAlignment(Qt.AlignCenter)
        listType = QLabel(info['types'])
        listType.setAlignment(Qt.AlignCenter)
        listName = QLabel(info['name'])
        listName.setAlignment(Qt.AlignLeft)
        listCompleteButton = QToolButton(self)
        listCompleteButton.setText('완료')
        listProg = QLabel(info['prog'] + '%')
        listProg.setAlignment(Qt.AlignCenter)
        listDetailButton = QToolButton(self)
        listDetailButton.setText('상세')

        if info['typeGroup'] == '개인':
            listPrior.setStyleSheet('color: purple;'
                                    'background-color: #e6d6ff;')
        elif info['typeGroup'] == '팀플':
            listPrior.setStyleSheet('color: #854800;'
                                    'background-color: #ffdfb3;')

        listLayoutLine = QHBoxLayout(self)
        listLayoutLine.addWidget(listPrior)
        listLayoutLine.addWidget(listDate)
        listLayoutLine.addWidget(listType)
        listLayoutLine.addWidget(listName)
        listLayoutLine.addWidget(listCompleteButton)
        listLayoutLine.addWidget(listProg)
        listLayoutLine.addWidget(listDetailButton)
        self.listButtonRow[listDetailButton] = row

        listCompleteButton.clicked.connect(lambda: self.listCompleteButtonClicked(info, listLayoutLine))
        listDetailButton.clicked.connect(lambda: self.listDetailButtonClicked(info))

        return listLayoutLine

    # 추가한 TODO를 마지막 라인에 추가한 탭별 TODO LIST를 새로 구성함
    def addTabTodoLayout(self, listlayout, listlayoutline, position):
        listlayout.addLayout(listlayoutline, position, 0)
        return self.addScroll(listlayout)

    # TODO를 추가할 때 우선순위 순으로 정렬해서 보여주게 하는 함수
    # 구현 실패
    def sortListLayout(self, currlist, sortedlist):
        self.listButtonRow.clear()
        for idx in range(len(sortedlist)-1, -1, -1):
            if idx == 0 or currlist[idx-1] == sortedlist[idx-1]:
                return
            lowerrow = self.listLineRow[str(currlist[idx])]
            upperrow = self.listLineRow[str(sortedlist[idx])]
            #self.listLayoutLines.removeItem(self.listLayoutLines.itemAtPosition(lowerrow, 0))
            #self.listLayoutLines.removeItem(self.listLayoutLines.itemAtPosition(upperrow, 0))
            for i in range(7):
                self.listLayoutLines.itemAtPosition(lowerrow, 0).itemAt(i).widget().close()
                self.listLayoutLines.itemAtPosition(upperrow, 0).itemAt(i).widget().close()
            listLayoutLineLow = self.getListLayoutLine(sortedlist[idx], lowerrow)
            listLayoutLineUp = self.getListLayoutLine(sortedlist[idx], upperrow)
            self.listLayoutLines.addLayout(listLayoutLineLow, lowerrow, 0)
            self.listLayoutLines.addLayout(listLayoutLineUp, upperrow, 0)
            self.listLineRow[str(currlist[idx])] = upperrow
            self.listLineRow[str(sortedlist[idx])] = lowerrow
        self.updateTabLayout(0, '전체', self.addScroll(self.listLayoutLines))
        self.subjectTabs.setCurrentIndex(0)

    # 해당 과목의 정보를 보여줌
    def addSubjectInfoLayout(self, info):
        subjectType = QLabel(info['types'])
        subjectType.setAlignment(Qt.AlignRight)
        subjectCredit = QLabel(info['credit'])
        subjectCredit.setAlignment(Qt.AlignRight)
        subjectCreditLabel = QLabel('학점')
        subjectCreditLabel.setAlignment(Qt.AlignLeft)
        subjectProf = QLabel(info['prof'])
        subjectProf.setAlignment(Qt.AlignRight)
        subjectProfLabel = QLabel('교수님')
        subjectProfLabel.setAlignment(Qt.AlignLeft)

        subjectLayout = QHBoxLayout()
        subjectLayout.addWidget(subjectType)
        subjectLayout.addWidget(subjectCredit)
        subjectLayout.addWidget(subjectCreditLabel)
        subjectLayout.addWidget(subjectProf)
        subjectLayout.addWidget(subjectProfLabel)

        return subjectLayout

    # 선택한 탭의 과목 정보와 TODO LIST를 보여주는 탭 레이아웃
    def updateSubjectTabLayout(self, idx, name, tablayout, listlayout):
        tabLayout = QVBoxLayout()
        tabLayout.addLayout(self.addSubjectInfoLayout(self.subject.getSubjectInfo(name)))
        tabLayout.addLayout(self.addScroll(listlayout))
        self.updateTabLayout(idx, name, tablayout)

    # 새로 구성한 탭 레이아웃으로 해당 탭을 다시 생성
    def updateTabLayout(self, idx, name, tablayout):
        self.subjectTabs.removeTab(idx)
        tab = QWidget()
        self.subjectTabs.insertTab(idx, tab, name)
        tab.setLayout(tablayout)

    # 과목 추가 탭을 통해 추가한 과목의 탭을 추가함
    def subjectAddButtonClicked(self, info):
        self.subjectName.clear()
        self.subjectCredit.clear()
        self.subjectProf.clear()

        idx = len(self.subjectList)
        name = info['name']

        # 파일에서 읽어온 과목 탭 추가
        for index in range(len(self.subjectList)):
            if self.subjectList[index]['name'] == name:
                idx = index
                break

        if info not in self.subjectList:
            self.subject.addSubject(info)
        self.todoSubject.addItem(name)

        tab = QWidget()
        self.subjectTabs.insertTab(idx+1, tab, name)

        listLayout = QGridLayout(self)
        tabLayout = QVBoxLayout(self)
        tabLayout.addLayout(self.addSubjectInfoLayout(info))
        tabLayout.addLayout(self.addScroll(listLayout))
        tab.setLayout(tabLayout)

        self.layout[name] = [tabLayout, listLayout]

# Slots
    def listCompleteButtonClicked(self, info, layout):
        self.todo.deleteTodo(info)
        del self.listLineRow[str(info)]
        for i in range(layout.count()):
            layout.itemAt(i).widget().close()

        if len(self.todoList) + 1 < self.todoPrior.count():
            self.todoPrior.removeItem(self.todoPrior.count() - 1)

    def listDetailButtonClicked(self, info):
        sender = self.sender()
        self.todoAddButton.clicked.disconnect()
        self.todoAddButton.clicked.connect(lambda: self.todoModifyButtonClicked(info, sender))

        self.todoSubject.setCurrentText(info['subject'])
        self.todoTypeMajor.setCurrentText(info['typeMajor'])
        self.todoType.setCurrentText(info['types'])
        self.todoTypeGroup.setCurrentText(info['typeGroup'])
        self.todoName.setText(info['name'])
        self.todoDateMonth.setCurrentText(info['dateMonth'])
        self.todoDateDay.setCurrentText(info['dateDay'])
        self.todoPrior.setCurrentText(info['prior'])
        self.todoMemo.setText(info['memo'])
        self.todoProgNum.setText('{}%'.format(info['prog']))
        self.todoAddButton.setText('수정')

    def todoModifyButtonClicked(self, info, sender):
        row = self.listButtonRow[sender]
        self.todoAddButton.clicked.disconnect()
        self.todoAddButton.clicked.connect(lambda: self.todoAddButtonClicked(self.getTodoInfo()))

        todoInfo = self.getTodoInfo()
        self.listLineRow[str(todoInfo)] = self.listLineRow[str(info)]
        del self.listLineRow[str(info)]
        self.todo.modifyTodo(info, todoInfo)
        self.todoName.clear()
        self.todoMemo.clear()
        self.listLayoutLines.removeItem(self.listLayoutLines.itemAtPosition(row, 0))
        del self.listButtonRow[sender]

        listLayoutLine = self.getListLayoutLine(todoInfo, row)
        self.updateTabLayout(0, '전체', self.addTabTodoLayout(self.listLayoutLines, listLayoutLine, row))
        subject = todoInfo['subject']
        for index in range(1, len(self.subjectList) + 1):
            if self.subjectTabs.tabText(index) == subject:
                self.layout[subject][1].removeItem(self.layout[subject][1].itemAtPosition(row, 0))
                self.updateSubjectTabLayout(index, subject, self.layout[subject][0],
                                            self.addTabTodoLayout(self.layout[subject][1], listLayoutLine, self.layout[subject][1].rowCount()))
                break
        self.subjectTabs.setCurrentIndex(0)
        self.todoAddButton.setText('추가')

    def todoAddButtonClicked(self, todoInfo):
        if todoInfo not in self.todoList:
            self.todo.addTodo(todoInfo)
        self.todoName.clear()
        self.todoMemo.clear()
        if len(self.todoList) + 1 > self.todoPrior.count():
            self.todoPrior.addItem(str(len(self.todoList) + 1))
        row = self.listLayoutLines.rowCount()
        self.listLineRow[str(todoInfo)] = row
        listLayoutLine = self.getListLayoutLine(todoInfo, row)
        self.updateTabLayout(0, '전체', self.addTabTodoLayout(self.listLayoutLines, listLayoutLine, row))
        subject = todoInfo['subject']
        for index in range(1, len(self.subjectList)+1):
            if self.subjectTabs.tabText(index) == subject:
                self.updateSubjectTabLayout(index, subject, self.layout[subject][0],
                                            self.addTabTodoLayout(self.layout[subject][1], listLayoutLine, self.layout[subject][1].rowCount()))
                break

       # currList = copy.deepcopy(self.todo.getTodoList())
       # sortList = copy.deepcopy(self.todo.sortTodoList())
       # self.sortListLayout(currList, sortList)
        self.subjectTabs.setCurrentIndex(0)

    def todoTypeMajorChanged(self):
        self.todoType.clear()
        for types in self.todo.getType()[1 if self.todoTypeMajor.currentText() == '과제' else 2]:
            self.todoType.addItem(types)

    def todoProgChanged(self, value):
        self.todoProgValue = value
        self.todoProgNum.setText('{}%'.format(value))

    def getTodoInfo(self):
        self.todoInfo = {'subject': self.todoSubject.currentText(), 'typeMajor': self.todoTypeMajor.currentText(),
                         'types': self.todoType.currentText(), 'typeGroup': self.todoTypeGroup.currentText(),
                         'name': self.todoName.text(), 'dateMonth': self.todoDateMonth.currentText(),
                         'dateDay': self.todoDateDay.currentText(), 'prior': self.todoPrior.currentText(),
                         'memo': self.todoMemo.toPlainText(), 'prog': str(self.todoProgValue)}
        return self.todoInfo

    def getSubjectInfo(self):
        self.subjectInfo = {'name': self.subjectName.text(), 'types': self.subjectType.currentText(),
                       'credit': self.subjectCredit.text(), 'prof': self.subjectProf.text()}
        return self.subjectInfo


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    ex = ToDoList()
    ex.show()
    sys.exit(app.exec_())
