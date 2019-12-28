def lir(liste):
    we = []
    for i in liste:
        for y in i:
            if y:
                we.append(y)

    return we


class de:
    def __init__(self, numbe=None, pathofthemovie=None, pathofthethumb=None, name=None, movie_ca=None):
        self.pathmovie = pathofthemovie
        self.paththumb = pathofthethumb
        self.name = name
        self.cat = movie_ca
        self.numbe = numbe


class series:
    def __init__(self, numbe, pathofthemovie, pathofthethumb, name, movie_ca, season, episode):
        self.pathmovie = pathofthemovie
        self.paththumb = pathofthethumb
        self.name = name
        self.cat = movie_ca
        self.numbe = numbe
        self.season = season
        self.episode = episode

