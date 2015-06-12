import sublime, sublime_plugin
import re, os, os.path

class TabstashCommand(sublime_plugin.WindowCommand):

    def run(self):
        filename_list = []
        for openedfile in self.window.views():
            filename_list.append(openedfile.file_name())
            # self.window.run_command('close_file')
            self.new_stash_obj = {
                "name" : '',
                "files" : filename_list
            }
            if len(filename_list) > 0:
                self.window.show_input_panel("Stash Name:","", self.save_stash_name, None, None)
            else:
                sublime.message_dialog("No tabs to stash at the time")

    def save_stash_name(self, stash):
        default_settings = sublime.load_settings("Tabstasher.sublime-settings")
        self.new_stash_obj['name'] = stash
        default_stashes = default_settings.get('stashes')
        default_stashes.append(self.new_stash_obj)
        default_settings.set('stashes',default_stashes)
        self.window.run_command('close_all')

class TabunstashCommand(sublime_plugin.WindowCommand):

    def run(self):
        default_settings = sublime.load_settings("Tabstasher.sublime-settings")
        if default_settings.has('stashes'):
            self.array_of_stashes = default_settings.get('stashes')
            array_of_stashes_names = []
            for stash in self.array_of_stashes:
                array_of_stashes_names.append(stash['name'])
            self.window.show_quick_panel(array_of_stashes_names, self.on_done)

    def on_done(self, picked):
        for stashedFile in self.array_of_stashes[picked]['files']:
            self.window.open_file(stashedFile)

class TabdeletestashCommand(sublime_plugin.WindowCommand):

    def run(self):
        self.default_settings = sublime.load_settings("Tabstasher.sublime-settings")
        if self.default_settings.has('stashes'):
            self.array_of_stashes = self.default_settings.get('stashes')
            array_of_stashes_names = []
            for stash in self.array_of_stashes:
                array_of_stashes_names.append(stash['name'])
            self.window.show_quick_panel(array_of_stashes_names, self.on_done)

    def on_done(self, picked):
        del self.array_of_stashes[picked]
        self.default_settings.set('stashes',self.array_of_stashes)

class TabclearstashCommand(sublime_plugin.WindowCommand):

    def run(self):
        self.default_settings = sublime.load_settings("Tabstasher.sublime-settings")
        if self.default_settings.has('stashes'):
            self.default_settings.erase('stashes')