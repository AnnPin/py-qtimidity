import QtQuick 2.7
import QtQuick.Window 2.3
import QtQuick.Controls 2.2
import QtQuick.Layouts 1.3
import QtQuick.Dialogs 1.1

ApplicationWindow {
    id: preferencesWindow
    width: 600
    height: 200
    minimumWidth: 600
    minimumHeight: 200
    visible: true
    title: "Preferences"

    Shortcut {
        sequence: "Esc"
        autoRepeat: false
        context: Qt.ApplicationShortcut
        onActivated: {
            preferencesWindow.visible = false
        }
    }

    FileDialog {
        id: sfOpenDialog
        objectName: "sfOpenDialog"
        title: "Please choose a SoundFont file"
        nameFilters: [ "SoundFont files (*.sf2)", "All files (*)" ]
        selectFolder: false
        selectMultiple: false
        onAccepted: {
            var filePath = sfOpenDialog.fileUrl.toString().replace(/^file:\/\//, "")
            sfFilePath.text = qsTr(filePath)
        }
        onRejected: {
        }
    }

    FileDialog {
        id: cfgOpenDialog
        objectName: "cfgOpenDialog"
        title: "Please choose a timidity.cfg file"
        nameFilters: [ "timidity.cfg files (*.cfg)", "All files (*)" ]
        selectFolder: false
        selectMultiple: false
        onAccepted: {
            var filePath = cfgOpenDialog.fileUrl.toString().replace(/^file:\/\//, "")
            cfgFilePath.text = qsTr(filePath)
        }
        onRejected: {
        }
    }

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
                        selectByMouse: true
                        Layout.fillWidth: true
                    }

                    Button {
                        id: sfSearchButton
                        text: qsTr("Search")
                        onClicked: {
                            sfOpenDialog.open()
                        }
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
                        onClicked: {
                            app_core.set_timidity_config("sf", sfFilePath.text)
                            preferencesWindow.visible = false
                        }
                    }

                    Button {
                        id: sfCancelButton
                        text: qsTr("Cancel")
                        onClicked: {
                            preferencesWindow.visible = false
                        }
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
                        selectByMouse: true
                        Layout.fillWidth: true
                    }

                    Button {
                        id: cfgSearchButton
                        text: qsTr("Search")
                        onClicked: {
                            cfgOpenDialog.open()
                        }
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
                        onClicked: {
                            app_core.set_timidity_config("cfg", cfgFilePath.text)
                            preferencesWindow.visible = false
                        }
                    }

                    Button {
                        id: cfgCancelButton
                        text: qsTr("Cancel")
                        onClicked: {
                            preferencesWindow.visible = false
                        }
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
                        onClicked: {
                            app_core.set_timidity_config("default", "")
                            preferencesWindow.visible = false
                        }
                    }

                    Button {
                        id: defaultCfgCancelButton
                        text: qsTr("Cancel")
                        onClicked: {
                            preferencesWindow.visible = false
                        }
                    }
                }
            }
        }
    }
}
