from abc import ABC, abstractmethod
import random
from playlist import Playlist
from classes import Musica

class PlaybackStrategy(ABC):
    """
    a interface da estratégia declara operações comuns a todas as
    versões suportadas de um algoritmo
    """
    @abstractmethod
    def selecionar_musicas(self, playlist: Playlist) -> list[Musica]:
        """retorna a lista de músicas na ordem definida pela estratégia"""
        pass

class SequentialPlayStrategy(PlaybackStrategy):
    """estratégia de reprodução sequencial"""
    def selecionar_musicas(self, playlist: Playlist) -> list[Musica]:
        print("Tocando em ordem sequencial.")
        return playlist.musicas

class ShufflePlayStrategy(PlaybackStrategy):
    """estratégia de reprodução aleatória"""
    def selecionar_musicas(self, playlist: Playlist) -> list[Musica]:
        print("Tocando em ordem aleatória (shuffle).")
        musicas_aleatorias = list(playlist.musicas)
        random.shuffle(musicas_aleatorias)
        return musicas_aleatorias