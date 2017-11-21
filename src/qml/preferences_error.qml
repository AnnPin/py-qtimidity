import QtQuick 2.7
import QtQuick.Dialogs 1.1

MessageDialog {
    id: preferencesErrorDialog
    title: "PyQTimidity"
    icon: StandardIcon.Critical
    text: "Error: Invalid `preferences.json` format."
    standardButtons: StandardButton.Ok
    onAccepted: {
        Qt.quit()
    }
    Component.onCompleted: visible = true
}
