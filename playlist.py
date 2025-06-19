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

    def mover_musica(self, indice_atual: int, novo_indice: int) -> bool:
        if 0 <= indice_atual < len(self.__musicas) and 0 <= novo_indice < len(self.__musicas):
            musica = self.__musicas.pop(indice_atual)
            self.__musicas.insert(novo_indice, musica)
            self.logger.info(f"Musica {musica.nome} movida da posição {indice_atual} para {novo_indice}")
            return True
        return False
    
    def ordenar_por_nome(self, reverso: bool = False):
        self.__musicas.sort(key=lambda m: m.nome.lower(), reverse=reverso)
        self.logger.info(f"Playlist ordenada por nome (reverso={reverso})")

    def remover_musica_por_indice(self, indice: int) -> bool:
        if 0 <= indice < len(self.__musicas):
            musica = self.__musicas.pop(indice)
            self.logger.info(f"Musica {musica.nome} removida da posição {indice}")
            return True
        return False

    def __getstate__(self):
        state = self.__dict__.copy()
        if 'logger' in state:
            del state['logger']
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)
        self.logger = Logger()