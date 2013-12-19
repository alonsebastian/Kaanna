#!/usr/bin/python
# -*- coding: UTF-8 -*-

import pygtk
import gtk
import conf
#import keybinder #this does the trick for the global hotkey, sudo apt-get install python-keybinder
#import pynotify
from os.path import join, dirname
from translation import blank_string, translate
from translation import Language_dict, Language_list
import pyHook
import win32clipboard
import win32con
import gtkwin32
import win32gui
import path

pygtk.require("2.0")        #We import everything we need to deal with the GUI
PATH = dirname(path.__file__)

def deco(join):
    def returned(*arg,**karg):
        print 'chota'
        return join(*arg, **karg).replace("."+chr(92), r"")
    return returned

join = deco(join)

class App:
    def __init__(self):         #initialize every important widget that we will interact with.
        print PATH
        self.hotkey_conf = []
        self.configManager = conf.Config(join(PATH, "conf")) #Load the programs configuration
        self.get_widgets()

        self.ls = gtk.ListStore(str)
        for item in Language_list:          #We create the list store that will store all the languages
            self.ls.append ([item.capitalize()])

        self.original_language_combobox.set_model(self.ls)
        self.new_language_combobox.set_model(self.ls)

        self.cellr = gtk.CellRendererText()
        self.original_language_combobox.pack_start(self.cellr)
        self.original_language_combobox.add_attribute(self.cellr, 'text', 0)

        self.cellr1 = gtk.CellRendererText()
        self.new_language_combobox.pack_start(self.cellr1)
        self.new_language_combobox.add_attribute(self.cellr1, 'text', 0)

        #We do the initial binding
        self.bind = self.configManager.hotKey_key
        self.pressed= []
#        keybinder.bind (self.bind, self.bind_callback, 1)
        self.hm = pyHook.HookManager()
        self.hm.KeyDown = self.Down
        self.hm.KeyUp = self.Up
        self.hm.HookKeyboard()

        self.restoreConfig()

        #Set the languages labels.
        self.original_language_label.set_text (self.original.capitalize())
        self.new_language_label.set_text (self.translation.capitalize())

        #this does the trick for the tray icon and it's different signals
#        self.icon = gtk.StatusIcon()
        self.pixels = gtk.gdk.pixbuf_new_from_file(join(PATH,'Resources/kaanna.png'))
#        self.icon.set_from_pixbuf(self.pixels)
#        self.change_icon_tooltip()
#        self.icon.connect("activate", self.activate_callback)
#        self.icon.connect("popup-menu", self.popup_callback)



        #define the clipboard we'll be working with
#        self.clipboard = gtk.Clipboard(selection="CLIPBOARD")

        self.window.show = self.show_decorator(self.window.show)

        if not self.configManager.general_strartOnTray:
            self.window.show()
            self.minimized = True
        else:
            self.minimized = False

        self.window.realize()
        self.win32ext = gtkwin32.GTKWin32Ext(self.window)
        hinst = win32gui.GetModuleHandle(None)
        icon_flags = win32con.LR_LOADFROMFILE | win32con.LR_DEFAULTSIZE
        hicon = win32gui.LoadImage(hinst, join(PATH, "Resources\kaanna.ico"), win32con.IMAGE_ICON, 0, 0, icon_flags)
        self.win32ext.add_notify_icon(hicon = hicon)
        self.win32ext.notify_icon.menu = self.menu
        self.win32ext.message_map({
            gtkwin32.WM_TRAYMESSAGE: self.on_notifyicon_activity
            })

        self.change_icon_tooltip()

        self.translate_called = False #this will help for the global hotkey not to happen twice

    def on_notifyicon_activity(self, hwnd, message, wparam, lparam):
        if lparam == gtkwin32.WM_RBUTTONUP:
            self.win32ext.notify_icon.menu.popup(None, None, None, 0, 0)
        elif lparam == gtkwin32.WM_LBUTTONUP:
            self.activate_callback()

    def show_decorator(self, infunction):
        def out(*args, **kwargs):
            infunction(*args, **kwargs)
            self.original_entry.grab_focus()
        return out

    def Down(self, event):
        if not event.Key in self.pressed:
            self.pressed.append(event.Key)
        return True

    def Up (self, event):#FIXME
        #for some reason some keys apparently never leave the stack
        for key in self.hotkey_conf:
            if not key in self.pressed:
                try:
                    self.pressed.remove(event.Key)
                except ValueError:
                    pass
                return True

        if event.Key in self.hotkey_conf and not self.translate_called:
            self.translate_called = True
            self.bind_callback(1)

        self.translate_called = False
        self.pressed= []
        return True

#        if "Lcontrol" in self.pressed and "B" in self.pressed:
#            if event.Key == "B":
#                self.bind_callback(1)
                #self.pressed.remove("B")
#        self.pressed.remove(event.Key)
        #if event.Key in self.pressed:
        #    self.pressed.remove(event.Key)
#        return True


    def get_widgets(self):
        #bring the file where the settings dialog is described
        self.settingsfile = join(PATH, "Resources\Configurations.ui")
        self.settingswtree = gtk.Builder()
        self.settingswtree.add_from_file(self.settingsfile)

        self.settingswtree.connect_signals(self)

        #settings dialog
        self.settings = self.settingswtree.get_object("window1")

        #language config tab
        self.original_language_combobox = self.settingswtree.get_object("combobox1")
        self.new_language_combobox = self.settingswtree.get_object("combobox2")

        #hotkey config tab
        self.Alt_button = self.settingswtree.get_object("button3")
        self.Ctrl_button = self.settingswtree.get_object("button4")
        self.Shift_button = self.settingswtree.get_object("button5")
        self.hotkey_entry = self.settingswtree.get_object("entry1")
        self.hotkey_label = self.settingswtree.get_object("label8")

        #general configs tab
        self.spinbutton1 = self.settingswtree.get_object("spinbutton1")
        self.spinbutton1.set_range(1, 100)
        self.checkbutton1 = self.settingswtree.get_object("checkbutton1")
        self.checkbutton2 = self.settingswtree.get_object("checkbutton2")
        self.checkbutton3 = self.settingswtree.get_object("checkbutton3")
        self.checkbutton4 = self.settingswtree.get_object("checkbutton4")
        self.spinbutton1 = self.settingswtree.get_object("spinbutton1")
        adjustment = gtk.Adjustment(1, 1, 100, 1, 1)
        self.spinbutton1.configure (adjustment, 1, 0)


        #bring all the file where the GUI is described
        self.uifile = join(PATH, "Resources/Translator.ui")
        self.wTree = gtk.Builder()
        self.wTree.add_from_file(self.uifile)

        #connect the signals
        self.wTree.connect_signals(self)

        #bring all the different widgets and hide/show the window/dialogs
        self.window = self.wTree.get_object("window1")

        #Main window widgets
        self.original_entry = self.wTree.get_object("entry1")
        self.translated_entry = self.wTree.get_object("entry2")
        self.translate_button = self.wTree.get_object("button1")
        self.invert_button = self.wTree.get_object("button4")
        self.original_language_label = self.wTree.get_object("label1")
        self.new_language_label = self.wTree.get_object("label2")

        #Tray icon's menu
        self.menu = self.wTree.get_object("menu1")

    def restoreConfig(self): #This function shall be called whenever restoring the settings is needed
                             #example, cancel button in the settings dialog, opening the program

        self.configManager.open(join(PATH,"conf/"))  #update the settings

        #hotkey settings
        self.hotkey_label.set_text(self.configManager.hotKey_key)
        self.update_internal_hotkey_conf()

        #languages settings
        self.original = self.configManager.languages_from
        self.translation = self.configManager.languages_into
        for i in range (len(Language_list)):
            if Language_list [i] == self.original.upper():
                break
        for j in range (len(Language_list)):
            if Language_list [j] == self.translation.upper():
                break
        self.original_language_combobox.set_active(i)        #We update the comboboxes to the current option.
        self.original_language_label.set_text(self.original.capitalize())
        self.new_language_combobox.set_active(j)
        self.new_language_label.set_text(self.translation.capitalize())

        #general settings
        self.checkbutton1.set_active(0)
        self.checkbutton2.set_active(0)
        self.checkbutton3.set_active(0)
        self.checkbutton4.set_active(0)

        if self.configManager.general_notifications:
            self.checkbutton1.set_active(1)

        if self.configManager.general_hotkey:
            self.checkbutton2.set_active(1)

        if self.configManager.general_clipboardtraslation:
            self.checkbutton3.set_active(1)

        if self.configManager.general_strartOnTray:
            self.checkbutton4.set_active(1)

        self.spinbutton1.set_value(int(self.configManager.general_notificationTime))

        #Update hotkey to the setted value
        self.updateHotkey()

    def disable_hotkey(self, widget):
        self.hotkey_entry.set_sensitive(False)
        self.Alt_button.set_sensitive(False)

    #Alt button in the hotkey config
    def on_button5_clicked(self, widget):
        if "<Alt>" in self.hotkey_label.get_text():
            self.bindstr = self.hotkey_label.get_text().replace("<Alt>", "")
            self.hotkey_label.set_text(self.bindstr)
        else:
            self.bindstr = "<Alt>" + self.hotkey_label.get_text()
            self.hotkey_label.set_text(self.bindstr)

    #Ctrl button in the hotkey config
    def on_button6_clicked(self, widget):
        if "<Ctrl>" in self.hotkey_label.get_text():
            self.bindstr = self.hotkey_label.get_text().replace("<Ctrl>", "")
            self.hotkey_label.set_text(self.bindstr)
        else:
            self.bindstr = "<Ctrl>" + self.hotkey_label.get_text()
            self.hotkey_label.set_text(self.bindstr)

    #Shift button in the hotkey config
    def on_button7_clicked_conf(self, widget):
        if "<Shift>" in self.hotkey_label.get_text():
            self.bindstr = self.hotkey_label.get_text().replace("<Shift>", "")
            self.hotkey_label.set_text(self.bindstr)
        else:
            self.bindstr = "<Shift>" + self.hotkey_label.get_text()
            self.hotkey_label.set_text(self.bindstr)

    def on_button8_clicked(self, widget):
        self.configManager.default()
        self.restoreConfig()

    #Hotkey config entry changed
    def on_entry3_changed(self, widget):
        if '>'in self.hotkey_entry.get_text() or '<' in self.hotkey_entry.get_text():
             self.hotkey_entry.set_text('')
        if len(self.hotkey_entry.get_text()) == 2:
             self.hotkey_entry.set_text(self.hotkey_entry.get_text()[1].lower())

        if self.hotkey_label.get_text()[-1:] != "<" and self.hotkey_label.get_text()[-1:] != ">":
            self.bindstr = self.hotkey_label.get_text()[:-1] + self.hotkey_entry.get_text().lower()
            self.hotkey_label.set_text(self.bindstr)
        else:
            self.bindstr = self.hotkey_label.get_text() + self.hotkey_entry.get_text().lower()
            self.hotkey_label.set_text(self.bindstr)

    #hotkey config callback in the tray menu
    def settings_cb(self, menuoption):
        self.minimized = True
        self.settings.show()

    #which languages are selected for the translation?
    def which_language(self):
        self.lang1 = self.original.upper()
        self.lang2 = self.translation.upper()
        self.lang1 = Language_dict[self.lang1]
        self.lang2 = Language_dict[self.lang2]


    #this takes care of the translation
    def translate(self):
        #we get the string that the user wants to translate.
        self.string = self.original_entry.get_text()
        self.which_language()
        self.string = (translate(self.string, self.lang1, self.lang2)).decode("UTF-8")
        self.translated_entry.set_text (self.string.encode("latin-1"))


    #callback for the global hotkey event
    def translate_online_cb(self, menuoption):
        print "translating online"
        win32clipboard.OpenClipboard()
        try:
            #we try to get the data
            self.string = win32clipboard.GetClipboardData(win32con.CF_TEXT)
        except TypeError:
            print "Clipboard is empty"
            #this generally means there's no data in the clipboard
            #and we escape the function
            win32clipboard.CloseClipboard()
            return
        else:
            win32clipboard.CloseClipboard()
#        self.string = str(self.clipboard.wait_for_text())
        self.which_language()
        #we get the selected languages and turned them into google translate options.
        self.string = translate(self.string, self.lang1, self.lang2)
        self.string = self.string.decode("UTF-8")
#        if self.configManager.general_clipboardtraslation:
#            self.clipboard.set_text(self.string, len=-1)
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        try:
            print self.string
            win32clipboard.SetClipboardData(win32con.CF_UNICODETEXT, self.string)
        except pywintypes.error: #for some reason we can't set the clipboard
            pass #there's nothing to do about it but to catch the exception
        win32clipboard.CloseClipboard()
        if self.configManager.general_notifications:
            self.notify(self.string)

    def notify(self, message):
##        if pynotify.init("Kaanna"):
##            Alert = pynotify.Notification("Kaanna", message)
##            Alert.set_icon_from_pixbuf(self.pixels)
##            Alert.show()
##            #print "notify"
##        else:
##            print "Error starting pynotify"
        self.win32ext.show_balloon_tooltip(
                'Kaanna Translator', message.decode("UTF-8"), timeout = self.configManager.general_notificationTime)

    #Cancel button in the settings dialog
    def cancel(self, widget):
        self.restoreConfig()
        self.settings.hide()
        if not self.minimized:
            self.window.show()
            self.minimized = False

    #Save button in the settings dialog
    def save_changes(self,widget):
        self.saveSettings()
        self.configManager.open(join(PATH, "conf/"))  #update the settings
        self.updateHotkey()

    #updateHotkey takes care of unbind old hotkeys and creating the new bind
    #according to the settings
    def updateHotkey(self):
        #keybinder.unbind(self.bind)
        self.bind = self.configManager.hotKey_key
        self.update_internal_hotkey_conf()
        print self.bind
        #keybinder.bind (self.bind, self.bind_callback, 1)


    def bind_callback(self, menuoption):
        if self.configManager.general_hotkey:
            self.translate_online_cb(menuoption)

    #Stores all the settings in the configManager
    def saveSettings(self):

        #Languages settings
        self.language1, self.language2 = self.original_language_combobox.get_active(), self.new_language_combobox.get_active()

        self.language1 = Language_list [self.language1]
        self.language2 = Language_list [self.language2]

        self.original = self.language1
        self.translation = self.language2

        self.configManager.change_languages_from(self.original)
        self.configManager.change_languages_into(self.translation)

        self.original_language_label.set_text (self.original.capitalize())
        self.new_language_label.set_text (self.translation.capitalize())

        self.change_icon_tooltip()

        #Hotkey settings
        self.configManager.change_hotKey_key(self.hotkey_label.get_text())

        #General settings
        if self.checkbutton1.get_active():
            self.configManager.change_general_notifications(True)
        else:
            self.configManager.change_general_notifications(False)

        if self.checkbutton2.get_active():
            self.configManager.change_general_hotkey(True)
        else:
            self.configManager.change_general_hotkey(False)

        if self.checkbutton3.get_active():
            self.configManager.change_general_clipboardtraslation(True)
        else:
            self.configManager.change_general_clipboardtraslation(False)

        if self.checkbutton4.get_active():
            self.configManager.change_general_strartontray(True)
        else:
            self.configManager.change_general_strartontray(False)


        self.configManager.change_general_notificationTime(str(int(self.spinbutton1.get_value())))

        #Save the settings
        self.configManager.save()

        print 'Changes saved'
        self.settings.hide()
        self.window.show()

    def update_internal_hotkey_conf(self):
        self.old = self.hotkey_label.get_text()
        self.hotkey_conf = []
        if "<Shift>" in self.old and "Lshift" not in self.hotkey_conf:
            self.hotkey_conf.append("Lshift")
        if "<Ctrl>" in self.old and "Lcontrol" not in self.hotkey_conf:
            self.hotkey_conf.append("Lcontrol")
        if "<Alt>" in self.old and "Lmenu" not in self.hotkey_conf:
            self.hotkey_conf.append("Lmenu")
        if self.old[-1:] not in self.hotkey_conf:
            self.hotkey_conf.append(self.old[-1:].upper())

    #Close the settings window
    def on_settings_delete_event(self, widget, signal):
        self.cancel(widget)
        return True #so we dont mess up with gtk

    #this displays the menu in the tray when the icon is clicked
    def popup_callback(self, icon, button, active_time):
        self.menu.popup(None, None, gtk.status_icon_position_menu, button, active_time, self.icon)

    #callback for the left click event on the tray icon
    #this takes care of not mixing the window and the options dialog
    def activate_callback(self):
        if self.window.get_property("visible"):
            self.window.hide()
        else:
            self.window.show()

    #callback for the "Exit" option in the tray icon's menu
    def exit_callback (self, menuitem):
        gtk.main_quit()

    #"translate" button
    def on_button1_clicked (self, widget):
        self.translate()

     #"invert" button
    def on_button4_clicked (self, widget):
        self.invertLanguages()

        #Save settings in the configManager
        self.saveSettings()

        #Update the tray icon's tooltip
        self.change_icon_tooltip()

    def invertOnTray (self, widget):
        self.invertLanguages()
        self.change_icon_tooltip()

    #invert button in the settings
    def on_button7_clicked(self, widget):
        #FIXME
        i = self.original_language_combobox.get_active()
        j= self.new_language_combobox.get_active()
        self.original_language_combobox.set_active(j)        #We update the comboboxes to the current option.
        self.new_language_combobox.set_active(i)

    def invertLanguages(self):
        self.temp = self.original
        self.original = self.translation
        self.translation = self.temp

        #set labels
        self.original_language_label.set_text (self.original.capitalize())
        self.new_language_label.set_text (self.translation.capitalize())

        #set the entrys
        self.originaltext = self.original_entry.get_text()
        self.translationtext = self.translated_entry.get_text()
        self.original_entry.set_text(self.translationtext)
        self.translated_entry.set_text(self.originaltext)

        #Update comboboxes
        i = Language_list.index(self.original.upper())
        j = Language_list.index(self.translation.upper())

        self.original_language_combobox.set_active(i)        #We update the comboboxes to the current option.
        self.new_language_combobox.set_active(j)

    #options button in the main window
    def on_button3_clicked (self, widget):
        self.settings.show()
        self.window.hide()
        self.minimized = False

    #press the "enter" key when writing in the first entry box
    def on_entry1_activate (self, widget):
        self.translate()

    def on_window1_delete_event(self, widget, event):       #Close main window.
        self.window.hide()
        if self.configManager.general_firsttime:
            self.notify("Kaanna is now running on system tray")
            self.configManager.change_general_firsttime(False)
            self.configManager.save()
        return True

    #hotkey config close button
    def on_dialog2_delete_event(self, widget, event):       #Close option dialog.
        self.hotkey_config_dialog.hide()
        return True #so we don't mess gtk up

    #This function takes care of changing the tooltip of the tray icon
    #depending on the languages the user is working with
    def change_icon_tooltip(self):
        self.TrayTooltip = "Kaanna | %s -> %s" % (self.original_language_label.get_text(),
                                                self.new_language_label.get_text())
        del (self.win32ext.notify_icon._infotitle)
        del (self.win32ext.notify_icon._info)
        self.win32ext.notify_icon.set_tooltip(self.TrayTooltip)

    def show_about_dialog(self, widget):
        self.about_dialog = gtk.AboutDialog()
        self.about_dialog.set_icon_from_file (join(PATH, "Resources/kaanna.ico"))
        self.about_dialog.set_comments("Kaanna is a small but powerful translator")
        self.about_dialog.set_website('https://code.launchpad.net/kaanna')
        self.about_dialog.set_license(''.join(open(join(PATH, "LICENSE")).readlines()))
        self.about_dialog.set_logo(self.pixels)
        self.about_dialog.set_destroy_with_parent(True)
        self.about_dialog.set_name('Kaanna')
        self.about_dialog.set_version('\n(First Development Version)')
        self.about_dialog.set_authors(['Sebastian Alonso <alon.sebastian@gmail.com>', 'Martin Volpe <martin.volpe@gmail.com>'])
        self.about_dialog.run()
        self.about_dialog.destroy()


def main():
##    try:
##        import ctypes
##        libc = ctypes.CDLL('libc.so.6')
##        libc.prctl(15, 'Kaanna', 0, 0)        # Change the process name.
##    except ImportError:
##        print "Process name was not changed"
    a = App()   #Initialize the app.
    gtk.main()  #let's gtk take care of the situation.

if __name__ == "__main__":
    main()
