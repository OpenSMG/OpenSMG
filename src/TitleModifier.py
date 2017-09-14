class TitleModifier():
    def __init__(self, configuration):
        # keep a reference to the config object
        self.configuration = configuration
        self.toggles_have_changed()

        # QlineEdit input boxes do not transform characters like "\n" into actual newlines
        # Instead, a literal "\n" gets outputted.
        # Inside python however, the literal string "\n" is represented as "\\n".
        # This dictionary defines replacements for strings like newlines, and perhaps later other characters
        # that need to be replaced with other special characters (tabs for example)
        self.replacement_characters = {
            "\\n": "\n",
            # perhaps regex would fare a little bit better against single tags instead of this mess
            "<br>": "\n",
            "<br />": "\n",
            "<br/>": "\n"
        }

    def toggles_have_changed(self):
        """ Updates the <TitleModifier>'s internal state of what title modifiers are currently on and off"""

        # yes, 'True' should definitely NOT be a string. but because of a huge battle between me and
        # .ini configuration files, it has ended up that bools are being saved as "True" or something stupid like that.
        self.append_state  = self.configuration['edit_output']['append_state']
        self.prepend_state = self.configuration['edit_output']['prepend_state']
        self.filter_state  = self.configuration['edit_output']['filter_state']
        self.replace_state = self.configuration['edit_output']['replace_state']

    def get_modifiers(self, which_string):
        # a shorthand for `configuration.get('edit_output', 'whatever').split(',')
        # because I'm nice, it also takes care of replacing special characters with their intended meaning
        # eg, \n or <br> written in the QLineEdit becomes an actual newline

        modifier_list = self.configuration['edit_output'][which_string].split(',')

        for key, value in self.replacement_characters.items():
            modifier_list = [string.replace(key, value) for string in modifier_list]

        return modifier_list

    def modify_title(self, title):
        """
        Used to transform a piece of text using user-defined behaviors.
        handles prepending and appending text, as well as filtering and replacing.
        """

        if self.append_state:
            append = self.get_modifiers('append')
            for string in append:
                title += string

        if self.prepend_state:
            prepend = self.get_modifiers('prepend')
            for string in prepend:
                title = string + title

        if self.filter_state:
            filters = self.get_modifiers('filter')
            for string in filters:
                title = title.replace(string, '')

        if self.replace_state:
            replace_in = self.get_modifiers('replace_in')
            replace_out = self.get_modifiers('replace_out')
            for (string_in, string_out) in zip(replace_in, replace_out):
                title = title.replace(string_in, string_out)

        return title
