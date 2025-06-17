import os
import pygame

# Classes

class Musica:
    def __init__(self, nome, nome_arquivo):
        self.__nome = nome
        self.__nome_arquivo = nome_arquivo

    @property
    def nome(self):
        return self.__nome
    
    @property
    def nome_arquivo(self):
        return self.__nome_arquivo

class Album:
    def __init__(self, nome):
        self.__nome = nome
        self.musicas = []

    @property
    def nome(self):
        return self.__nome
    
    def adicionar_musica(self, musica: str, caminho_arquivo: str) -> None:
        self.musicas.append(Musica(musica, caminho_arquivo))

class Artista:
    def __init__(self, nome: str):
        self.__nome = nome
        self.albuns = []

    @property
    def nome(self):
        return self.__nome
    
    def adicionar_album(self, nome_album:str) -> None:
        self.albuns.append(Album(nome_album))

class Reprodutor:
    def tocar_musica(nome_arquivo_musica: str, pasta_musicas: str, nome_display_musica: str = None) -> bool:
        if nome_display_musica is None:
            nome_display_musica = nome_arquivo_musica

        if not pygame.get_init():
            pygame.init()
        pygame.mixer.init()

        caminho_completo = os.path.join(pasta_musicas, nome_arquivo_musica)

        if pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()

        pygame.mixer.music.load(caminho_completo)
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play()

        print(f"--- '{nome_display_musica}' está tocando ---")

    def parar_musica():
        if pygame.mixer.get_init() and pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()

# Funções de Busca

def buscar_artista(artistas: list, nome_artista: str) -> list:
    artistas_encontrados = []
    for artista in artistas:
        if nome_artista in artista.nome:
            artistas_encontrados.append(artista)
    return artistas_encontrados

def buscar_album(artistas: list, nome_album: str) -> list:
    albuns_encontrados = []
    for artista in artistas:
        albuns = []
        album_encontrado = False
        for album in artista.albuns:
            if nome_album in album.nome:
                albuns.append(album)
                album_encontrado = True
        if album_encontrado:
            albuns_encontrados.append((artista, albuns))
    return albuns_encontrados

def buscar_musica(artistas: list, nome_musica: str) -> list:
    resultados = []
    for artista in artistas:
        albuns_musicas = {}
        
        for album in artista.albuns:
            musicas_encontradas = [
                musica for musica in album.musicas 
                if nome_musica.lower() in musica.nome.lower()
            ]
            if musicas_encontradas:
                albuns_musicas[album] = musicas_encontradas
        
        if albuns_musicas:
            resultados.append((artista, albuns_musicas))
    
    return resultados
