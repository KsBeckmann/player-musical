import pickle
import os
import shutil
from pathlib import Path
from classes import Artista

CAMINHO_ARQUIVO = "dados.pkl"
PASTA_MUSICAS = "musicas"

def salvar_dados(artistas, playlists=None):
    """Salva dados de artistas e playlists"""
    if playlists is None:
        playlists = []
    
    dados = {
        'artistas': artistas,
        'playlists': playlists
    }
    with open(CAMINHO_ARQUIVO, 'wb') as arquivo:
        pickle.dump(dados, arquivo)

def adicionar_artista(artistas: list, novo_artista: str) -> bool:
    for artista in artistas:
        if artista.nome == novo_artista:
            return False
    
    artistas.append(Artista(novo_artista))
    return True

def adicionar_album(artistas: list, nome_artista: str, nome_album: str) -> bool:
    adicionar_artista(artistas, nome_artista)
    for artista in artistas:
        if artista.nome == nome_artista:
            for album in artista.albuns:
                if album.nome == nome_album:
                    return False
            artista.adicionar_album(nome_album)
            return True

def adicionar_musica(artistas: list, nome_artista: str, nome_album: str, 
                    nome_musica: str, caminho_arquivo: str) -> bool:
    adicionar_album(artistas, nome_artista, nome_album)
    for artista in artistas:
        if artista.nome == nome_artista:
            for album in artista.albuns:
                if album.nome == nome_album:
                    for musica in album.musicas:
                        if musica.nome == nome_musica:
                            print("Música já existe")
                            return False
                    album.adicionar_musica(nome_musica, caminho_arquivo)
                    return True

def carregar_dados() -> tuple:
    """Carrega dados de artistas e playlists do arquivo pickle"""
    if not Path(CAMINHO_ARQUIVO).exists():
        return [], []
        
    try:
        with open(CAMINHO_ARQUIVO, 'rb') as arquivo:
            dados = pickle.load(arquivo)
            artistas = dados.get('artistas', [])
            playlists = dados.get('playlists', [])
            return artistas, playlists
    except Exception as e:
        print(f"Erro ao carregar dados: {e}")
        return [], []

def copiar_musica(caminho: Path) -> bool:
    Path(PASTA_MUSICAS).mkdir(exist_ok=True)
    arquivo = Path(caminho)
    if arquivo.is_file() and arquivo.suffix in ('.mp3', '.wav', '.flac'):
        try:
            shutil.copy2(arquivo, PASTA_MUSICAS)
            print("Música copiada com sucesso!")
            return True
        except Exception as e:
            print(f"Erro ao copiar música: {e}")
            return False
    else:
        print("Arquivo não é um formato de música válido (.mp3, .wav, .flac)")
        return False

def limpas_musicas_orfaos(artistas):
    '''Remove musicas que não estão no pickle'''
    if Path(PASTA_MUSICAS).exists():
        musicas_validas = set()
        for artista in artistas:
            for album in artista.albuns:
                for musica in album.musicas:
                    musicas_validas.add(musica.nome_arquivo)
        
        for arquivo in Path(PASTA_MUSICAS).iterdir():
            if arquivo.name not in musicas_validas:
                arquivo.unlink()

def limpar_tela() -> None:
    os.system('cls' if os.name == 'nt' else 'clear')