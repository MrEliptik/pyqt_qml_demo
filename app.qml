import QtQuick 2.5
import QtQuick.Window 2.2
import QtQuick.Controls 2.2
import QtQuick.Layouts 1.2
 
ApplicationWindow {
    visible: true
    width: Screen.width/2
    height: Screen.height/2
    title: qsTr("Hacker News Fetcher")
    color: "#202121"
    id: window

    
    Component {
        id: storyDelegate
        Column{
            Text{
                text: model.title
            } 
            Rectangle{
                height: model.height
                width: model.width
                color: model.color
            }
        }
        
    }

    ScrollView{
        width: parent.width
        height: parent.height

        Grid {
            columns: 4
            spacing: 9
            horizontalItemAlignment: Grid.AlignHCenter
            verticalItemAlignment : Grid.AlignVCenter
            Repeater{
                model:myModel
                delegate: storyDelegate
            }
        }
    }
}