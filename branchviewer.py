import wx
import subprocess
import string

REPO = '.git'

class MyFrame(wx.Frame):
    """ We simply derive a new class of Frame. """
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(200,200))
        panel = wx.Panel(self, -1, style=wx.SUNKEN_BORDER)
        
        sizer = wx.GridBagSizer()
        
        self.list_ctrl = wx.ListCtrl(panel, size=(-11,100),
                         style=wx.LC_REPORT
                         |wx.BORDER_SUNKEN
                         |wx.EXPAND
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
        self.SetClientSize(panel.GetBestSize())
        panel.Layout()
        self.Show(True)

    def OnDelete(self, event):
        print event

    def OnRefresh(self, event):
        print event

    def add_tags(self,tags):
        for tag in tags:
            self.list_ctrl.Append([tag,''])
        
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
