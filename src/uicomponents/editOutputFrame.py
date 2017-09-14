from PySide.QtGui import QLineEdit, QFrame, QLabel, QCheckBox, QVBoxLayout,\
    QHBoxLayout, QGridLayout
from PySide.QtCore import Qt
import SMG
from Configuration import get_config

configuration = get_config("config/config.json")

class UiEditOutputFrame(QFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.explanation          = QLabel('You can change the title here. Use commas as a separator for multiple edits.')

        self.preview              = QLabel(self)
        self.preview_text         = 'Darude - Sandstorm'

        self.update_preview()

        self.prepend_label        = QLabel('Before')
        self.prepend              = QLineEdit(self)
        self.prepend.setDisabled(False)
        self.prepend_checkbox     = QCheckBox(self)

        self.append_label         = QLabel('After')
        self.append               = QLineEdit(self)
        self.append_checkbox      = QCheckBox(self)

        self.filter_label         = QLabel('Filter')
        self.filter               = QLineEdit(self)
        self.filter_checkbox      = QCheckBox(self)

        self.replace_input_label  = QLabel('Replace')
        self.replace_input        = QLineEdit(self)
        self.replace_checkbox     = QCheckBox(self)

        self.replace_output_label = QLabel('With')
        self.replace_output       = QLineEdit(self)

        append_state  = bool(configuration['edit_output']['append_state'])
        prepend_state = bool(configuration['edit_output']['prepend_state'])
        filters_state = bool(configuration['edit_output']['filter_state'])
        replace_state = bool(configuration['edit_output']['replace_state'])

        append        = configuration['edit_output']['append']
        prepend       = configuration['edit_output']['prepend']
        filters       = configuration['edit_output']['filter']
        replace_in    = configuration['edit_output']['replace_in']
        replace_out   = configuration['edit_output']['replace_out']

        self.append.setText(append)
        self.prepend.setText(prepend)
        self.filter.setText(filters)
        self.replace_input.setText(replace_in)
        self.replace_output.setText(replace_out)

        if append_state:
            self.append_checkbox.setCheckState(Qt.CheckState.Checked)
        else:
            self.append_checkbox.setCheckState(Qt.CheckState.Unchecked)
            self.append.setDisabled(True)

        if prepend_state:
            self.prepend_checkbox.setCheckState(Qt.CheckState.Checked)
        else:
            self.prepend_checkbox.setCheckState(Qt.CheckState.Unchecked)
            self.prepend.setDisabled(True)

        if filters_state:
            self.filter_checkbox.setCheckState(Qt.CheckState.Checked)
        else:
            self.filter_checkbox.setCheckState(Qt.CheckState.Unchecked)
            self.filter.setDisabled(True)

        if replace_state:
            self.replace_checkbox.setCheckState(Qt.CheckState.Checked)
        else:
            self.replace_checkbox.setCheckState(Qt.CheckState.Unchecked)
            self.replace_input.setDisabled(True)
            self.replace_output.setDisabled(True)

        # layout
        self.mainLayout = QVBoxLayout(self)

        self.editLayout = QGridLayout()
        self.editLayout.addWidget(self.prepend_label,        0, 0)
        self.editLayout.addWidget(self.prepend,              0, 1)
        self.editLayout.addWidget(self.prepend_checkbox,     0, 2)

        self.editLayout.addWidget(self.append_label,         1, 0)
        self.editLayout.addWidget(self.append,               1, 1)
        self.editLayout.addWidget(self.append_checkbox,      1, 2)

        self.editLayout.addWidget(self.filter_label,         2, 0)
        self.editLayout.addWidget(self.filter,               2, 1)
        self.editLayout.addWidget(self.filter_checkbox,      2, 2)

        self.editLayout.addWidget(self.replace_input_label,  3, 0)
        self.editLayout.addWidget(self.replace_input,        3, 1)
        self.editLayout.addWidget(self.replace_checkbox,     3, 2)

        self.editLayout.addWidget(self.replace_output_label, 4, 0)
        self.editLayout.addWidget(self.replace_output,       4, 1)

        self.replaceOutputLayout = QHBoxLayout()
        self.replaceOutputLayout.addWidget(self.replace_output_label)
        self.replaceOutputLayout.addWidget(self.replace_output)

        self.mainLayout.addLayout(self.editLayout)
        self.mainLayout.addWidget(self.preview)
        self.mainLayout.addWidget(self.explanation)

        # signals
        self.append.           textChanged  .connect(self.append_to_title)
        self.prepend.          textChanged  .connect(self.prepend_to_title)
        self.filter.           textChanged  .connect(self.remove_from_title)
        self.replace_input.    textChanged  .connect(self.replace_in_title_input)
        self.replace_output.   textChanged  .connect(self.replace_in_title_output)

        self.append_checkbox.  stateChanged .connect(self.toggle_append)
        self.prepend_checkbox. stateChanged .connect(self.toggle_prepend)
        self.filter_checkbox.  stateChanged .connect(self.toggle_filter)
        self.replace_checkbox. stateChanged .connect(self.toggle_replace)


    def update_preview(self):
        self.preview.setText(SMG.smg.titleModifier.modify_title(self.preview_text))


    def append_to_title(self, string):
        configuration['edit_output']['append'] = str(string)
        configuration.save()
        self.update_preview()


    def prepend_to_title(self, string):
        configuration['edit_output']['prepend'] = str(string)
        configuration.save()
        self.update_preview()


    def remove_from_title(self, string):
        configuration['edit_output']['filter'] = str(string)
        configuration.save()
        self.update_preview()


    def replace_in_title_input(self, string):
        str_in = self.replace_input.text()
        str_out = self.replace_output.text()
        configuration['edit_output']['replace_in'] = str(string)
        configuration.save()

        try:
            if string[-1] == ',' and not (str_in.count(',') == str_out.count(',')):
                self.replace_output.setText(self.replace_output.text() + ', ')
        except IndexError:
            pass

        self.update_preview()


    def replace_in_title_output(self, string):
        str_in = self.replace_input.text()
        str_out = self.replace_output.text()
        configuration['edit_output']['replace_out'] = string
        configuration.save()

        try:
            if string[-1] == ',' and not (str_in.count(',') == str_out.count(',')):
                self.replace_input.setText(self.replace_input.text() + ', ')
        except IndexError:
            pass

        self.update_preview()


    def toggle_append(self, state):
        self.append.setDisabled(not state)
        configuration['edit_output']['append_state'] = bool(state)
        configuration.save()
        SMG.smg.titleModifier.toggles_have_changed()
        self.update_preview()


    def toggle_prepend(self, state):
        self.prepend.setDisabled(not state)
        configuration['edit_output']['prepend_state'] = bool(state)
        configuration.save()
        self.update_preview()
        SMG.smg.titleModifier.toggles_have_changed()


    def toggle_filter(self, state):
        self.filter.setDisabled(not state)
        configuration['edit_output']['filter_state'] = bool(state)
        configuration.save()
        SMG.smg.titleModifier.toggles_have_changed()
        self.update_preview()


    def toggle_replace(self, state):
        self.replace_input.setDisabled(not state)
        self.replace_output.setDisabled(not state)
        configuration['edit_output']['replace_state'] = bool(state)
        configuration.save()
        SMG.smg.titleModifier.toggles_have_changed()
        self.update_preview()
