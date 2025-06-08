import pygame
from pathlib import Path
from classes import *
from utils import *

def menu_principal():
    try:
        pygame.init()
        pygame.mixer.init()
    except pygame.error as e:
        print(f"Erro crítico ao inicializar Pygame: {e}. A reprodução de música não funcionará.")
        input("Pressione Enter para continuar mesmo assim ou feche o terminal.")

    artistas = carregar_artistas()
    musica_tocando_info = None
    continuar = True

    while continuar:
        limpar_tela()
        print("========== REPRODUTOR DE MÚSICA ==========")
        print("[1] - Adicionar Música")
        print("[2] - Remover")
        print("[3] - Listar Biblioteca")
        print("[4] - Buscar por Nome")
        
        mixer_pronto = pygame.mixer.get_init() is not None
        if mixer_pronto and pygame.mixer.music.get_busy():
            nome_musica = musica_tocando_info['nome_display'] if musica_tocando_info else "Faixa Atual"
            print(f"[5] - Parar Música ('{nome_musica}')")
        else:
            print("[5] - Tocar Música")
        
        print("[6] - Sair")
        
        if mixer_pronto and pygame.mixer.music.get_busy() and musica_tocando_info:
            print(f"\n --> Tocando agora: {musica_tocando_info['nome_display']} - {musica_tocando_info['artista_nome']}")

        opcao = input("Escolha: ").strip()

        if opcao == '1':
            lidar_com_adicionar_musica(artistas)
            salvar_dados(artistas)
        elif opcao == '2':
            lidar_com_remover(artistas)
            salvar_dados(artistas)
        elif opcao == '3':
            lidar_com_listar_biblioteca(artistas)
        elif opcao == '4':
            lidar_com_busca(artistas)
        elif opcao == '5':
            musica_tocando_info = lidar_com_tocar_parar_musica(artistas, musica_tocando_info)
        elif opcao == '6':
            if artistas:
                limpas_musicas_orfaos(artistas)
                salvar_dados(artistas)
            continuar = False
        else:
            print("\nOpção inválida! Pressione Enter para tentar novamente.")
            input()

    # Finalização
    if pygame.get_init() and pygame.mixer.get_init() and pygame.mixer.music.get_busy():
        Reprodutor.parar_musica()
    limpar_tela()
    print("Obrigado por usar o Reprodutor de Música!")
    if pygame.get_init():
        pygame.quit()
    print("Recursos do Pygame liberados. Até logo!")

def lidar_com_adicionar_musica(artistas):
    """Lida com a lógica de coletar dados e adicionar uma nova música."""
    limpar_tela()
    print("--- Adicionar Nova Música ---")
    artista = str(input("Nome do artista: ")).strip()
    album = str(input("Nome do álbum: ")).strip()
    musica = str(input("Nome da música: ")).strip()
    caminho_str = str(input("Caminho completo do arquivo da música: ")).strip()
    
    if not all([artista, album, musica, caminho_str]):
        print("\nErro: Todos os campos são obrigatórios.")
    else:
        if copiar_musica(Path(caminho_str)):
            adicionar_musica(artistas, artista, album, musica, Path(caminho_str).name)
    input("\nPressione Enter para voltar ao menu.")

def lidar_com_remover(artistas):
    '''Gerencia o sub-menu de remoção.'''
    alteracoes: bool = False
    while True:
        limpar_tela()
        print("--- Remover Música ---")
        print("[1] - Artista")
        print("[2] - Album")
        print("[3] - Musica")
        print("[4] - Sair")
        escolha = str(input("Escolha: "))

        if escolha == '1':
            limpar_tela()
            nome_artista = str(input("Artista: "))
            if remover_artista(artistas, nome_artista):
                print(f"Artista {nome_artista} removido com sucesso")
                alteracoes: bool = True
            else:
                print("Artista não encontrado")
            input("\nAperte ENTER para continuar")

        if escolha == '2':
            limpar_tela()
            nome_artista = str(input("Artista: "))
            nome_album = str(input("Álbum: "))
            if remover_album(artistas, nome_artista, nome_album):
                print(f"Álbum {nome_album} removido com sucesso")
                alteracoes: bool = True
            else:
                print("Álbum não encontrado")
            input("\nAperte ENTER para continuar")

        if escolha == '3':
            limpar_tela()
            nome_artista = str(input("Artista: "))
            nome_album = str(input("Álbum: "))
            nome_musica = str(input("Musica: "))
            if remover_musica(artistas, nome_artista, nome_album, nome_musica):
                print(f"Musica {nome_musica} removida com sucesso")
                alteracoes: bool = True
            else:
                print("Musica não encontrada")
            input("\nAperte ENTER para continuar")

        if escolha == '4':
            if alteracoes:
                salvar_dados(artistas)
            return
        
def remover_artista(artistas: list, nome_artista: str) -> bool:
    nome_artista = nome_artista.lower()
    for i, artista in enumerate(artistas):
        if artista.nome.lower() == nome_artista:
            artistas.pop(i)
            return True
    return False

def remover_album(artistas: list, nome_artista: str, nome_album: str) -> bool:
    nome_artista = nome_artista.lower()
    nome_album = nome_album.lower()
    for artista in artistas:
        if artista.nome.lower() == nome_artista:
            for i, album in enumerate(artista.albuns):
                if album.nome.lower() == nome_album:
                    artista.albuns.pop(i)
                    return True
    return False

def remover_musica(artistas: list, nome_artista:str, nome_album: str, nome_musica: str):
    nome_artista = nome_artista.lower()
    nome_album = nome_album.lower()
    nome_musica = nome_musica.lower()
    for artista in artistas:
        if artista.nome.lower() == nome_artista:
            for album in artista.albuns:
                if album.nome.lower() == nome_album:
                    for i, musica in enumerate(album.musicas):
                        if musica.nome.lower() == nome_musica:
                            album.musicas.pop(i)
                            return True
    return False

def lidar_com_listar_biblioteca(artistas):
    """Exibe toda a biblioteca de músicas de forma organizada."""
    limpar_tela()
    print("========== MINHA BIBLIOTECA ==========")
    if not artistas:
        print("\nSua biblioteca está vazia.")
    else:
        for art_obj in artistas:
            print(f"\nArtista: {art_obj.nome.title()}")
            if not art_obj.albuns: print("  (Nenhum álbum)")
            for alb_obj in art_obj.albuns:
                print(f"  Álbum: {alb_obj.nome.title()}")
                if not alb_obj.musicas: print("    (Nenhuma música)")
                for mus_obj in alb_obj.musicas:
                    print(f"    - {mus_obj.nome.title()} (Arquivo: {mus_obj.nome_arquivo})")
    input("\nPressione Enter para voltar ao menu.")

def lidar_com_busca(artistas: list):
    """Gerencia o sub-menu de busca."""
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

def lidar_com_tocar_parar_musica(artistas, musica_info_atual):
    """Alterna entre tocar e parar a música, retornando o novo estado da música."""
    if pygame.mixer.get_init() and pygame.mixer.music.get_busy():
        Reprodutor.parar_musica()
        print("\nMúsica parada.")
        input("Pressione Enter para voltar.")
        return None

    # Mostra a lista para tocar uma nova
    limpar_tela()
    fila_de_musicas = []
    for art in artistas:
        for alb in art.albuns:
            for mus in alb.musicas:
                fila_de_musicas.append({
                    'nome_arquivo': mus.nome_arquivo,
                    'nome_display': mus.nome.title(),
                    'artista_nome': art.nome.title()
                })
    
    if not fila_de_musicas:
        print("Biblioteca vazia. Adicione músicas primeiro.")
        input("Pressione Enter para voltar.")
        return None

    print("========== ESCOLHA UMA MÚSICA PARA TOCAR ==========")
    for i, info in enumerate(fila_de_musicas):
        print(f"[{i+1}] - {info['nome_display']} (Artista: {info['artista_nome']})")
    print(f"[{len(fila_de_musicas)+1}] - Voltar")

    try:
        escolha_str = input(f"Escolha (1-{len(fila_de_musicas)+1}): ").strip()
        escolha_num = int(escolha_str)

        if escolha_num == len(fila_de_musicas) + 1: return None
        
        if 1 <= escolha_num <= len(fila_de_musicas):
            musica_selecionada = fila_de_musicas[escolha_num - 1]
            if Reprodutor.tocar_musica(
                musica_selecionada['nome_arquivo'],
                PASTA_MUSICAS,
                musica_selecionada['nome_display']
            ):
                return musica_selecionada
        else:
            print("\nEscolha inválida.")
            input("Pressione Enter para voltar.")
    except (ValueError, IndexError):
        print("\nEntrada inválida. Por favor, digite um número da lista.")
        input("Pressione Enter para voltar.")
    
    return None # Retorna None se nada foi tocado ou houve erro
