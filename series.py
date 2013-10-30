import urllib2, json

class Series():

    # recuperation de la liste des episodes
    def get_json(self,url):
        datas = {}
        if url:
            y = urllib2.urlopen(url)
            datas = json.load(y)
            y.close()

        return datas

    # creation d'un dictionnaire contenant le nom des series et l'URL correspondante
    def get_series_names(self,datas):
        names = {}
        if datas:
            # recuperation des cles du dictionnaire datas contenant le nom des series
            keys = datas.keys()
            for item in keys :
                name=urllib2.unquote(item).decode('utf8')  # decodage utf8
                pos = name.rfind('/') # position du dernier / pour trouver le nom de la serie
                names[name[pos+1:]] = item # nom serie => url serie

        return names

    # retourne l'URL complete d'un episode donne
    def get_url_episode_number(self,name,nb):
        episode = ''
        if name and isinstance(nb,int) :
            episode = self.URL + '/' + self.names[name] + '/' + self.episodes[self.names[name]][nb]

        return episode 

    # retourne les elements necessaire au visonnage d'un episode : url episode et nom pour le sous-titre
    def get_episode_url(self,filename):
        resultat = ''
        # trouver le nom de la serie en fonction de l'episode
        for item in self.get_series_list():
            if filename in self.get_episodes_list(item):
                resultat = self.URL_EPISODES + '/' + self.names[item] + '/' + filename
                break

        return resultat

    # retourne la liste des episodes d'une serie
    def get_episodes_list(self,serie_name):
        return self.episodes[self.names[serie_name]]

    # retourne la liste des series triee par ordre alphabetique
    def get_series_list(self):
        liste = []
        for item in self.names.keys():
            liste.append(item)
        liste = sorted(liste)
        
        return liste

    def __init__(self):
        self.URL = 'http://www.myurl.com'
        self.JSON_DATAS_URL = self.URL + '/get_files.php'
        self.URL_EPISODES = self.URL
        # if password protected directory, add like this :
        #self.URL_EPISODES = 'http://mylogin:mypassword@www.myurl.com'
        # local downloads directory to store the subtitles
        self.DOWNLOADS = '/Users/toto/Downloads'
        self.episodes = {}
        self.names = {}

        self.episodes = self.get_json( self.JSON_DATAS_URL )
        self.names = self.get_series_names( self.episodes )