#!/usr/bin/python
# -*- coding: UTF-8 -*-

from os import remove
from ConfigParser import ConfigParser, RawConfigParser

class Config(ConfigParser):
    def __init__(self, path=''):
        ConfigParser.__init__(self)
        self.path = path
        self.open(self.path)

    def open(self, path):
        #Does "conf.cfg" exist?
        self.conf = self.read([path, "conf.cfg"])
        if not self.conf:
            #copy default.cfg -> conf.cfg
            self.f = open('default.cfg','r')
            self.f2 = open('conf.cfg', 'a')
            for i in self.f :self.f2.write(i)
            self.f.close()
            self.f2.close()
            self.read(["conf.cfg"])
        else:
            #file already exist, so we do nothing
            pass

        #[General]
        self.general_firsttime = self.getboolean("General", "FirstTime")
        self.general_notifications = self.getboolean("General", "Notifications")
        self.general_hotkey = self.getboolean("General", "Hotkey")
        self.general_clipboardtraslation = self.getboolean("General", "ClipboardTraslation")
        self.general_strartOnTray = self.getboolean("General", "StrartOnTray")
        self.general_notificationTime = self.getint("General", "NotificationTime")
        #[Languages]
        self.languages_from = self.get("Languages", "From")
        self.languages_into = self.get("Languages", "Into")
        #[HotKey]
        self.hotKey_key = self.get("HotKey", "Key")

    def save(self):
        configfile = open ('conf.cfg', 'wb')
        self.write(configfile)
#        self.__init__()
        self.open(self.path)

    def default(self):
        if not self.general_firsttime:
            self.do = False
        remove("conf.cfg")
        self.open(self.path)
        if not self.do:
            self.change_general_firsttime(False)
        self.save()

    #[General]
    def change_general_firsttime(self, value):
        self.set("General", "FirstTime", str(value))

    def change_general_notifications(self, value):
        self.set("General", "Notifications", str(value))

    def change_general_hotkey(self, value):
        self.set("General", "Hotkey", str(value))

    def change_general_clipboardtraslation(self, value):
        self.set("General", "ClipboardTraslation", str(value))

    def change_general_strartontray(self, value):
        self.set("General", "strartOnTray", str(value))

    def change_general_notificationTime(self, value):
        self.set("General", "NotificationTime", str(value))

    #[Languages]
    def change_languages_from(self, value):
        self.set("Languages", "From", value)

    def change_languages_into(self, value):
        self.set("Languages", "Into", value)

    #[HotKey]
    def change_hotKey_key(self, value):
        self.set("HotKey", "Key", value)


if __name__ == '__main__':
    hola = Config()
    print hola.general_notificationTime
    hola.change_general_notificationTime(5)
    hola.save()
    print hola.general_notificationTime
