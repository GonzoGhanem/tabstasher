import sublime, sublime_plugin
import re, os, os.path, subprocess

class TabstashCommand(sublime_plugin.WindowCommand):

    def run(self):
        self.root = self.window.folders()[0]
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
        if default_settings.get('git'):
            git_stash_cmd = 'git stash save tabstasher' + stash
            process = subprocess.call( 'cd' + self.root + ';'+ git_stash_cmd, shell=True)
        self.window.run_command('close_all')

class TabunstashCommand(sublime_plugin.WindowCommand):

    def run(self):
        self.root = self.window.folders()[0]
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
            if self.default_settings.get('git'):
                git_apply_cmd = 'git stash apply --tabstasher' + self.array_of_stashes[picked]['name']
                process = subprocess.call( 'cd' + self.root + ';'+ git_apply_cmd, shell=True)

class TabpoplaststashCommand(sublime_plugin.WindowCommand):

    def run(self):
        default_settings = sublime.load_settings("Tabstasher.sublime-settings")
        self.root = self.window.folders()[0]
        if default_settings.has('stashes'):
            self.window.run_command('close_all')
            array_of_stashes = default_settings.get('stashes')
            for stashedFile in array_of_stashes[-1]['files']:
                self.window.open_file(stashedFile)
            if default_settings.get('git'):
                git_poplast_cmd = 'git stash pop --tabstasher' + array_of_stashes[-1]['name']
                process = subprocess.call( 'cd' + self.root + ';'+ git_poplast_cmd, shell=True)
            del array_of_stashes[-1]
            default_settings.set('stashes',array_of_stashes)

class TabpopstashCommand(sublime_plugin.WindowCommand):

    def run(self):
        self.default_settings = sublime.load_settings("Tabstasher.sublime-settings")
        self.root = self.window.folders()[0]
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
            git_pop_cmd = 'git stash pop --tabstasher' + array_of_stashes[picked]['name']
            if self.default_settings.get('git'):
                process = subprocess.call( 'cd' + self.root + ';'+ git_pop_cmd, shell=True)
            del self.array_of_stashes[picked]
            self.default_settings.set('stashes',self.array_of_stashes)


class TabdeletestashCommand(sublime_plugin.WindowCommand):

    def run(self):
        self.default_settings = sublime.load_settings("Tabstasher.sublime-settings")
        self.root = self.window.folders()[0]
        if self.default_settings.has('stashes'):
            self.array_of_stashes = self.default_settings.get('stashes')
            array_of_stashes_names = []
            for stash in self.array_of_stashes:
                array_of_stashes_names.append(stash['name'])
            self.window.show_quick_panel(array_of_stashes_names, self.on_done)

    def on_done(self, picked):
        if picked >= 0:
            git_drop_cmd = 'git stash drop --tabstasher' + self.array_of_stashes[picked]['name']
            if self.default_settings.get('git'):
                process = subprocess.call( 'cd' + self.root + ';'+ git_drop_cmd, shell=True)
            del self.array_of_stashes[picked]
            self.default_settings.set('stashes',self.array_of_stashes)

class TabclearstashCommand(sublime_plugin.WindowCommand):

    def run(self):
        self.default_settings = sublime.load_settings("Tabstasher.sublime-settings")
        self.root = self.window.folders()[0]
        if self.default_settings.has('stashes'):
            stashes = self.default_settings.get('stashes')
            if self.default_settings.get('git'):
                for stash in stashes:
                    git_drop_cmd = 'git stash drop --tabstasher' + stash['name']
                    process = subprocess.call( 'cd' + self.root + ';'+ git_drop_cmd, shell=True)
            self.default_settings.erase('stashes')

class TabsetgitCommand(sublime_plugin.WindowCommand):

    def run(self):
        self.window.show_quick_panel(['Yes', 'No'], self.save_git_setting)

    def save_git_setting(self, option):
        default_settings = sublime.load_settings("Tabstasher.sublime-settings")
        default_settings.set('git',not option)