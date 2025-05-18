import pickle
import os
from pathlib import Path

CAMINHO_ARQUIVO = "dados.pkl"

class Musica:
    def __init__(self, nome):
        self.__nome = nome

    @property
    def nome(self):
        return self.__nome

class Album:
    def __init__(self, nome):
        self.__nome = nome
        self.musicas = []

    @property
    def nome(self):
        return self.__nome
    
    def adicionar_musica(self, musica: list) -> None:
        self.musicas.append(Musica(musica))

class Artista:
    def __init__(self, nome: str):
        self.__nome = nome
        self.albuns = []

    @property
    def nome(self):
        return self.__nome
    
    def adicionar_album(self, nome_album:str) -> None:
        self.albuns.append(Album(nome_album))

def adicionar_artista(artistas: list, novo_artista: str) -> None:
    for artista in artistas:
        if artista.nome == novo_artista:
            return
    
    artistas.append(Artista(novo_artista))

    with open(CAMINHO_ARQUIVO, 'wb') as arquivo:
        pickle.dump(artistas, arquivo)

def adicionar_album(artistas:list, nome_artista: str, nome_album: str):
    adicionar_artista(artistas, nome_artista)
    for artista in artistas:
        if artista.nome == nome_artista:
            for album in artista.albuns:
                if album.nome == nome_album:
                    return 
            artista.adicionar_album(nome_album)
            with open(CAMINHO_ARQUIVO, 'wb') as arquivo:
                pickle.dump(artistas, arquivo)
            return

def adicionar_musica(artistas:list, nome_artista: str, nome_album: str, nome_musica: str):
    adicionar_album(artistas, nome_artista, nome_album)
    for artista in artistas:
        if artista.nome == nome_artista:
            for album in artista.albuns:
                if album.nome == nome_album:
                    for musica in album.musicas:
                        if musica.nome == nome_musica:
                            print("Musica ja existe")
                    album.adicionar_musica(nome_musica)
                    with open(CAMINHO_ARQUIVO, 'wb') as arquivo:
                        pickle.dump(artistas, arquivo)
                    return

def carregar_artistas() -> list:
    if not Path(CAMINHO_ARQUIVO).exists():
        return []
    
    try:
        with open(CAMINHO_ARQUIVO, 'rb') as arquivo:
            return pickle.load(arquivo)
    except (EOFError, pickle.PickleError):
        return []

def limpar_tela() -> None:
    os.system('cls' if os.name == 'nt' else 'clear')

##################################################################################

if __name__ == "__main__":
    artistas = carregar_artistas()

    continuar = True
    while continuar:
        limpar_tela()
        print("==========REPRODUTOR DE MUSICA==========")
        print("[1] - Adicionar Musica")
        print("[2] - Listar Biblioteca")
        print("[3] - Sair")
        opcao = int(input("Escolha: "))

        if opcao == 1:
            artista_nome = input("Digite o nome do artista: ")
            album = input("Digite o nome do album: ")
            musica = input("Digite o nome da música: ")
        
            adicionar_musica(artistas, artista_nome, album, musica)

        if opcao == 2:
            indice_artistas = 1
            for artista in artistas:
                print(f"[{indice_artistas}] - {artista.nome}")
                indice_artistas += 1

                indice_albuns = 1
                for album in artista.albuns:
                    print(f"    [{indice_albuns}] - {album.nome}")
                    indice_albuns += 1

                    indice_musicas = 1
                    for musica in album.musicas:
                        print(f"        [{indice_musicas}] - {musica.nome}")
                        indice_musicas += 1
                print("")

            input("Pressione Enter para voltar")

        if opcao == 3:
            continuar = False