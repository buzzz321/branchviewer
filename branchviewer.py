#!/usr/bin/python
# -*- coding: utf-8 -*-

import wx
import subprocess
import string

REPO = '.git'

class MyFrame(wx.Frame):
    """ We simply derive a new class of Frame. """
    def __init__(self, parent, title):
        super(MyFrame, self).__init__(parent, title=title, size=(400,800)) #wx.Frame self,
        panel = wx.Panel(self)

        sizer = wx.GridBagSizer()

        self.list_ctrl = wx.ListCtrl(panel, -1, size=(-11,100),
                         style=wx.LC_REPORT
                         |wx.BORDER_SUNKEN
                         |wx.LB_MULTIPLE
                         )

        self.list_ctrl.InsertColumn(0, 'Branch tag')
        self.list_ctrl.InsertColumn(1, 'Top msg')
        sizer.Add(self.list_ctrl, pos=(0, 0), span=(2, 4), flag=wx.ALL|wx.EXPAND, border=5)

        self.refreshBtn = wx.Button(panel, -1, "Refresh")
        self.deleteBtn = wx.Button(panel, -1, "Delete")
        sizer.Add(self.refreshBtn, pos=(2, 0), span=(1,1), flag=wx.ALL|wx.EXPAND, border=5)
        sizer.Add(self.deleteBtn, pos=(2, 3), span=(1,1), flag=wx.ALL|wx.EXPAND, border=5)
        self.deleteBtn.Bind(wx.EVT_BUTTON, self.OnDelete)
        self.refreshBtn.Bind(wx.EVT_BUTTON, self.OnRefresh)
        for i in range(3):
            sizer.AddGrowableCol(i)
            sizer.AddGrowableRow(i)

        box = wx.BoxSizer(wx.VERTICAL)
        box.Add(sizer, 1, flag=wx.ALL|wx.EXPAND)

        panel.SetSizer(box)
        panel.Layout()
        #self.Center()
        self.Show(True)


    def deleteListItems(self, items):

        #print sorted(items) items seems to be sorted..
        pos = 0
        for item in items:
         
            self.list_ctrl.DeleteItem(item - pos)
            pos += 1


    def OnDelete(self, event):

        item = -1

        items = []
        while True:
            item = self.list_ctrl.GetNextItem(item,
                                wx.LIST_NEXT_ALL,
                                wx.LIST_STATE_SELECTED)
            if item == -1:
                break
            items.append(item)

            print("Item %ld is selected text %s"% (item, self.list_ctrl.GetItem(itemId=item).GetText()) )
        print items
        self.deleteListItems(items)
        self.list_ctrl.RefreshItems(0, self.list_ctrl.GetItemCount() - 1)


    def OnRefresh(self, event):
        print event

    def add_tags(self,tags):
        for tag in tags:
            #self.list_ctrl.Append([tag,''])
            self.list_ctrl.InsertStringItem(self.list_ctrl.GetItemCount(), tag)
        self.list_ctrl.SetColumnWidth(0, wx.LIST_AUTOSIZE)

def get_tags():
     cmd = "git"
     parameter1 = '--git-dir'
     parameter2 = REPO
     parameter3 = "tag"
     try:
         result = subprocess.check_output([cmd, parameter1, parameter2, parameter3])
         return string.split(result, '\n')
     except OSError as e:
         print >>sys.stderr, "Execution failed:", e

if __name__ == '__main__':
    tags = get_tags()

    app = wx.App(False)
    frame = MyFrame(None, 'Branch Deleter')
    frame.add_tags(tags)

    app.MainLoop()
