#!/usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess, signal, sys, os

from series import Series
from PySide import QtGui, QtCore

class MySeries(QtGui.QWidget):
    
    def __init__(self):
        super(MySeries, self).__init__()
        self.series = Series()
        self.initUI()
        
    def initUI(self):
          
        # parametres de la position originale des elements
        x = 8
        y = 0
        
        # parametres des dimensions de la fenetre
        ox = 300
        oy = 300
        l = 250
        h = 180
        
        # label serie
        self.label_serie = QtGui.QLabel('', self)
        self.label_serie.setText("Nom de la série :".decode('utf-8'))
        self.label_serie.move(x+2, y+10)
        
        # combobox series
        combo = QtGui.QComboBox(self)
        for item in self.series.get_series_list():
            combo.addItem(item)
        combo.move(x, y+25)
        combo.activated[str].connect(self.on_series_activated)
        
        # label episodes
        self.label_episode = QtGui.QLabel('', self)
        self.label_episode.setText("Choix de l'épisode :".decode('utf-8'))
        self.label_episode.move(x+2, y+60)
        
        # combobox episodes
        self.combo_episodes = QtGui.QComboBox(self)
        self.combo_episodes.move(x, y+75)
        self.combo_episodes.activated[str].connect(self.on_episodes_activated)  
        if self.combo_episodes.currentText() == '':
            self.on_series_activated(combo.currentText())
        
        # bouton OK
        okb = QtGui.QPushButton('OK', self)
        okb.move(x-4, 120)
        okb.clicked[bool].connect(self.call_vlc)
        
        # dimensionne la fenetre et lui donne un titre
        self.setGeometry(ox, oy, l, h)
        self.setWindowTitle('My TV Shows')
        #self.adjustSize()
        self.show()

    def call_vlc(self, pressed):
        #if source.text() == "OK":
        episode_url = self.series.get_episode_url(self.combo_episodes.currentText())
        self.kill_process('VLC')
        self.kill_process('Subtitles')
        
        # nom du fichier
        pos = episode_url.rfind('/')
        filename = episode_url[pos+1:]
        
        # nom du sous-titre
        pos = filename.rfind('.')
        subtitle = filename[:pos] + '.srt'
        
        #print os.path.exists()
        
        # telecharge le sous-titre
        processus = subprocess.Popen('/Applications/Subtitles.app/Contents/MacOS/Subtitles ' + self.series.DOWNLOADS + '/' + filename,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
        subtitle_file = self.series.DOWNLOADS + '/' + subtitle
        
        # stream la video et affiche le sous-titre      
        processus = subprocess.Popen('/Applications/VLC.app/Contents/MacOS/VLC --no-media-library --no-playlist-tree --play-and-exit --sub-file=' + subtitle_file + ' ' + episode_url, stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
    
    # méthode statique pour détruire un processus par son nom
    @staticmethod
    def kill_process(name):
        processus = subprocess.Popen(['ps', '-A'], stdout=subprocess.PIPE)
        out, err = processus.communicate()
        for line in out.splitlines():
            if name in line:
                pid = int(line.split(None, 1)[0])
                os.kill(pid, signal.SIGKILL)
    
    def on_series_activated(self, text):
        
        # detruit tous les elements de la combobox
        self.combo_episodes.clear()
        
        # remplit la combobox avec les noms de fichiers de la serie
        for item in self.series.get_episodes_list(text):
            self.combo_episodes.addItem(item)
        
        # redimensionne la combobox
        self.combo_episodes.SizeAdjustPolicy(QtGui.QComboBox.AdjustToContents)
        self.combo_episodes.setSizeAdjustPolicy(QtGui.QComboBox.AdjustToContents)
        self.combo_episodes.adjustSize()

        # redimensionne la fenetre
        self.adjustSize()
        
    def on_episodes_activated(self, text):         
        print "Episode : " + text


def myExitHandler():         
    MySeries.kill_process('VLC')
    MySeries.kill_process('Subtitles')
                  
def main():
    
    app = QtGui.QApplication(sys.argv)
    
    myseries = MySeries()
    
    app.aboutToQuit.connect(myExitHandler) 
    sys.exit(app.exec_())
    
if __name__ == '__main__':
    main()

