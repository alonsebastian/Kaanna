#!/usr/bin/python
# -*- coding: UTF-8 -*-

import pygtk, gtk
import sys
from conf.conf import Config

class App (Config):
    def __init__(self):         #initialize every important widget that we will interact with.
        #bring all the file where the GUI is described
        Config.__init__(self, "conf/")
        self.uifile = "Resources/Configurations.ui"
        self.wTree = gtk.Builder()
        self.wTree.add_from_file(self.uifile)

        #connect the signals
        self.wTree.connect_signals(self)

        #bring all the different widgets and hide/show the window/dialogs
        self.checkbutton1 = self.wTree.get_object("checkbutton1")
        self.checkbutton2 = self.wTree.get_object("checkbutton2")
        self.checkbutton3 = self.wTree.get_object("checkbutton3")
        self.checkbutton4 = self.wTree.get_object("checkbutton4")
        self.window = self.wTree.get_object("window1")
        self.window.show()

        if self.general_notifications:
            self.checkbutton1.set_active(1)

        if self.general_hotkey:
            self.checkbutton2.set_active(1)

        if self.general_clipboardtraslation:
            self.checkbutton3.set_active(1)

        if self.general_strartOnTray:
            self.checkbutton4.set_active(1)

    def cancel(self, widget):
        sys.exit()

    def save_changes(self, widget):

        if self.checkbutton1.get_active():
            self.change_general_notifications(True)
        else:
            self.change_general_notifications(False)

        if self.checkbutton2.get_active():
            self.change_general_hotkey(True)
        else:
            self.change_general_hotkey(False)

        if self.checkbutton3.get_active():
            self.change_general_clipboardtraslation(True)
        else: 
            self.change_general_clipboardtraslation(False)

        if self.checkbutton4.get_active():
            self.change_general_strartontray(True)
        else: 
            self.change_general_strartontray(False)


        self.save()

        print 'Changes saved'
        sys.exit()

if __name__ == "__main__":

    GUI = App()
    gtk.main()

