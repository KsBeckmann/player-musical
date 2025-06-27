from classes import Musica
from logger import Logger

class Playlist:
    """
    representa uma playlist de músicas

    atributos:
        nome (str): nome da playlist
        musicas (list[Musica]): lista de músicas na playlist
    """
    def __init__(self, nome: str):
        self.logger = Logger()
        self.__nome = nome
        self.__musicas: list[Musica] = []

    @property
    def nome(self) -> str:
        return self.__nome

    @property
    def musicas(self) -> list[Musica]:
        return self.__musicas

    def adicionar_musica(self, musica: Musica):
        """adiciona uma música à playlist"""
        self.__musicas.append(musica)
        self.logger.info(f"Música '{musica.nome}' adicionada à playlist '{self.nome}'.")

    def remover_musica(self, musica: Musica):
        """remove uma música da playlist"""
        if musica in self.__musicas:
            self.__musicas.remove(musica)
            self.logger.info(f"Música '{musica.nome}' removida da playlist '{self.nome}'.")
        else:
            self.logger.warning(f"Música '{musica.nome}' não encontrada na playlist '{self.nome}'.")

    def mover_musica(self, indice_atual: int, novo_indice: int) -> bool:
        """
        move uma música para uma nova posição na playlist

        args:
            indice_atual (int): o índice atual da música
            novo_indice (int): o novo índice para a música

        Returns:
            bool: True se a música foi movida e False caso contrário
        """
        if 0 <= indice_atual < len(self.__musicas) and 0 <= novo_indice < len(self.__musicas):
            musica = self.__musicas.pop(indice_atual)
            self.__musicas.insert(novo_indice, musica)
            self.logger.info(f"Música movida da posição {indice_atual} para {novo_indice} na playlist '{self.nome}'.")
            return True
        return False

    def ordenar_por_nome(self, reverso: bool = False):
        """
        ordena as músicas da playlist por nome

        args:
            reverso (bool): se True, ordena em ordem decrescente
        """
        self.__musicas.sort(key=lambda m: m.nome.lower(), reverse=reverso)
        self.logger.info(f"Playlist '{self.nome}' ordenada por nome (reverso={reverso}).")

    def remover_musica_por_indice(self, indice: int) -> bool:
        """
        remove uma música da playlist pelo seu índice

        args:
            indice (int): o índice da música a ser removida

        returns:
            bool: True se a música foi removida e False caso contrário
        """
        if 0 <= indice < len(self.__musicas):
            musica = self.__musicas.pop(indice)
            self.logger.info(f"Música '{musica.nome}' removida da posição {indice} na playlist '{self.nome}'.")
            return True
        return False

    def __getstate__(self):
        """
        prepara o estado do objeto para serialização (pickle), removendo o logger
        """
        state = self.__dict__.copy()
        if 'logger' in state:
            del state['logger']
        return state

    def __setstate__(self, state):
        """
        restaura o estado do objeto a partir da desserialização (unpickle) e recria o logger
        """
        self.__dict__.update(state)
        self.logger = Logger()