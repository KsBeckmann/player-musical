import unittest
from unittest.mock import patch, mock_open

# Adicione o diretório pai ao sys.path para encontrar os módulos
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import utils
from classes import Artista, Album, Musica

class TestUtils(unittest.TestCase):

    def setUp(self):
        """Configura uma estrutura de artistas e álbuns para os testes."""
        # Artista 1: Beatles
        artista_beatles = Artista("Beatles")
        album_beatles = Album("Singles")
        album_beatles.adicionar_musica("Let it Be", "mus2.mp3")
        album_beatles.adicionar_musica("Yesterday", "mus3.mp3")
        artista_beatles.albuns.append(album_beatles)

        # Artista 2: Chitãozinho & Xororó
        artista_chitao = Artista("Chitãozinho & Xororó")
        album_chitao = Album("Página de Amigos")
        album_chitao.adicionar_musica("Página de amigos", "mus1.mp3")
        artista_chitao.albuns.append(album_chitao)

        self.artistas_teste = [artista_beatles, artista_chitao]

    @patch('utils.open', new_callable=mock_open)
    @patch('pickle.dump')
    def test_salvar_dados(self, mock_pickle_dump, mock_file):
        """Testa se a função salvar_dados chama o pickle.dump corretamente."""
        playlists_teste = []
        utils.salvar_dados(self.artistas_teste, playlists_teste)
        
        mock_file.assert_called_with(utils.CAMINHO_ARQUIVO, 'wb')
        
        dados_esperados = {'artistas': self.artistas_teste, 'playlists': playlists_teste}
        mock_pickle_dump.assert_called_with(dados_esperados, mock_file())

    @patch('pathlib.Path.exists', return_value=True)
    @patch('utils.open', new_callable=mock_open)
    @patch('pickle.load')
    def test_carregar_dados(self, mock_pickle_load, mock_file, mock_exists):
        """Testa se a função carregar_dados processa os dados corretamente."""
        dados_mock = {'artistas': self.artistas_teste, 'playlists': []}
        mock_pickle_load.return_value = dados_mock
        
        artistas, playlists = utils.carregar_dados()
        
        mock_file.assert_called_with(utils.CAMINHO_ARQUIVO, 'rb')
        self.assertEqual(len(artistas), 2)
        self.assertEqual(artistas[0].nome, "Beatles")
        self.assertEqual(artistas[1].albuns[0].musicas[0].nome, "Página de amigos")
        self.assertEqual(len(playlists), 0)
    
    def test_adicionar_artista_novo(self):
        """Testa a adição de um artista que não existe na lista."""
        artistas = []
        resultado = utils.adicionar_artista(artistas, "Queen")
        self.assertTrue(resultado)
        self.assertEqual(len(artistas), 1)
        self.assertEqual(artistas[0].nome, "Queen")

    def test_adicionar_artista_existente(self):
        """Testa a tentativa de adicionar um artista que já existe."""
        artistas_existentes = [Artista("Beatles")]
        resultado = utils.adicionar_artista(artistas_existentes, "Beatles")
        self.assertFalse(resultado)
        self.assertEqual(len(artistas_existentes), 1)

if __name__ == '__main__':
    unittest.main()