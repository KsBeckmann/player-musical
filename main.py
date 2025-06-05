import pickle
import os
import pygame
import shutil
from pathlib import Path

CAMINHO_ARQUIVO = "dados.pkl"
PASTA_MUSICAS = "musicas"

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
    
    def adicionar_musica(self, musica, caminho_arquivo: list) -> None:
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

        pygame.mixer.music.play()

        print(f"--- '{nome_display_musica}' está tocando ---")

    def parar_musica():
        if pygame.mixer.get_init() and pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()

def salvar_dados(artistas):
    with open(CAMINHO_ARQUIVO, 'wb') as arquivo:
        pickle.dump(artistas, arquivo)

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

def carregar_artistas() -> list:
    if not Path(CAMINHO_ARQUIVO).exists():
        return []
    
    try:
        with open(CAMINHO_ARQUIVO, 'rb') as arquivo:
            return pickle.load(arquivo)
    except (EOFError, pickle.PickleError):
        return []

def copiar_musica(caminho: Path) -> bool:
    Path(PASTA_MUSICAS).mkdir(exist_ok=True)
    arquivo = Path(caminho)
    if arquivo.is_file() and arquivo.suffix in ('.mp3', '.wav', '.flac'):
        try:
            shutil.copy2(arquivo, PASTA_MUSICAS)
        except:
            return False
        return True
    else:
        return False

def limpar_tela() -> None:
    os.system('cls' if os.name == 'nt' else 'clear')
    
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

##################################################################################

if __name__ == "__main__":

    pygame.init()
    pygame.mixer.init()

    limpar_tela()
    artistas = carregar_artistas()
    musica_tocando_info = None
    continuar = True

    while continuar:
        print("==========REPRODUTOR DE MUSICA==========")
        print("[1] - Adicionar Musica")
        print("[2] - Listar Biblioteca")
        print("[3] - Buscar por nome")
        if pygame.mixer.get_init() and pygame.mixer.music.get_busy():
            print(f"[4] - Parar Música ('{musica_tocando_info['nome_display'] }')")
        else:
            print("[4] - Tocar Musica")
        print("[5] - Sair")
        opcao = input("Escolha: ")

        if opcao == '1':
            artista_nome = str(input("Digite o nome do artista: ")).lower()
            album = str(input("Digite o nome do album: ")).lower()
            musica = str(input("Digite o nome da música: ")).lower()
            musica_arquivo = Path(str(input("Digite o caminho da musica a ser adicionada: ")))
            if not copiar_musica(musica_arquivo):
                limpar_tela()
                print("Arquivo de musica não existe ou não tem a extensão certa")
                continue
            if adicionar_musica(artistas, artista_nome, album, musica, musica_arquivo.name):
                salvar_dados(artistas)
            limpar_tela()

        elif opcao == '2':
            limpar_tela()
            print("==========BIBLIOTECA==========")
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
            limpar_tela()
            
        elif opcao == '3':
            while True:
                limpar_tela()
                print("==========REPRODUTOR DE MUSICA==========")
                print("[1] - Artista")
                print("[2] - Album")
                print("[3] - Musica")
                print("[4] - Voltar")
                opcao_busca = str(input("Escolha: "))
                
                if opcao_busca == '1':
                    limpar_tela()
                    artista_busca = str(input("Artista: "))
                    resultado = buscar_artista(artistas, artista_busca)
                    limpar_tela()
                    indice_print_busca = 1
                    print("==========ARTISTAS ENCONTRADOS==========")
                    indice_artistas = 1
                    if resultado:
                        for artista in resultado:
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
                    else:
                        print("Nenhum artista encontrado")

                    input("\nPressione Enter para voltar")
                    limpar_tela()
                
                if opcao_busca == '2':
                    limpar_tela()
                    album_busca = str(input("Album: "))
                    resultado = buscar_album(artistas, album_busca)
                    limpar_tela()
                    print("==========ALBUNS ENCONTRADOS==========")
                    indice_artista = 1
                    if resultado:
                        for albuns in resultado:
                            nome_artista = albuns[0].nome
                            albuns_artista = albuns[1]
                            print(f"[{indice_artista}] - {nome_artista}")
                            indice_albuns = 1
                            for album in albuns_artista:
                                print(f"    [{indice_albuns}] - {album.nome}")
                                indice_albuns += 1
                                indice_musicas = 1
                                for musica in album.musicas:
                                    print(f"        [{indice_musicas}] - {musica.nome}")
                                    indice_musicas += 1
                    else:
                        print("Nenhum album encontrado")
                    input("\nPressione Enter para voltar")
                    limpar_tela()
                
                if opcao_busca == '3':
                    limpar_tela()
                    musica_busca = str(input("Música: ")).strip()
                    resultados = buscar_musica(artistas, musica_busca)
                    limpar_tela()
                    print("==========MÚSICAS ENCONTRADAS==========")
                    
                    if resultados:
                        indice_artista = 1
                        for artista, albuns_musicas in resultados:
                            print(f"[{indice_artista}] - {artista.nome}")
                            indice_artista += 1
                            
                            indice_album = 1
                            for album, musicas in albuns_musicas.items():
                                print(f"    [{indice_album}] - {album.nome}")
                                indice_album += 1
                                
                                indice_musica = 1
                                for musica in musicas:
                                    print(f"        [{indice_musica}] - {musica.nome}")
                                    indice_musica += 1
                    else:
                        print("Nenhuma música encontrada")
                    
                    input("\nPressione Enter para voltar")
                    limpar_tela()
                
                if opcao_busca == '4':
                    limpar_tela()
                    break

        elif opcao == '4':
            limpar_tela()
            if not pygame.mixer.get_init():
                print("Erro: Mixer do Pygame não está inicializado. Não é possível tocar música.")
                input("Pressione Enter para voltar.")
                continue
                
            if pygame.mixer.music.get_busy():
                musica_tocando_info = None
                input("Pressione Enter para voltar ao menu.")
                continue

            musicas_selecao = []
            if artistas:
                for artista_obj_fila in artistas:
                    for album_obj_fila in artista_obj_fila.albuns:
                        for musica_obj_fila in album_obj_fila.musicas:
                            musicas_selecao.append({
                                'nome_arquivo': musica_obj_fila.nome_arquivo,
                                'nome_display': musica_obj_fila.nome.title(),
                                'artista_nome': artista_obj_fila.nome.title()
                            })

            print("========== ESCOLHA UMA MÚSICA PARA TOCAR ==========")
            for idx, info_musica in enumerate(musicas_selecao):
                print(f"[{idx + 1}] - {info_musica['nome_display']} (Artista: {info_musica['artista_nome']})")
            
            print(f"[{len(musicas_selecao) + 1}] - Voltar ao Menu Principal")

            escolha_musica_str = input(f"Escolha (1-{len(musicas_selecao)+1}): ").strip()
            if not escolha_musica_str.isdigit():
                raise ValueError("Entrada inválida. Digite um número.")
                
            escolha_musica_num = int(escolha_musica_str)

            if escolha_musica_num == len(musicas_selecao) + 1:
                continue

            musica_selecionada = musicas_selecao[escolha_musica_num - 1]

            if Reprodutor.tocar_musica(
                musica_selecionada['nome_arquivo'],
                PASTA_MUSICAS,
                musica_selecionada['nome_display']
            ):
                musica_tocando_info = musica_selecionada
            else:
                musica_tocando_info = None
                input("Pressione Enter para voltaaaaaaaaar.")
                #Aqui dá problema se não parar a música depois do Enter, mas tá tarde, amanhã eu conserto
                Reprodutor.parar_musica()
                limpar_tela()

        elif opcao == '5':
            continuar = False
    
        else:
            limpar_tela()
            print("Opção inválida! Escolha novamente.")
            input("Pressione Enter para tentar novamente:")
            limpar_tela()

    limpar_tela()