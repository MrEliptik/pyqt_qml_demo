import QtQuick 2.5
import QtQuick.Window 2.2
import QtQuick.Controls 1.4
import QtQuick.Layouts 1.2
 
ApplicationWindow {
    visible: true
    width: Screen.width/2
    height: Screen.height/2
    title: qsTr("Hacker News Fetcher")
    color: "whitesmoke"
    id: stories
 
    
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
        width: Screen.width/2
        height: Screen.height/2
        ScrollBar.horizontal.policy: ScrollBar.AlwaysOff
        ScrollBar.vertical.policy: ScrollBar.AsNeeded
        
        Grid {
            columns: 4
            spacing: 9
            Repeater{
                model:myModel
                delegate: storyDelegate
            }
        }
    }
}