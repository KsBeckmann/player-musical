from classes import Musica
from logger import Logger

class Playlist:
    def __init__(self, nome: str):
        self.logger = Logger()
        self.__nome = nome
        self.__musicas = []

    @property
    def nome(self):
        return self.__nome
    
    @property
    def musicas(self):
        return self.__musicas
    
    def adicionar_musica(self, musica: Musica):
        self.__musicas.append(musica)
        self.logger.info(f"Musica {musica.nome} adicionada com sucesso")

    def remover_musica(self, musica: Musica):
        if musica in self.__musicas:
            self.__musicas.remove(musica)
            self.logger.info(f"Musica {musica.nome} removida com sucesso")
        else:
            self.logger.error(f"Música {musica.nome} não encontrada")

    def __getstate__(self):
        state = self.__dict__.copy()
        if 'logger' in state:
            del state['logger']
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)
        self.logger = Logger()