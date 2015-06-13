import sublime, sublime_plugin
import re, os, os.path, subprocess

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
        subprocess.call('git stash save tabstasher' + stash, shell=True)
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
        if picked >= 0:
            self.window.run_command('close_all')
            for stashedFile in self.array_of_stashes[picked]['files']:
                self.window.open_file(stashedFile)
            subprocess.call('git stash apply --tabstasher' + self.array_of_stashes[picked]['name'], shell=True)

class TabpoplaststashCommand(sublime_plugin.WindowCommand):

    def run(self):
        default_settings = sublime.load_settings("Tabstasher.sublime-settings")
        if default_settings.has('stashes'):
            self.window.run_command('close_all')
            array_of_stashes = default_settings.get('stashes')
            for stashedFile in array_of_stashes[-1]['files']:
                self.window.open_file(stashedFile)
            subprocess.call('git stash pop --tabstasher'+array_of_stashes[-1]['name'], shell=True)
            del array_of_stashes[-1]
            default_settings.set('stashes',array_of_stashes)

class TabpopstashCommand(sublime_plugin.WindowCommand):

    def run(self):
        self.default_settings = sublime.load_settings("Tabstasher.sublime-settings")
        if self.default_settings.has('stashes'):
            self.array_of_stashes = self.default_settings.get('stashes')
            array_of_stashes_names = []
            for stash in self.array_of_stashes:
                array_of_stashes_names.append(stash['name'])
            self.window.show_quick_panel(array_of_stashes_names, self.on_done)

    def on_done(self, picked):
        if picked >= 0:
            self.window.run_command('close_all')
            for stashedFile in self.array_of_stashes[picked]['files']:
                self.window.open_file(stashedFile)
            subprocess.call('git stash pop --tabstasher'+array_of_stashes[picked]['name'], shell=True)
            del self.array_of_stashes[picked]
            self.default_settings.set('stashes',self.array_of_stashes)


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
        if picked >= 0:
            del self.array_of_stashes[picked]
            self.default_settings.set('stashes',self.array_of_stashes)

class TabclearstashCommand(sublime_plugin.WindowCommand):

    def run(self):
        self.default_settings = sublime.load_settings("Tabstasher.sublime-settings")
        if self.default_settings.has('stashes'):
            self.default_settings.erase('stashes')