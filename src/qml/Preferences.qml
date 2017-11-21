import QtQuick 2.0
import QtQuick.Window 2.3
import QtQuick.Controls 2.2
import QtQuick.Layouts 1.3

ApplicationWindow {
    id: preferencesWindow
    width: 600
    height: 200
    minimumWidth: 600
    minimumHeight: 200
    visible: true
    title: "Preferences"

    header: TabBar {
        id: preferencesTabBar
        width: parent.width
        TabButton {
            text: qsTr("Load SoundFont")
        }

        TabButton {
            text: qsTr("Load timidty.cfg")
        }

        TabButton {
            text: qsTr("Load default timidty.cfg")
        }
    }

    StackLayout {
        anchors.fill: parent
        currentIndex: preferencesTabBar.currentIndex
        Item {
            id: sfTab

            ColumnLayout {
                id: sfTabColumnLayout
                anchors.topMargin: 10
                anchors.rightMargin: 10
                anchors.leftMargin: 10
                anchors.fill: parent

                RowLayout {
                    id: sfLabelLayout
                    width: 100
                    height: 100
                    Layout.fillWidth: true

                    Text {
                        id: sfLabel
                        text: "Select the SoundFont file to load."
                    }
                }

                RowLayout {
                    id: sfTabFieldLayout
                    width: 100
                    height: 100
                    Layout.fillWidth: true

                    TextField {
                        id: sfFilePath
                        text: qsTr("")
                        placeholderText: "Path to your SoundFont file..."
                        Layout.fillWidth: true
                    }

                    Button {
                        id: sfSearchButton
                        text: qsTr("Search")
                    }
                }

                RowLayout {
                    id: sfTabButtonsLayout
                    width: 100
                    height: 100
                    Layout.alignment: Qt.AlignRight | Qt.AlignVCenter

                    Button {
                        id: sfOkButton
                        text: qsTr("OK")
                    }

                    Button {
                        id: sfCancelButton
                        text: qsTr("Cancel")
                    }
                }
            }

        }

        Item {
            id: cfgTab
            ColumnLayout {
                id: cfgTabColumnLayout
                anchors.topMargin: 10
                anchors.rightMargin: 10
                anchors.leftMargin: 10
                anchors.fill: parent

                RowLayout {
                    id: cfgLabelLayout
                    width: 100
                    height: 100
                    Layout.fillWidth: true

                    Text {
                        id: cfgLabel
                        text: "Select the timidity.cfg file to load."
                    }
                }

                RowLayout {
                    id: cfgTabFieldLayout
                    width: 100
                    height: 100
                    Layout.fillWidth: true

                    TextField {
                        id: cfgFilePath
                        text: qsTr("")
                        placeholderText: "Path to your timidity.cfg file..."
                        Layout.fillWidth: true
                    }

                    Button {
                        id: cfgSearchButton
                        text: qsTr("Search")
                    }
                }

                RowLayout {
                    id: cfgTabButtonsLayout
                    width: 100
                    height: 100
                    Layout.alignment: Qt.AlignRight | Qt.AlignVCenter

                    Button {
                        id: cfgOkButton
                        text: qsTr("OK")
                    }

                    Button {
                        id: cfgCancelButton
                        text: qsTr("Cancel")
                    }
                }
            }

        }

        Item {
            id: defaultCfgTab
            ColumnLayout {
                id: defaultCfgTabColumnLayout
                anchors.topMargin: 10
                anchors.rightMargin: 10
                anchors.leftMargin: 10
                anchors.fill: parent

                RowLayout {
                    id: defaultCfgLabelLayout
                    width: 100
                    height: 100
                    Layout.fillWidth: true

                    Text {
                        id: defaultCfgLabel
                        text: "Click OK to load default timidity.cfg."
                    }
                }

                RowLayout {
                    id: defaultCfgTabButtonsLayout
                    width: 100
                    height: 100
                    Layout.alignment: Qt.AlignRight | Qt.AlignVCenter

                    Button {
                        id: defaultCfgOkButton
                        text: qsTr("OK")
                    }

                    Button {
                        id: defaultCfgCancelButton
                        text: qsTr("Cancel")
                    }
                }
            }
        }
    }
}
