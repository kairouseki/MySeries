MySeries
========

This is my attempt to build a python client for Mac OS for watching my series stored on a server somewhere (not a NAS), and a work in progress, until I find some time to code this properly in Objective-C. Several things to remember in order to use those files :

* Install [PySide](http://qt-project.org/wiki/PySide) with [Brew](http://brew.sh) in order to display the GUI :

<pre><code>
    brew install pyside
</code></pre>

Add this line in your .bash_profile :
<pre><code>
export PYTHONPATH=/usr/local/lib/python2.7/site-packages:$PYTHONPATH 
</code></pre>

* Install VLC & [Subtitles](http://subtitlesapp.com) & go get some popcorn while you're at it.

* Install get_files.php on the server where it'll be able to scan the episodes files & directories.

* In series.py, adjust the settings according to your server configuration.

And voila.
