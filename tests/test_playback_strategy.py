import unittest
import random

# adiciona o diretório pai ao sys.path
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from playlist import Playlist
from classes import Musica
from playback_strategy import SequentialPlayStrategy, ShufflePlayStrategy

class TestPlaybackStrategy(unittest.TestCase):

    def setUp(self):
        """configura uma playlist com algumas músicas para os testes"""
        self.playlist = Playlist("Test Playlist")
        self.musica1 = Musica("A", "a.mp3")
        self.musica2 = Musica("B", "b.mp3")
        self.musica3 = Musica("C", "c.mp3")
        self.playlist.adicionar_musica(self.musica1)
        self.playlist.adicionar_musica(self.musica2)
        self.playlist.adicionar_musica(self.musica3)

    def test_sequential_play_strategy(self):
        """testa se a estratégia sequencial retorna a ordem original"""
        strategy = SequentialPlayStrategy()
        musicas_ordenadas = strategy.selecionar_musicas(self.playlist)
        
        self.assertEqual(len(musicas_ordenadas), 3)
        self.assertEqual(musicas_ordenadas[0].nome, "A")
        self.assertEqual(musicas_ordenadas[1].nome, "B")
        self.assertEqual(musicas_ordenadas[2].nome, "C")

    def test_shuffle_play_strategy(self):
        """testa se a estratégia de shuffle retorna uma ordem diferente"""
        # só uma seed aleatória mesmo
        random.seed(42)
        
        strategy = ShufflePlayStrategy()
        musicas_embaralhadas = strategy.selecionar_musicas(self.playlist)
        
        # verifica se a lista ainda contém todos os elementos originais
        self.assertEqual(len(musicas_embaralhadas), 3)
        self.assertIn(self.musica1, musicas_embaralhadas)
        self.assertIn(self.musica2, musicas_embaralhadas)
        self.assertIn(self.musica3, musicas_embaralhadas)
        
        self.assertEqual(musicas_embaralhadas[0].nome, "C")
        self.assertEqual(musicas_embaralhadas[1].nome, "B")
        self.assertEqual(musicas_embaralhadas[2].nome, "A")
        
        self.assertNotEqual([m.nome for m in self.playlist.musicas], [m.nome for m in musicas_embaralhadas])

if __name__ == '__main__':
    unittest.main()