import unittest

# Adicione o diretório pai ao sys.path para encontrar o módulo 'classes'
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from classes import Musica, Album, Artista

class TestClasses(unittest.TestCase):

    def test_musica(self):
        """Testa a criação de um objeto Musica."""
        musica = Musica("Let it Be", "mus2.mp3")
        self.assertEqual(musica.nome, "Let it Be")
        self.assertEqual(musica.nome_arquivo, "mus2.mp3")

    def test_album_e_adicionar_musica(self):
        """Testa a criação de um Album e a adição de músicas a ele."""
        album = Album("Let it Be")
        self.assertEqual(album.nome, "Let it Be")
        self.assertEqual(len(album.musicas), 0)
        
        album.adicionar_musica("Let it Be", "mus2.mp3")
        album.adicionar_musica("Yesterday", "mus3.mp3")
        
        self.assertEqual(len(album.musicas), 2)
        self.assertEqual(album.musicas[0].nome, "Let it Be")
        self.assertEqual(album.musicas[1].nome_arquivo, "mus3.mp3")

    def test_artista_e_adicionar_album(self):
        """Testa a criação de um Artista e a adição de um álbum a ele."""
        artista = Artista("Beatles")
        self.assertEqual(artista.nome, "Beatles")
        self.assertEqual(len(artista.albuns), 0)
        
        artista.adicionar_album("Let it Be")
        self.assertEqual(len(artista.albuns), 1)
        self.assertEqual(artista.albuns[0].nome, "Let it Be")

if __name__ == '__main__':
    unittest.main()