from linkpreview import link_preview
from webpreview import web_preview
from hackernews import get_top_stories_ids, get_story_from_id

import sys
import threading
from queue import Queue

from PyQt5.QtGui import QGuiApplication, QIcon, QColor
from PyQt5.QtQml import QQmlApplicationEngine, QQmlComponent
from PyQt5.QtCore import QObject, QUrl, Qt, QCoreApplication, QAbstractListModel, QModelIndex, QTimer, qsrand, qrand, QTime, pyqtSlot, pyqtSignal
from PyQt5.QtQuick import QQuickItem

def test_preview():
    data = get_top_stories()

    for (i, id) in enumerate(data):

        print('\n')
        print('########################################"')
        
        if i == 5: break

        story = get_story_from_id(id)
        print("Title: {} - by: {} - score: {} - URL: {}".format(story['title'], story['by'], story['score'], story['url']))

        preview = link_preview(story['url'])
        print("title: {} - description: {} - image: {}".format(preview.title, preview.description, preview.image))

        title, description, image = web_preview(story['url'], parser='lxml')
        print("title: {} - description: {} - image: {}".format(title, description, image))

class Data(object):
    def __init__(self, width=35, height=35, color=QColor("red"), title=None, image=None, author=None, url=None, description=None, point=None, comments=None):
        self._width = width
        self._height = height
        self._color = color
        self._title = title
        self._image = image
        self._author = author
        self._url = url
        self._description = description
        self._point = point
        self._comments = comments

    def width(self):
        return self._width

    def height(self):
        return self._height

    def color(self):
        return self._color

    def title(self):
        return self._title

    def image(self):
        return self._image

    def author(self):
        return self._author

    def url(self):
        return self._url

    def description(self):
        return self._description
    
    def point(self):
        return self._point

    def comments(self):
        return self._comments

class Model(QAbstractListModel):

    WidthRole = Qt.UserRole + 1
    HeightRole = Qt.UserRole + 2
    ColorRole = Qt.UserRole + 3
    TitleRole = Qt.UserRole + 4
    ImageRole = Qt.UserRole + 5
    AuthorRole = Qt.UserRole + 6
    UrlRole = Qt.UserRole + 7
    DescriptionRole = Qt.UserRole + 8
    PointRole = Qt.UserRole + 9
    CommentsRole = Qt.UserRole + 10

    _roles = {WidthRole: b"width", HeightRole: b"height", ColorRole: b"color", TitleRole:b"title",
        ImageRole:b"image", AuthorRole:b"author", UrlRole:b"url", DescriptionRole:b"description", 
        PointRole:b"point", CommentsRole:b"comments"}

    def __init__(self, parent=None):
        QAbstractListModel.__init__(self, parent)

        self._datas = []

    def addData(self, data):
        self.beginInsertRows(QModelIndex(), self.rowCount(), self.rowCount())
        self._datas.append(data)
        self.endInsertRows()

    def rowCount(self, parent=QModelIndex()):
        return len(self._datas)

    def data(self, index, role=Qt.DisplayRole):
        try:
            data = self._datas[index.row()]
        except IndexError:
            return QVariant()

        if role == self.WidthRole:
            return data.width()

        if role == self.HeightRole:
            return data.height()

        if role == self.ColorRole:
            return data.color()
        
        if role == self.TitleRole:
            return data.title()

        if role == self.ImageRole:
            return data.image()

        if role == self.AuthorRole:
            return data.author()
        
        if role == self.UrlRole:
            return data.url()
        
        if role == self.DescriptionRole:
            return data.description()

        if role == self.PointRole:
            return data.point()

        if role == self.CommentsRole:
            return data.comments()

        return QVariant()

    def roleNames(self):
        return self._roles

class HNFetcher(QObject):
    # Must be a class variable and not instance variable
    story_fetched = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.story_fetched.connect(self.onStoryFetched)
        self.stories_q = Queue()
        self.last_fetched_id_index = 0
        self.ids = None

    def fetchStories(self, how_much=10):
        count = 0
        if not self.ids:
            self.ids = get_top_stories_ids()
        for i in range(self.last_fetched_id_index, len(self.ids)):
            self.stories_q.put(get_story_from_id(self.ids[i]))
            self.story_fetched.emit()
            self.last_fetched_id = i
            count += 1
            if count == how_much: break

    @pyqtSlot()
    def onStoryFetched(self):
        if not self.stories_q.empty():
            story = self.stories_q.get()
            print(story)
            model.addData(Data(256, 144, QColor("#6e6e6e"), story['title'], 
                image="https://upload.wikimedia.org/wikipedia/commons/9/9a/Gull_portrait_ca_usa.jpg", 
                author=story['by'], url=story['url'], point=story['score'], comments=story['descendants']))

if __name__ == "__main__":
    QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app = QGuiApplication(sys.argv)
    app.setWindowIcon(QIcon("icon.png"))

    # Add engin
    engine = QQmlApplicationEngine()

    # add initial data
    model = Model()
    '''
    for i in range(30):
        model.addData(Data(256, 144, QColor("#6e6e6e"), "Test"))
    '''

    # And register it in the context of QML
    context = engine.rootContext()
    context.setContextProperty('myModel', model)

    # Load the qml file into the engine
    engine.load(QUrl.fromLocalFile("app.qml"))

    if len(engine.rootObjects()) == 0:
        sys.exit(-1)

    engine.quit.connect(app.quit)

    fetcher = HNFetcher()
    ## Launch thread to get data from HN
    x = threading.Thread(target=fetcher.fetchStories, args=(10,))
    x.start() 

    win = engine.rootObjects()[0]
    moreBtn = win.findChild(QObject, "more_btn")
    moreBtn.clicked.connect(fetcher.fetchStories)


    sys.exit(app.exec_())
