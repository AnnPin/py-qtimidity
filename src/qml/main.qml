import QtQuick 2.7 as QtQuick2
import QtQuick.Controls 2.2 as Controls2
import QtQuick.Layouts 1.3 as Layouts
import Qt.labs.platform 1.0 as Platform
import QtQuick.Dialogs 1.1 as Dialogs

Controls2.ApplicationWindow {
    id: mainWindow
    visible: true
    width: 400
    height: 140
    minimumWidth: 400
    minimumHeight: 140
    title: qsTr("PyQTimidity")

    Preferences{
        id: preferencesWindow
        visible: false
    }

    Dialogs.FileDialog {
        id: fileOpenDialog
        objectName: "fileOpenDialog"
        title: "Please choose a midi file"
        nameFilters: [ "MIDI files (*.mid *.midi)", "All files (*)" ]
        selectFolder: false
        selectMultiple: false
        onAccepted: {
            timidity.inport_midi_file(fileOpenDialog.fileUrl)
            timidity.set_volume(volumeSlider.value)

            rewindButton.enabled = true
            playPauseButton.enabled = true
            fastFeedButton.enabled = true
            timeSlider.enabled = true
            exportMenuItem.enabled = true
        }
        onRejected: { /* Qt.quit() */ }
        // QtQuick2.Component.onCompleted: visible = true
    }

    Dialogs.FileDialog {
        id: waveExportDialog
        objectName: "waveExportDialog"
        title: "Please select the output file name"
        nameFilters: [ "WAV files (*.wav *.wave)", "All files (*)" ]
        selectFolder: false
        selectMultiple: false
        selectExisting: false
        onAccepted: {
            timidity.export_wave_file(waveExportDialog.fileUrl)
        }
        onRejected: {
        }
    }

    Platform.MenuBar {
        id: menuBar

        Platform.Menu {
            Platform.MenuItem {
                id: preferencesItem
                objectName: "preferencesItem"
                text: qsTr("Preferences")
                role: Platform.MenuItem.PreferencesRole
                onTriggered: {
                    // TODO
                    // Load soundfont
                    // Load config file
                    preferencesWindow.visible = true
                }
            }
        }


        Platform.Menu {
            id: fileMenu
            title: qsTr("File")

            Platform.MenuItem {
                id: openMenuItem
                objectName: "openMenuItem"
                text: qsTr("Open")
                shortcut: "Ctrl+O"
                onTriggered: {
                    fileOpenDialog.open()
                }
            }

            Platform.MenuItem {
                id: exportMenuItem
                objectName: "exportMenuItem"
                text: qsTr("Export as WAV")
                shortcut: "Ctrl+Shift+E"
                enabled: false
                onTriggered: {
                    waveExportDialog.open()
                }
            }
        }

        Platform.Menu {
            id: playbackMenu
            title: qsTr("Playback")

            Platform.MenuItem {
                id: loopItem
                objectName: "loopItem"
                text: qsTr("Enable loop")
                shortcut: "Ctrl+Alt+L"
                onTriggered: {
                    timidity.toggle_loop()
                }
            }
        }

        Platform.Menu {
            id: helpMenu
            title: qsTr("&Help")

            Platform.MenuItem {
                text: qsTr("Check GitHub repository")
                onTriggered: {
                    Qt.openUrlExternally("https://github.com/AnnPin/py-qtimidity")
                }
            }
        }
    }

    Layouts.ColumnLayout {
        id: columnLayout
        anchors.rightMargin: 10
        anchors.leftMargin: 10
        anchors.bottomMargin: 0
        anchors.topMargin: 0
        anchors.fill: parent

        Layouts.RowLayout {
            id: rowLayout
            width: 100
            height: 100
            Layouts.Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter

            QtQuick2.Text {
                id: currentTime
                text: qsTr("00:00")
                font.pixelSize: 12
            }

            Controls2.Slider {
                id: timeSlider
                Layouts.Layout.fillWidth: true
                enabled: false
                from: 0
                to: 0
                stepSize: 1
                snapMode: Controls2.Slider.SnapAlways
                value: 0
                onMoved: {
                    timidity.set_position(timeSlider.value)
                }
            }

            QtQuick2.Text {
                id: endTime
                text: qsTr("00:00")
                font.pixelSize: 12
            }
        }

        Layouts.RowLayout {
            id: rowLayout1
            width: 100
            height: 100
            spacing: 10
            Layouts.Layout.fillWidth: false
            Layouts.Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter

            Controls2.Button {
                id: rewindButton
                text: qsTr("<<")
                enabled: false
                onClicked: {
                    rewindButton.focus = false
                    timidity.set_position(timeSlider.value - 10000)
                }

                QtQuick2.Shortcut {
                    sequence: "Left"
                    autoRepeat: false
                    context: Qt.ApplicationShortcut
                    onActivated: {
                        timidity.set_position(timeSlider.value - 10000)
                    }
                }
            }

            Controls2.Button {
                id: playPauseButton
                text: qsTr("Play/Pause")
                enabled: false
                onClicked: {
                    playPauseButton.focus = false
                    timidity.play_pause_button_clicked()
                }
                focus: false

                QtQuick2.Shortcut {
                    sequence: "Space"
                    autoRepeat: false
                    context: Qt.ApplicationShortcut
                    onActivated: {
                        timidity.play_pause_button_clicked()
                    }
                }
            }

            Controls2.Button {
                id: fastFeedButton
                text: qsTr(">>")
                enabled: false
                onClicked: {
                    fastFeedButton.focus = false
                    timidity.set_position(timeSlider.value + 10000)
                }

                QtQuick2.Shortcut {
                    sequence: "Right"
                    autoRepeat: false
                    context: Qt.ApplicationShortcut
                    onActivated: {
                        timidity.set_position(timeSlider.value + 10000)
                    }
                }
            }
        }

        Layouts.RowLayout {
            id: rowLayout2
            width: 100
            height: 100
            Layouts.Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter

            Controls2.Slider {
                id: volumeSlider
                Layouts.Layout.fillWidth: true
                from: 0
                to: 100
                stepSize: 1
                snapMode: Controls2.Slider.SnapAlways
                value: 100
                onValueChanged: {
                    timidity.set_volume(volumeSlider.value)
                }

                QtQuick2.Shortcut {
                    sequence: "Up"
                    autoRepeat: false
                    context: Qt.ApplicationShortcut
                    onActivated: {
                        volumeSlider.value = volumeSlider.value + 10
                    }
                }
                QtQuick2.Shortcut {
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

    QtQuick2.Connections {
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
