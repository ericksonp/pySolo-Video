import urllib.request as urllib
import sys, time, subprocess, paramiko
import view, socket, webbrowser
from PySide import QtCore, QtGui


class ControlMainWindow(QtGui.QMainWindow):
    
    rpiList=[]    
    
    def __init__(self, parent=None):
        super(ControlMainWindow, self).__init__(parent)
        self.ui = view.Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.loadButton.clicked.connect(self.piDiscover)
        self.ui.ipEdit.setText(str(localIp[0]))
        self.ui.ipEdit_2.setText(str(localIp[1]))
        self.ui.ipEdit_3.setText(str(localIp[2]))
        self.ui.listWidget.itemEntered.connect(self.openPi)
        self.ui.listWidget.itemDoubleClicked.connect(self.openPi)
        self.ui.progressBar.hide()
        
    
    @QtCore.Slot()
    def piDiscover(self):
        self.ui.progressBar.show()
        port = 80
        rpiList = []
        nameList =[]
        for i in range(1,255):
            url = "http://"+localIp[0]+"."+localIp[1]+"."+localIp[2]+"."+str(i)
            #print(url+port)
            try:
                req = urllib.Request(url=url+':8088/pidiscover')
                f = urllib.urlopen(req,timeout = 0.05)
                message = f.read()
                print(message)
               # password = b'yes'
                if (message):
                    message = message.decode("utf-8")
                    nameList.append(message)
                    rpiList.append(url)
                    print ('[%s]' % ', '.join(map(str, rpiList)))
                    self.ui.listWidget.addItem(message)
            except:
                pass
                #print("No this one")
                
            #print percentage complete
            sys.stdout.write( "scaning..."+str(int(i/255*100)) + '%\r'),
            self.ui.progressBar.setValue(int(i/255*100))
        print("Ended  ")
        self.ui.listWidget.addItems(nameList)
        self.rpiList = rpiList
        self.ui.progressBar.hide()
        
    @QtCore.Slot()
    def openPi(self):
        itemId = str(self.ui.listWidget.currentRow())#indexFromItem(self.ui.listWidget.currentItem))
        print (itemId)
        url = self.rpiList[int(itemId)]+":8088"
        webbrowser.open(url, new=2)

def askPiId(device, port):
    req = urllib.Request(url='http://'+device+':'+str(port),method='PIID')
    f = urllib.urlopen(req,timeout = 1)
    piId=f.read()
    return piId
    
        

            
   
if __name__ == "__main__":
    localIp = socket.gethostbyname(str(socket.gethostname())).split('.')
    app = QtGui.QApplication(sys.argv)
    mySW = ControlMainWindow()
    mySW.show()
    sys.exit(app.exec_())
