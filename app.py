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
    def __init__(self, width=35, height=35, color=QColor("red"), title=None, image=None, url=None, description=None):
        self._width = width
        self._height = height
        self._color = color
        self._title = title
        self._image = image
        self._url = url
        self._description = description

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

    def url(self):
        return self._url

    def description(self):
        return self._description

class Model(QAbstractListModel):

    WidthRole = Qt.UserRole + 1
    HeightRole = Qt.UserRole + 2
    ColorRole = Qt.UserRole + 3
    TitleRole = Qt.UserRole + 4
    ImageRole = Qt.UserRole + 5
    UrlRole = Qt.UserRole + 6
    DescriptionRole = Qt.UserRole + 7

    _roles = {WidthRole: b"width", HeightRole: b"height", ColorRole: b"color", TitleRole:b"title",
        ImageRole:b"image", UrlRole:b"url", DescriptionRole:b"description"}

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
        
        if role == self.UrlRole:
            return data.url()
        
        if role == self.DescriptionRole:
            return data.description()

        return QVariant()

    def roleNames(self):
        return self._roles

def HNFetcher(QObject):
    def __init__(self):
        super().__init__()
        self.story_fetched = pyqtSignal()

    def fetchStories(self, q):
        ids = get_top_stories_ids()
        for _id in ids:
            q.put(get_story_from_id(id))
            story_fetched.emit()

    @pyqtSlot()
    def onStoryFetched():
        if not q.empty():
            story = q.get()
            model.model.addData(Data(256, 144, QColor("#6e6e6e"), story['title']))

if __name__ == "__main__":
    QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app = QGuiApplication(sys.argv)
    #app.setWindowIcon(QIcon("icon.png"))

    # Add engin
    engine = QQmlApplicationEngine()

    # add initial data
    model = Model()
    for i in range(30):
        model.addData(Data(256, 144, QColor("#6e6e6e"), "Test"))

    # And register it in the context of QML
    context = engine.rootContext()
    context.setContextProperty('myModel', model)

    # Load the qml file into the engine
    engine.load(QUrl.fromLocalFile("app.qml"))

    if len(engine.rootObjects()) == 0:
        sys.exit(-1)

    engine.quit.connect(app.quit)

    ## Launch thread to get data from HN
    # Doesn't work because we try to access GUI from another thread
    #x = threading.Thread(target=fetchAndAdd, args=(model,))
    #x.start()
    #fetcher = HNFetcher()
    #fetcher.story_fetched.connect(fetcher.onStoryFetched)

    stories_q = Queue()
    #x = threading.Thread(target=fetcher.fetchStories, args=(stories_q,))
    #x.start() 

    sys.exit(app.exec_())
