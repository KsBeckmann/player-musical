import pickle
import os
import shutil
from pathlib import Path
from classes import Artista, Album, Musica

CAMINHO_ARQUIVO = "dados.pkl"
PASTA_MUSICAS = "musicas"
CAMINHO_CONFIG = "config.pkl"

def salvar_dados(artistas: list[Artista], playlists: list = None):
    """
    salva os dados de artistas e playlists em um arquivo pickle

    args:
        artistas (list[Artista]): A lista de artistas
        playlists (list, optional): A lista de playlists
    """
    if playlists is None:
        playlists = []
    
    dados = {'artistas': artistas, 'playlists': playlists}
    with open(CAMINHO_ARQUIVO, 'wb') as arquivo:
        pickle.dump(dados, arquivo)

def carregar_dados() -> tuple[list[Artista], list]:
    """
    carrega os dados de artistas e playlists do arquivo pickle

    returns:
        tuple[list[Artista], list]: uma tupla contendo a lista de artistas e a lista de playlists
    """
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

def salvar_configuracoes(config: dict):
    """
    salva as configurações do usuario, como o volume

    args:
        config (dict): o dicionário de configurações
    """
    try:
        with open(CAMINHO_CONFIG, 'wb') as f:
            pickle.dump(config, f)
    except Exception as e:
        print(f"Erro ao salvar configurações: {e}")

def carregar_configuracoes() -> dict:
    """
    carrega as configurações do usuário

    returns:
        dict: o dicionario de configurações ou um dicionário padrao em caso de erro
    """
    if Path(CAMINHO_CONFIG).exists():
        try:
            with open(CAMINHO_CONFIG, 'rb') as f:
                return pickle.load(f)
        except Exception as e:
            print(f"Erro ao carregar configurações: {e}")
    return {'volume': 0.5}

def adicionar_artista(artistas: list[Artista], novo_artista: str) -> bool:
    """
    adiciona um novo artista a lista, se ele ainda não existir

    args:
        artistas (list[Artista]): a lista de artistas
        novo_artista (str): o nome do novo artista

    returns:
        bool: True se o artista foi adicionado e False caso contrário
    """
    if not any(artista.nome.lower() == novo_artista.lower() for artista in artistas):
        artistas.append(Artista(novo_artista))
        return True
    return False

def adicionar_album(artistas: list[Artista], nome_artista: str, nome_album: str) -> bool:
    """
    adiciona um novo álbum a um artista

    args:
        artistas (list[Artista]): a lista de artistas
        nome_artista (str): o nome do artista
        nome_album (str): o nome do novo álbum

    returns:
        bool: True se o álbum foi adicionado e False se ele já existia
    """
    adicionar_artista(artistas, nome_artista)
    for artista in artistas:
        if artista.nome.lower() == nome_artista.lower():
            if not any(album.nome.lower() == nome_album.lower() for album in artista.albuns):
                artista.adicionar_album(nome_album)
                return True
            return False
    return False

def adicionar_musica(artistas: list[Artista], nome_artista: str, nome_album: str, 
                    nome_musica: str, caminho_arquivo: str) -> bool:
    """
    adiciona uma nova música a um álbum

    args:
        artistas (list[Artista]): a lista de artistas
        nome_artista (str): o nome do artista
        nome_album (str): o nome do álbum
        nome_musica (str): o nome da nova música
        caminho_arquivo (str): o nome do arquivo da música

    returns:
        bool: True se a música foi adicionada e False se ela já existia
    """
    adicionar_album(artistas, nome_artista, nome_album)
    for artista in artistas:
        if artista.nome.lower() == nome_artista.lower():
            for album in artista.albuns:
                if album.nome.lower() == nome_album.lower():
                    if not any(musica.nome.lower() == nome_musica.lower() for musica in album.musicas):
                        album.adicionar_musica(nome_musica, caminho_arquivo)
                        return True
                    print("Música já existe.")
                    return False
    return False

def copiar_musica(caminho: Path) -> bool:
    """
    copia um arquivo de música para a pasta de músicas do projeto

    args:
        caminho (Path): o caminho do arquivo de música original

    returns:
        bool: True se a música foi copiada e False caso contrário
    """
    Path(PASTA_MUSICAS).mkdir(exist_ok=True)
    if caminho.is_file() and caminho.suffix.lower() in ('.mp3', '.wav', '.flac'):
        try:
            shutil.copy2(caminho, PASTA_MUSICAS)
            print("Música copiada com sucesso!")
            return True
        except Exception as e:
            print(f"Erro ao copiar música: {e}")
            return False
    else:
        print("Arquivo não é um formato de música válido (.mp3, .wav, .flac)")
        return False

def limpar_musicas_orfas(artistas):
    """remove da pasta 'musicas' os arquivos que não estão listados na biblioteca"""
    if Path(PASTA_MUSICAS).exists():
        musicas_validas = set()
        for artista in artistas:
            for album in artista.albuns:
                for musica in album.musicas:
                    musicas_validas.add(musica.nome_arquivo)
        
        for arquivo in Path(PASTA_MUSICAS).iterdir():
            if arquivo.name not in musicas_validas:
                # Remove o arquivo "órfão"
                arquivo.unlink()

def limpar_tela():
    """limpa a tela do console"""
    os.system('cls' if os.name == 'nt' else 'clear')