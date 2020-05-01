import QtQuick 2.14
import QtQuick.Window 2.2
import QtQuick.Controls 2.4
import QtQuick.Controls.Material 2.4
import Qt.labs.platform 1.0
import QtQuick.Layouts 1.2
 
ApplicationWindow {
    visible: true
    width: Screen.width/3
    height: Screen.height/2
    title: qsTr("Hacker News Fetcher")
    color: "#202121"
    id: window

    header: ToolBar {
        width: parent.width
        anchors.horizontalCenter: parent.horizontalCenter

        leftPadding: 8
        Material.elevation: 4
        background: Rectangle {
            implicitWidth: parent.width
            implicitHeight: parent.height
            border.color: "#999"
            color: "#CC5200" 
        }

        RowLayout {
            id: fileRow
            anchors.fill: parent
            
            ToolButton {
                id: topBtn
                text: "Top" // icon-doc-text-inv-1
                focusPolicy: Qt.TabFocus
                onClicked: mainController.menuController.newFileClicked();
                MouseArea {
                    anchors.fill: parent
                    hoverEnabled: true
                    cursorShape: Qt.PointingHandCursor
                }
                //backgroundColor: "#999"
            }
            ToolButton {
                id: newsBtn
                text: "News" // icon-doc-text-inv-1
                focusPolicy: Qt.TabFocus
                onClicked: mainController.menuController.newFileClicked();
                MouseArea {
                    anchors.fill: parent
                    hoverEnabled: true
                    cursorShape: Qt.PointingHandCursor
                }
                //backgroundColor: "#999"
            }
            ToolButton {
                id: bestBtn
                text: "Best" // icon-doc-text-inv-1
                focusPolicy: Qt.TabFocus
                onClicked: mainController.menuController.newFileClicked();
                MouseArea {
                    anchors.fill: parent
                    hoverEnabled: true
                    cursorShape: Qt.PointingHandCursor
                }
                //backgroundColor: "#999"
            }
            ToolButton {
                id: askBtn
                text: "Ask" // icon-folder
                focusPolicy: Qt.TabFocus
                onClicked: openDialog.open()
                MouseArea {
                    anchors.fill: parent
                    hoverEnabled: true
                    cursorShape: Qt.PointingHandCursor
                }
                //backgroundColor: "#999"
            }
            ToolButton {
                id: showBtn
                text: "Show" // icon-floppy
                focusPolicy: Qt.TabFocus
                onClicked: saveDialog.open()
                MouseArea {
                    anchors.fill: parent
                    hoverEnabled: true
                    cursorShape: Qt.PointingHandCursor
                }
                //backgroundColor: "#999"
            }
            ToolButton {
                id: jobBtn
                text: "Job" // icon-floppy
                focusPolicy: Qt.TabFocus
                onClicked: saveDialog.open()
                MouseArea {
                    anchors.fill: parent
                    hoverEnabled: true
                    cursorShape: Qt.PointingHandCursor
                }
                //backgroundColor: "#999"
            }
        }

        /*    
        Shortcut {
            id: openShortcut
            sequence: StandardKey.Open
            onActivated: 
        }
        */
    }

    Component {
        id: storyDelegate
        Rectangle{
            width: 260
            height: 180
            color: "black"
            border.color: "white"
            Column{
                leftPadding: 2
                Text{ text: model.title; color: "white" ; wrapMode: Text.WordWrap ; anchors.horizontalCenter: parent.horizontalCenter } 
                /*
                Rectangle{
                    height: model.height
                    width: model.width
                    color: model.color
                }*/
                Image {
                    source: model.image
                    fillMode: Image.PreserveAspectCrop
                    clip: true
                    width: 256
                    height: 144
                    MouseArea {
                        anchors.fill: parent
                        hoverEnabled: true
                        onClicked: { Qt.openUrlExternally(model.url);}
                        cursorShape: Qt.PointingHandCursor
                    }
                }
                Row{
                    anchors.horizontalCenter: parent.horizontalCenter
                    Text{ text: model.point + " points"; color: "white" }  
                    Text{ text: "by " + model.author; color: "white"; font.bold: true; leftPadding: 2} 
                    Text{ text: "|"; color: "white"; leftPadding: 2}
                    Text{ text: model.comments + " comments"; color: "white"; leftPadding: 2 } 
                }
            }
            
        }  
    }

    ScrollView{
        width: parent.width
        height: parent.height
        padding: 25

        ColumnLayout {
            anchors.horizontalCenter: parent.horizontalCenter
            GridLayout {
                id: grid
                columns: window.width / 256
                columnSpacing: 15
                rowSpacing: 15
                //anchors.fill: parent;
                //horizontalItemAlignment: Grid.AlignHCenter
                //verticalItemAlignment : Grid.AlignVCenter

                Repeater{
                    model:myModel
                    delegate: storyDelegate
                }    
            }

            Button {
                anchors.horizontalCenter: parent.horizontalCenter
                id: moreBtn
                objectName: "more_btn"
                text: "More" // icon-doc-text-inv-1
                focusPolicy: Qt.TabFocus
                onClicked: mainController.menuController.newFileClicked();
                MouseArea {
                    anchors.fill: parent
                    hoverEnabled: true
                    cursorShape: Qt.PointingHandCursor
                }
            }
        }
    }
}