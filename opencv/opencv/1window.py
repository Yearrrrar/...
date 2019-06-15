 #-*-coding:utf-8 -*-
import wx 

if __name__ == '__main__':
    app = wx.App(False)
    dlg = wx.Frame(None, wx.ID_ANY, "Hello World")
    dlg.Show(True)
    app.MainLoop()