import pygame
from pathlib import Path
from classes import *
from utils import *
import os
from logger import Logger
from playlist import Playlist
import threading

class MenuReprodutor:
    def __init__(self):
        self.logger = Logger("MenuReprodutor", "reprodutor.log")
        self.artistas, self.playlists = carregar_dados()
        self.musica_tocando_info = None
        self.continuar = True
        self.logger.info("MenuReprodutor inicializado")
        self.playlist_thread = None
        self.playlist_tocando = False

    def menu_principal(self):
        try:
            pygame.init()
            pygame.mixer.init()
            self.logger.info("Pygame inicializado com sucesso")
        except pygame.error as e:
            self.logger.error(f"Erro crítico ao inicializar Pygame: {e}")
            print(f"Erro crítico ao inicializar Pygame: {e}. A reprodução de música não funcionará.")
            input("Pressione Enter para continuar mesmo assim ou feche o terminal.")

        while self.continuar:
            self.logger.debug("Exibindo menu principal")
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
            print("[6] - Gerenciar Playlists")
            print("[7] - Ajustar volume")
            print("[8] - Sair")
            
            if mixer_pronto and pygame.mixer.music.get_busy() and self.musica_tocando_info:
                print(f"\n --> Tocando agora: {self.musica_tocando_info['nome_display']} - {self.musica_tocando_info['artista_nome']}")

            opcao = input("Escolha: ").strip()
            self.logger.info(f"Opção selecionada: {opcao}")

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
                self.menu_playlists()
            elif opcao == '7':
                self.ajustar_volume()
            elif opcao == '8':
                self.logger.info("Usuário escolheu sair")
                if self.artistas:
                    limpas_musicas_orfaos(self.artistas)
                    salvar_dados(self.artistas, self.playlists)
                self.continuar = False
            else:
                self.logger.warning(f"Opção inválida selecionada: {opcao}")
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
        self.logger.info("Aplicação finalizada")

    def lidar_com_adicionar_musica(self):
        self.logger.info("Iniciando processo de adicionar música")
        limpar_tela()
        print("--- Adicionar Nova Música ---")
        artista = str(input("Nome do artista: ")).strip()
        album = str(input("Nome do álbum: ")).strip()
        musica = str(input("Nome da música: ")).strip()
        caminho_str = str(input("Caminho completo do arquivo da música: ")).strip()
        
        self.logger.debug(f"Dados inseridos - Artista: {artista}, Álbum: {album}, Música: {musica}, Caminho: {caminho_str}")
        
        if not all([artista, album, musica, caminho_str]):
            self.logger.error("Erro: Campos obrigatórios não preenchidos")
            print("\nErro: Todos os campos são obrigatórios.")
        else:
            if copiar_musica(Path(caminho_str)):
                adicionar_musica(self.artistas, artista, album, musica, Path(caminho_str).name)
                self.logger.info(f"Música adicionada com sucesso: {musica} - {artista}")
        input("\nPressione Enter para voltar ao menu.")

    def lidar_com_remover(self):
        self.logger.info("Iniciando processo de remoção")
        alteracoes = False
        while True:
            limpar_tela()
            print("--- Remover Música ---")
            print("[1] - Artista")
            print("[2] - Album")
            print("[3] - Musica")
            print("[4] - Sair")
            escolha = str(input("Escolha: "))
            self.logger.debug(f"Opção de remoção selecionada: {escolha}")

            if escolha == '1':
                limpar_tela()
                nome_artista = str(input("Artista: "))
                self.logger.debug(f"Tentando remover artista: {nome_artista}")
                if self.remover_artista(nome_artista):
                    self.logger.info(f"Artista {nome_artista} removido com sucesso")
                    print(f"Artista {nome_artista} removido com sucesso")
                    alteracoes = True
                else:
                    self.logger.warning(f"Artista não encontrado: {nome_artista}")
                    print("Artista não encontrado")
                input("\nAperte ENTER para continuar")

            if escolha == '2':
                limpar_tela()
                nome_artista = str(input("Artista: "))
                nome_album = str(input("Álbum: "))
                self.logger.debug(f"Tentando remover álbum: {nome_album} do artista: {nome_artista}")
                if remover_album(self.artistas, nome_artista, nome_album):
                    self.logger.info(f"Álbum {nome_album} removido com sucesso")
                    print(f"Álbum {nome_album} removido com sucesso")
                    alteracoes = True
                else:
                    self.logger.warning(f"Álbum não encontrado: {nome_album}")
                    print("Álbum não encontrado")
                input("\nAperte ENTER para continuar")

            if escolha == '3':
                limpar_tela()
                nome_artista = str(input("Artista: "))
                nome_album = str(input("Álbum: "))
                nome_musica = str(input("Musica: "))
                self.logger.debug(f"Tentando remover música: {nome_musica} do álbum: {nome_album}")
                if self.remover_musica(nome_artista, nome_album, nome_musica):
                    self.logger.info(f"Música {nome_musica} removida com sucesso")
                    print(f"Musica {nome_musica} removida com sucesso")
                    alteracoes = True
                else:
                    self.logger.warning(f"Música não encontrada: {nome_musica}")
                    print("Musica não encontrada")
                input("\nAperte ENTER para continuar")

            if escolha == '4':
                if alteracoes:
                    salvar_dados(self.artistas)
                    self.logger.info("Dados salvos após remoções")
                return
        
    def remover_artista(self, nome_artista: str) -> bool:
        nome_artista = nome_artista.lower()
        for i, artista in enumerate(self.artistas):
            if artista.nome.lower() == nome_artista:
                self.artistas.pop(i)
                return True
        return False

    def lidar_com_listar_biblioteca(self):
        self.logger.info("Listando biblioteca")
        limpar_tela()
        print("========== MINHA BIBLIOTECA ==========")
        if not self.artistas:
            self.logger.debug("Biblioteca vazia")
            print("\nSua biblioteca está vazia.")
        else:
            self.logger.debug(f"Listando {len(self.artistas)} artistas")
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
        self.logger.info("Iniciando busca")
        while True:
            limpar_tela()
            print("==========REPRODUTOR DE MUSICA==========")
            print("[1] - Artista")
            print("[2] - Album")
            print("[3] - Musica")
            print("[4] - Voltar")
            opcao_busca = str(input("Escolha: "))
            self.logger.debug(f"Tipo de busca selecionado: {opcao_busca}")
            
            if opcao_busca == '1':
                limpar_tela()
                artista_busca = str(input("Artista: "))
                self.logger.debug(f"Buscando artista: {artista_busca}")
                resultado = buscar_artista(self.artistas, artista_busca)
                limpar_tela()
                print("==========ARTISTAS ENCONTRADOS==========")
                if resultado:
                    self.logger.info(f"Encontrados {len(resultado)} artistas")
                    for artista in resultado:
                        print(f"{artista.nome}")
                        for album in artista.albuns:
                            print(f"  - {album.nome}")
                            for musica in album.musicas:
                                print(f"    - {musica.nome}")
                else:
                    self.logger.info("Nenhum artista encontrado na busca")
                    print("Nenhum artista encontrado")
                input("\nPressione Enter para voltar")
                limpar_tela()
            
            elif opcao_busca == '2':
                limpar_tela()
                album_busca = str(input("Album: "))
                self.logger.debug(f"Buscando álbum: {album_busca}")
                resultado = buscar_album(self.artistas, album_busca)
                limpar_tela()
                print("==========ALBUNS ENCONTRADOS==========")
                if resultado:
                    self.logger.info(f"Encontrados álbuns em {len(resultado)} artistas")
                    for artista, albuns in resultado:
                        print(f"{artista.nome}")
                        for album in albuns:
                            print(f"  - {album.nome}")
                            for musica in album.musicas:
                                print(f"    - {musica.nome}")
                else:
                    self.logger.info("Nenhum álbum encontrado na busca")
                    print("Nenhum album encontrado")
                input("\nPressione Enter para voltar")
                limpar_tela()
            
            elif opcao_busca == '3':
                limpar_tela()
                musica_busca = str(input("Música: ")).strip()
                self.logger.debug(f"Buscando música: {musica_busca}")
                resultados = buscar_musica(self.artistas, musica_busca)
                limpar_tela()
                print("==========MÚSICAS ENCONTRADAS==========")
                
                if resultados:
                    self.logger.info(f"Encontradas músicas em {len(resultados)} artistas")
                    for artista, albuns_musicas in resultados:
                        print(f"{artista.nome}")
                        for album, musicas in albuns_musicas.items():
                            print(f"  {album.nome}")
                            for musica in musicas:
                                print(f"    - {musica.nome}")
                else:
                    self.logger.info("Nenhuma música encontrada na busca")
                    print("Nenhuma música encontrada")
                input("\nPressione Enter para voltar")
                limpar_tela()
            
            elif opcao_busca == '4':
                self.logger.debug("Saindo da busca")
                limpar_tela()
                break

    def lidar_com_tocar_parar_musica(self):
        if pygame.mixer.get_init() and pygame.mixer.music.get_busy():
            self.logger.info("Parando música em reprodução")
            Reprodutor.parar_musica()
            print("\nMúsica parada.")
            input("Pressione Enter para voltar.")
            return None

        self.logger.info("Iniciando seleção de música para reprodução")
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
            self.logger.warning("Tentativa de reprodução com biblioteca vazia")
            print("Biblioteca vazia. Adicione músicas primeiro.")
            input("Pressione Enter para voltar.")
            return None

        self.logger.debug(f"Exibindo {len(fila_de_musicas)} músicas disponíveis")
        print("========== ESCOLHA UMA MÚSICA PARA TOCAR ==========")
        for i, info in enumerate(fila_de_musicas):
            print(f"[{i+1}] - {info['nome_display']} (Artista: {info['artista_nome']})")
        print(f"[{len(fila_de_musicas)+1}] - Voltar")

        try:
            escolha_str = input(f"Escolha (1-{len(fila_de_musicas)+1}): ").strip()
            escolha_num = int(escolha_str)
            self.logger.debug(f"Escolha do usuário: {escolha_num}")

            if escolha_num == len(fila_de_musicas) + 1: 
                self.logger.debug("Usuário escolheu voltar")
                return None
            
            if 1 <= escolha_num <= len(fila_de_musicas):
                musica_selecionada = fila_de_musicas[escolha_num - 1]
                self.logger.info(f"Tentando reproduzir: {musica_selecionada['nome_display']} - {musica_selecionada['artista_nome']}")
                if Reprodutor.tocar_musica(
                    musica_selecionada['nome_arquivo'],
                    PASTA_MUSICAS,
                    musica_selecionada['nome_display']
                ):
                    self.logger.info("Música iniciada com sucesso")
                    return musica_selecionada
            else:
                self.logger.warning(f"Escolha inválida: {escolha_num}")
                print("\nEscolha inválida.")
                input("Pressione Enter para voltar.")
        except (ValueError, IndexError):
            self.logger.error(f"Entrada inválida: {escolha_str}")
            print("\nEntrada inválida. Por favor, digite um número da lista.")
            input("Pressione Enter para voltar.")
        
        return None
    
    def menu_playlists(self):
        while(True):
            limpar_tela()
            print("========== GERENCIAR PLAYLISTS ==========")
            print("[1] - Criar Playlist")
            print("[2] - Adicionar Música a Playlist")
            print("[3] - Listar playlists")
            if self.playlist_tocando:
                print("[4] - Parar reprodução da playlist")
            else:
                print("[4] - Tocar playlist")
            print("[5] - Voltar")

            opcao = input("Escolha: ").strip()

            if opcao == '1':
                nome = input("Nome da nova playlist: ").strip()
                if nome and not any(p.nome == nome for p in self.playlists):
                    self.playlists.append(Playlist(nome))
                    salvar_dados(self.artistas, self.playlists)

            elif opcao == '2':
                while True:
                    limpar_tela()
                    if not self.playlists:
                        print("Nenhuma playlist encontrada.")
                        input("Aperte ENTER para voltar")
                        break

                    self.listar_playlists()
                    opcao_playlist = input("Escolha uma playlist para adicionar música (ou 0 para voltar): ").strip()

                    if opcao_playlist == '0':
                        break

                    try:
                        opcao_playlist = int(opcao_playlist) - 1
                        if opcao_playlist < 0 or opcao_playlist >= len(self.playlists):
                            self.logger.warning("Opção de playlist inválida.")
                            print("Opção inválida de playlist.")
                            input("Pressione ENTER para continuar")
                            continue

                        playlist_escolhida = self.playlists[opcao_playlist]

                        while True:
                            limpar_tela()
                            if not self.artistas:
                                print("\nSua biblioteca está vazia.")
                                input("Pressione ENTER para continuar")
                                break

                            print(f"=== Músicas Disponíveis (Playlist: {playlist_escolhida.nome}) ===")
                            musicas = []
                            for i, art in enumerate(self.artistas):
                                for alb in art.albuns:
                                    for mus in alb.musicas:
                                        print(f"[{len(musicas) + 1}] {mus.nome.title()} (Álbum: {alb.nome})")
                                        musicas.append(mus)

                            print("\n[0] - Voltar")
                            opcao_musica = input("Escolha uma música (ou 0 para voltar): ").strip()

                            if opcao_musica == '0':
                                break

                            try:
                                indice = int(opcao_musica) - 1
                                if indice < 0 or indice >= len(musicas):
                                    raise ValueError("Índice fora do intervalo.")

                                musica_escolhida = musicas[indice]
                                playlist_escolhida.adicionar_musica(musica_escolhida)
                                salvar_dados(self.artistas, self.playlists)

                                print(f"Música '{musica_escolhida.nome}' adicionada à playlist '{playlist_escolhida.nome}'!")
                                input("Pressione ENTER para continuar")
                            except ValueError:
                                print("Opção inválida! Digite um número da lista.")
                                input("Pressione ENTER para continuar")

                    except ValueError:
                        print("Opção inválida! Digite um número da lista.")
                        input("Pressione ENTER para continuar")


            elif opcao == '3':
                while True:
                    limpar_tela()
                    print("=== Playlists ===")
                    self.listar_playlists()
                    print(f"[{len(self.playlists) + 1}] - Voltar")

                    opcao = input("Escolha uma playlist para mostrá-la: ").strip()
                    opcao = int(opcao) - 1

                    if opcao == len(self.playlists):
                        break

                    if opcao < 0 or opcao >= len(self.playlists):
                        continue
                    
                    limpar_tela()
                    if not self.playlists[opcao].musicas:
                        print("Playlist vazia.")
                    else:
                        for i, musica in enumerate(self.playlists[opcao].musicas):
                            print(f"[{i + 1}] - {musica.nome}")
                    
                    input("Pressione ENTER para continuar: ")
            
            elif opcao == '4':
                if self.playlist_tocando:
                    self.logger.info("Parando reprodução da playlist")
                    Reprodutor.parar_musica()
                    self.playlist_tocando = False
                    if self.playlist_thread and self.playlist_thread.is_alive():
                        self.playlist_thread.join(timeout=1)
                    print("\nPlaylist parada.")
                    input("Pressione Enter para voltar.")
                    return

                if not self.playlists:
                    print("Nenhuma playlist disponível.")
                    input("Pressione ENTER para voltar")
                    return

                limpar_tela()
                print("========== ESCOLHA UMA PLAYLIST ==========")
                for i, pl in enumerate(self.playlists):
                    print(f"[{i+1}] - {pl.nome}")
                print(f"[{len(self.playlists)+1}] - Voltar")

                try:
                    escolha_str = input(f"Escolha (1-{len(self.playlists)+1}): ").strip()
                    escolha_num = int(escolha_str)
                    self.logger.debug(f"Escolha de playlist: {escolha_num}")

                    if escolha_num == len(self.playlists) + 1:
                        return

                    if 1 <= escolha_num <= len(self.playlists):
                        playlist_escolhida = self.playlists[escolha_num - 1]
                        self.logger.info(f"Iniciando reprodução da playlist: {playlist_escolhida.nome}")

                        self.playlist_thread = threading.Thread(
                            target=self.reproduzir_playlist_thread,
                            args=(playlist_escolhida,),
                            daemon=True
                        )
                        self.playlist_tocando = True
                        self.playlist_thread.start()
                        print("Playlist está tocando em segundo plano. Use a opção [4] novamente para parar.")
                        input("Pressione ENTER para voltar.")
                    else:
                        print("Escolha inválida.")
                        input("Pressione ENTER para voltar.")
                except (ValueError, IndexError):
                    self.logger.error("Entrada inválida para seleção de playlist.")
                    print("Entrada inválida. Por favor, digite um número da lista.")
                    input("Pressione ENTER para voltar.")

            elif opcao == '5':
                break

    def listar_playlists(self):
        for i, playlist in enumerate(self.playlists):
            print(f"[{i+1}] - {playlist.nome}")

    def reproduzir_playlist_thread(self, playlist):
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.set_volume(0.5)

        for musica in playlist.musicas:
            if not self.playlist_tocando:
                break

            caminho = os.path.join(PASTA_MUSICAS, musica.nome_arquivo)

            if not os.path.exists(caminho):
                print(f"[ERRO] Arquivo '{musica.nome_arquivo}' não encontrado. Pulando.")
                continue

            self.logger.info(f"Tocando: {musica.nome}")
            pygame.mixer.music.load(caminho)
            pygame.mixer.music.play()

            while pygame.mixer.music.get_busy():
                if not self.playlist_tocando:
                    pygame.mixer.music.stop()
                    break
                pygame.time.Clock().tick(10)

        self.playlist_tocando = False

    def remover_musica(self, nome_artista: str, nome_album: str, nome_musica: str) -> bool:
        nome_artista = nome_artista.lower()
        nome_album = nome_album.lower()
        nome_musica = nome_musica.lower()
        musica_removida = None

        for artista in self.artistas:
            if artista.nome.lower() == nome_artista:
                for album in artista.albuns:
                    if album.nome.lower() == nome_album:
                        for i, musica in enumerate(album.musicas):
                            if musica.nome.lower() == nome_musica:
                                musica_removida = album.musicas.pop(i)
                                break

        if musica_removida:
            for playlist in self.playlists:
                playlist.remover_musica(musica_removida)
            return True
        return False
    
    def ajustar_volume(self):
        while True:
            limpar_tela()
            volume_atual = round(pygame.mixer.music.get_volume() * 100)
            print(f"=== AJUSTAR VOLUME (Atual: {volume_atual}%) ===")
            print("[1] - Definir volume (0-100%)")
            print("[2] - Voltar")
            
            opcao = input("Escolha: ").strip()
            
            if opcao == '1':
                try:
                    volume_input = int(input("Digite o volume desejado (0-100): "))
                    volume_input = max(0, min(volume_input, 100))
                    novo_volume = volume_input / 100
                    pygame.mixer.music.set_volume(novo_volume)
                    self.logger.info(f"Volume definido para {volume_input}%")
                    print(f"Volume definido para {volume_input}%")
                    input("Pressione ENTER para continuar.")
                except ValueError:
                    self.logger.error("Valor inválido. Digite um número inteiro entre 0 e 100.")
                    print("Valor inválido. Digite um número inteiro entre 0 e 100.")
                    input("Pressione ENTER para continuar.")
                    
            elif opcao == '2':
                break
            else:
                print("Opção inválida.")
                input("Pressione ENTER para continuar.")

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