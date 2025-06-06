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
        print("[2] - Listar Biblioteca")
        print("[3] - Buscar por Nome")
        
        mixer_pronto = pygame.mixer.get_init() is not None
        if mixer_pronto and pygame.mixer.music.get_busy():
            nome_musica = musica_tocando_info['nome_display'] if musica_tocando_info else "Faixa Atual"
            print(f"[4] - Parar Música ('{nome_musica}')")
        else:
            print("[4] - Tocar Música")
        
        print("[5] - Sair")
        
        if mixer_pronto and pygame.mixer.music.get_busy() and musica_tocando_info:
            print(f"\n --> Tocando agora: {musica_tocando_info['nome_display']} - {musica_tocando_info['artista_nome']}")

        opcao = input("Escolha: ").strip()

        if opcao == '1':
            lidar_com_adicionar_musica(artistas)
            salvar_dados(artistas)
        elif opcao == '2':
            lidar_com_listar_biblioteca(artistas)
        elif opcao == '3':
            lidar_com_busca(artistas)
        elif opcao == '4':
            musica_tocando_info = lidar_com_tocar_parar_musica(artistas, musica_tocando_info)
        elif opcao == '5':
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

def lidar_com_busca(artistas):
    """Gerencia o sub-menu de busca."""
    limpar_tela()
    termo = str(input("Digite o nome da música, álbum ou artista para buscar: ")).strip()
    if not termo: return

    print(f"\n--- Resultados da busca por '{termo}' ---")
    # Busca por música, que é a mais detalhada
    resultados_musica = buscar_musica(artistas, termo)
    
    if resultados_musica:
        for artista, albuns_map in resultados_musica:
            print(f"\nArtista: {artista.nome.title()}")
            for album, musicas in albuns_map.items():
                print(f"  Álbum: {album.nome.title()}")
                for musica in musicas:
                    print(f"    -> Música Encontrada: {musica.nome.title()}")
    else:
        print("Nenhum resultado encontrado para o termo.")
    input("\nPressione Enter para voltar ao menu.")

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
