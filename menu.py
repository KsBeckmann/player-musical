import pygame
from pathlib import Path
from classes import *
from utils import *

class MenuReprodutor:
    def __init__(self):
        self.artistas = carregar_artistas()
        self.musica_tocando_info = None
        self.continuar = True

    def menu_principal(self):
        try:
            pygame.init()
            pygame.mixer.init()
        except pygame.error as e:
            print(f"Erro crítico ao inicializar Pygame: {e}. A reprodução de música não funcionará.")
            input("Pressione Enter para continuar mesmo assim ou feche o terminal.")

        while self.continuar:
            limpar_tela()
            print("========== REPRODUTOR DE MÚSICA ==========")
            print("[1] - Adicionar Música")
            print("[2] - Remover")
            print("[3] - Listar Biblioteca")
            print("[4] - Buscar por Nome")
            
            mixer_pronto = pygame.mixer.get_init() is not None
            if mixer_pronto and pygame.mixer.music.get_busy():
                nome_musica = self.musica_tocando_info['nome_display'] if self.musica_tocando_info else "Faixa Atual"
                print(f"[5] - Parar Música ('{nome_musica}')")
            else:
                print("[5] - Tocar Música")
            
            print("[6] - Sair")
            
            if mixer_pronto and pygame.mixer.music.get_busy() and self.musica_tocando_info:
                print(f"\n --> Tocando agora: {self.musica_tocando_info['nome_display']} - {self.musica_tocando_info['artista_nome']}")

            opcao = input("Escolha: ").strip()

            if opcao == '1':
                self.lidar_com_adicionar_musica()
                salvar_dados(self.artistas)
            elif opcao == '2':
                self.lidar_com_remover()
                salvar_dados(self.artistas)
            elif opcao == '3':
                self.lidar_com_listar_biblioteca()
            elif opcao == '4':
                self.lidar_com_busca()
            elif opcao == '5':
                self.musica_tocando_info = self.lidar_com_tocar_parar_musica()
            elif opcao == '6':
                if self.artistas:
                    limpas_musicas_orfaos(self.artistas)
                    salvar_dados(self.artistas)
                self.continuar = False
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

    def lidar_com_adicionar_musica(self):
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
                adicionar_musica(self.artistas, artista, album, musica, Path(caminho_str).name)
        input("\nPressione Enter para voltar ao menu.")

    def lidar_com_remover(self):
        alteracoes = False
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
                if self.remover_artista(nome_artista):
                    print(f"Artista {nome_artista} removido com sucesso")
                    alteracoes = True
                else:
                    print("Artista não encontrado")
                input("\nAperte ENTER para continuar")

            if escolha == '2':
                limpar_tela()
                nome_artista = str(input("Artista: "))
                nome_album = str(input("Álbum: "))
                if remover_album(self.artistas, nome_artista, nome_album):
                    print(f"Álbum {nome_album} removido com sucesso")
                    alteracoes = True
                else:
                    print("Álbum não encontrado")
                input("\nAperte ENTER para continuar")

            if escolha == '3':
                limpar_tela()
                nome_artista = str(input("Artista: "))
                nome_album = str(input("Álbum: "))
                nome_musica = str(input("Musica: "))
                if remover_musica(self.artistas, nome_artista, nome_album, nome_musica):
                    print(f"Musica {nome_musica} removida com sucesso")
                    alteracoes = True
                else:
                    print("Musica não encontrada")
                input("\nAperte ENTER para continuar")

            if escolha == '4':
                if alteracoes:
                    salvar_dados(self.artistas)
                return
        
    def remover_artista(self, nome_artista: str) -> bool:
        nome_artista = nome_artista.lower()
        for i, artista in enumerate(self.artistas):
            if artista.nome.lower() == nome_artista:
                self.artistas.pop(i)
                return True
        return False

    def lidar_com_listar_biblioteca(self):
        limpar_tela()
        print("========== MINHA BIBLIOTECA ==========")
        if not self.artistas:
            print("\nSua biblioteca está vazia.")
        else:
            for art_obj in self.artistas:
                print(f"\nArtista: {art_obj.nome.title()}")
                if not art_obj.albuns: print("  (Nenhum álbum)")
                for alb_obj in art_obj.albuns:
                    print(f"  Álbum: {alb_obj.nome.title()}")
                    if not alb_obj.musicas: print("    (Nenhuma música)")
                    for mus_obj in alb_obj.musicas:
                        print(f"    - {mus_obj.nome.title()} (Arquivo: {mus_obj.nome_arquivo})")
        input("\nPressione Enter para voltar ao menu.")

    def lidar_com_busca(self):
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
                resultado = buscar_artista(self.artistas, artista_busca)
                limpar_tela()
                print("==========ARTISTAS ENCONTRADOS==========")
                if resultado:
                    for artista in resultado:
                        print(f"{artista.nome}")
                        for album in artista.albuns:
                            print(f"  - {album.nome}")
                            for musica in album.musicas:
                                print(f"    - {musica.nome}")
                else:
                    print("Nenhum artista encontrado")
                input("\nPressione Enter para voltar")
                limpar_tela()
            
            elif opcao_busca == '2':
                limpar_tela()
                album_busca = str(input("Album: "))
                resultado = buscar_album(self.artistas, album_busca)
                limpar_tela()
                print("==========ALBUNS ENCONTRADOS==========")
                if resultado:
                    for artista, albuns in resultado:
                        print(f"{artista.nome}")
                        for album in albuns:
                            print(f"  - {album.nome}")
                            for musica in album.musicas:
                                print(f"    - {musica.nome}")
                else:
                    print("Nenhum album encontrado")
                input("\nPressione Enter para voltar")
                limpar_tela()
            
            elif opcao_busca == '3':
                limpar_tela()
                musica_busca = str(input("Música: ")).strip()
                resultados = buscar_musica(self.artistas, musica_busca)
                limpar_tela()
                print("==========MÚSICAS ENCONTRADAS==========")
                
                if resultados:
                    for artista, albuns_musicas in resultados:
                        print(f"{artista.nome}")
                        for album, musicas in albuns_musicas.items():
                            print(f"  {album.nome}")
                            for musica in musicas:
                                print(f"    - {musica.nome}")
                else:
                    print("Nenhuma música encontrada")
                input("\nPressione Enter para voltar")
                limpar_tela()
            
            elif opcao_busca == '4':
                limpar_tela()
                break

    def lidar_com_tocar_parar_musica(self):
        if pygame.mixer.get_init() and pygame.mixer.music.get_busy():
            Reprodutor.parar_musica()
            print("\nMúsica parada.")
            input("Pressione Enter para voltar.")
            return None

        limpar_tela()
        fila_de_musicas = []
        for art in self.artistas:
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
        
        return None

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

def remover_musica(artistas: list, nome_artista: str, nome_album: str, nome_musica: str):
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