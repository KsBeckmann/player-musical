import unittest

# Adicione o diretório pai ao sys.path para encontrar os módulos
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from playlist import Playlist
from classes import Musica

class TestPlaylist(unittest.TestCase):

    def setUp(self):
        """Configura o ambiente de teste com as músicas fornecidas."""
        self.playlist = Playlist("Minhas Favoritas")
        self.mus_chitao = Musica("Página de amigos", "mus1.mp3")
        self.mus_beatles1 = Musica("Let it Be", "mus2.mp3")
        self.mus_beatles2 = Musica("Yesterday", "mus3.mp3")

    def test_adicionar_musica(self):
        """Testa a adição de uma música à playlist."""
        self.playlist.adicionar_musica(self.mus_beatles1)
        self.assertIn(self.mus_beatles1, self.playlist.musicas)
        self.assertEqual(len(self.playlist.musicas), 1)

    def test_remover_musica(self):
        """Testa a remoção de uma música da playlist."""
        self.playlist.adicionar_musica(self.mus_beatles1)
        self.playlist.adicionar_musica(self.mus_chitao)
        self.playlist.remover_musica(self.mus_beatles1)
        
        self.assertNotIn(self.mus_beatles1, self.playlist.musicas)
        self.assertIn(self.mus_chitao, self.playlist.musicas)
        self.assertEqual(len(self.playlist.musicas), 1)

    def test_ordenar_por_nome(self):
        """Testa a ordenação da playlist por nome de música (A-Z)."""
        self.playlist.adicionar_musica(self.mus_chitao)      # Página de amigos
        self.playlist.adicionar_musica(self.mus_beatles1)   # Let it Be
        self.playlist.adicionar_musica(self.mus_beatles2)   # Yesterday
        
        self.playlist.ordenar_por_nome()
        
        # Ordem esperada: Let it Be, Página de amigos, Yesterday
        self.assertEqual(self.playlist.musicas[0].nome, "Let it Be")
        self.assertEqual(self.playlist.musicas[1].nome, "Página de amigos")
        self.assertEqual(self.playlist.musicas[2].nome, "Yesterday")

    def test_mover_musica(self):
        """Testa a movimentação de uma música para uma nova posição."""
        self.playlist.adicionar_musica(self.mus_chitao)
        self.playlist.adicionar_musica(self.mus_beatles1)
        self.playlist.adicionar_musica(self.mus_beatles2)
        
        # Estado inicial: [Chitao, Beatles1, Beatles2]
        # Mover "Página de amigos" (índice 0) para a posição 1
        self.playlist.mover_musica(0, 1)
        
        # Estado esperado: [Beatles1, Chitao, Beatles2]
        self.assertEqual(self.playlist.musicas[0], self.mus_beatles1)
        self.assertEqual(self.playlist.musicas[1], self.mus_chitao)
        self.assertEqual(self.playlist.musicas[2], self.mus_beatles2)

if __name__ == '__main__':
    unittest.main()