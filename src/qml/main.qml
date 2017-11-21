import QtQuick 2.7
import QtQuick.Controls 2.2
import QtQuick.Layouts 1.3
import Qt.labs.platform 1.0
import QtQuick.Window 2.0
import QtQuick.Dialogs 1.1

ApplicationWindow {
    id: mainWindow
    visible: true
    width: 400
    height: 140
    minimumWidth: 400
    minimumHeight: 140
    title: qsTr("PyQTimidity")

    FileDialog {
        id: fileOpenDialog
        objectName: "fileOpenDialog"
        title: "Please choose a midi file"
        nameFilters: [ "MIDI files (*.mid *.midi)", "All files (*)" ]
        selectFolder: false
        selectMultiple: false
        onAccepted: {
            timidity.exec_timidity(fileOpenDialog.fileUrl)
            timidity.set_volume(volumeSlider.value)

            rewindButton.enabled = true
            playPauseButton.enabled = true
            fastFeedButton.enabled = true
            timeSlider.enabled = true
        }
        onRejected: { /* Qt.quit() */ }
        // Component.onCompleted: visible = true
    }

    MenuBar {
        id: menuBar

        Menu {
            id: fileMenu
            title: qsTr("File")

            MenuItem {
                id: openMenuItem
                objectName: "openMenuItem"
                text: qsTr("Open")
                shortcut: "Ctrl+O"
                onTriggered: {
                    fileOpenDialog.open()
                }
            }
        }

        Menu {
            id: playbackMenu
            title: qsTr("Playback")

            MenuItem {
                id: loopItem
                objectName: "loopItem"
                text: qsTr("Enable loop")
                shortcut: "Ctrl+Alt+L"
                onTriggered: {
                    timidity.toggle_loop()
                }
            }
        }

        Menu {
            id: helpMenu
            title: qsTr("&Help")

            MenuItem {
                text: qsTr("Check GitHub repository")
                onTriggered: {
                    Qt.openUrlExternally("https://github.com/AnnPin/py-qtimidity")
                }
            }
        }
    }

    ColumnLayout {
        id: columnLayout
        anchors.rightMargin: 10
        anchors.leftMargin: 10
        anchors.bottomMargin: 0
        anchors.topMargin: 0
        anchors.fill: parent

        RowLayout {
            id: rowLayout
            width: 100
            height: 100
            Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter

            Text {
                id: currentTime
                text: qsTr("00:00")
                font.pixelSize: 12
            }

            Slider {
                id: timeSlider
                Layout.fillWidth: true
                enabled: false
                from: 0
                to: 0
                stepSize: 1
                snapMode: Slider.SnapAlways
                value: 0
                onMoved: {
                    timidity.set_position(timeSlider.value)
                }
            }

            Text {
                id: endTime
                text: qsTr("00:00")
                font.pixelSize: 12
            }
        }

        RowLayout {
            id: rowLayout1
            width: 100
            height: 100
            spacing: 10
            Layout.fillWidth: false
            Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter

            Button {
                id: rewindButton
                text: qsTr("<<")
                enabled: false
                onClicked: {
                    rewindButton.focus = false
                    timidity.set_position(timeSlider.value - 10000)
                }

                Shortcut {
                    sequence: "Left"
                    autoRepeat: false
                    context: Qt.ApplicationShortcut
                    onActivated: {
                        timidity.set_position(timeSlider.value - 10000)
                    }
                }
            }

            Button {
                id: playPauseButton
                text: qsTr("Play/Pause")
                enabled: false
                onClicked: {
                    playPauseButton.focus = false
                    timidity.play_pause_button_clicked()
                }
                focus: false

                Shortcut {
                    sequence: "Space"
                    autoRepeat: false
                    context: Qt.ApplicationShortcut
                    onActivated: {
                        timidity.play_pause_button_clicked()
                    }
                }
            }

            Button {
                id: fastFeedButton
                text: qsTr(">>")
                enabled: false
                onClicked: {
                    fastFeedButton.focus = false
                    timidity.set_position(timeSlider.value + 10000)
                }

                Shortcut {
                    sequence: "Right"
                    autoRepeat: false
                    context: Qt.ApplicationShortcut
                    onActivated: {
                        timidity.set_position(timeSlider.value + 10000)
                    }
                }
            }
        }

        RowLayout {
            id: rowLayout2
            width: 100
            height: 100
            Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter

            Slider {
                id: volumeSlider
                Layout.fillWidth: true
                from: 0
                to: 100
                stepSize: 1
                snapMode: Slider.SnapAlways
                value: 100
                onValueChanged: {
                    timidity.set_volume(volumeSlider.value)
                }

                Shortcut {
                    sequence: "Up"
                    autoRepeat: false
                    context: Qt.ApplicationShortcut
                    onActivated: {
                        volumeSlider.value = volumeSlider.value + 10
                    }
                }
                Shortcut {
                    sequence: "Down"
                    autoRepeat: false
                    context: Qt.ApplicationShortcut
                    onActivated: {
                        volumeSlider.value = volumeSlider.value - 10
                    }
                }

            }
        }
    }

    Connections {
        target: timidity

        onSetFilenameLabel: {
            mainWindow.title = qsTr("PyQTimidity - " + newFilenameLabel)
        }

        onSetNewCurrentTimeLabel: {
            currentTime.text = qsTr(newCurrentTimeLabel)
        }

        onSetNewEndTimeLabel: {
            endTime.text = qsTr(newEndTimeLabel)
        }

        onSetNewCurrentTime: {
            timeSlider.value = newCurrentTime
        }

        onSetNewEndTime: {
            timeSlider.to = newEndTime
        }

        onSetLoopLabel: {
            loopItem.text = qsTr(newLoopLabel)
        }
    }
}
