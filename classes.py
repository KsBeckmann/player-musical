import os
import pygame

# CLASSES DE DADOS
class Musica:
    """representa uma única faixa de música"""
    def __init__(self, nome: str, nome_arquivo: str):
        self.__nome = nome
        self.__nome_arquivo = nome_arquivo

    @property
    def nome(self) -> str:
        return self.__nome
    
    @property
    def nome_arquivo(self) -> str:
        return self.__nome_arquivo

class Album:
    """representa um álbum, que é uma coleção de músicas"""
    def __init__(self, nome: str):
        self.__nome = nome
        self.musicas: list[Musica] = []

    @property
    def nome(self) -> str:
        return self.__nome
    
    def adicionar_musica(self, musica: str, caminho_arquivo: str) -> None:
        """adiciona um objeto Musica à lista de músicas do álbum"""
        self.musicas.append(Musica(musica, caminho_arquivo))

class Artista:
    """representa um artista, que possui uma coleção de álbuns"""
    def __init__(self, nome: str):
        self.__nome = nome
        self.albuns: list[Album] = []

    @property
    def nome(self) -> str:
        return self.__nome
    
    def adicionar_album(self, nome_album:str) -> None:
        """adiciona um objeto Album à lista de álbuns do artista"""
        self.albuns.append(Album(nome_album))

# PADRÃO DE PROJETO: FACADE
class Reprodutor:
    """
    atua como uma FACADE para simplificar as operações de áudio com Pygame
    
    ao inves de o cliente precisar saber como inicializar o Pygame, carregar um 
    arquivo, tocar, parar, etc., ele apenas interage com os métodos estáticos e 
    simples desta classe
    """
    @staticmethod
    def tocar_musica(nome_arquivo_musica: str, pasta_musicas: str, nome_display_musica: str = None) -> dict:
        """
        método da Facade que encapsula toda a lógica para tocar uma música.
        
        ele lida com:
        a inicialização do Pygame e do seu mixer
        a construção do caminho completo do arquivo
        a parada de qualquer música que já esteja tocando
        o carregamento da nova música
        a configuração do volume
        a execução da música
        o retorno de um status claro sobre o sucesso ou a falha da operação
        """
        if nome_display_musica is None:
            nome_display_musica = nome_arquivo_musica

        # garante que o subsistema Pygame está pronto para uso
        if not pygame.get_init():
            pygame.init()
        pygame.mixer.init()

        caminho_completo = os.path.join(pasta_musicas, nome_arquivo_musica)

        if pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()

        try:
            pygame.mixer.music.load(caminho_completo)
            pygame.mixer.music.set_volume(0.5)  # oo volume pode ser configurável
            pygame.mixer.music.play()
            print(f"--- '{nome_display_musica}' está tocando ---")
            return {
                'status': True,
                'nome_musica': nome_display_musica,
                'nome_arquivo': nome_arquivo_musica
            }
        except Exception as e:
            # a fachada também simplifica o tratamento de erros do subsistema
            print(f"Erro ao reproduzir música: {e}")
            return {
                'status': False,
                'erro': str(e)
            }

    @staticmethod
    def parar_musica() -> bool:
        """
        método da Facade que simplifica a ação de parar uma música
        
        ele verifica se o mixer está ativo e se uma música está tocando
        antes de tentar pará-la, evitando erros
        """
        if pygame.mixer.get_init() and pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()
            return True
        return False

# FUNÇÕES DE BUSCA
def buscar_artista(artistas: list[Artista], nome_artista: str) -> list[Artista]:
    """busca artistas cujo nome contenha o texto pesquisado"""
    artistas_encontrados = []
    for artista in artistas:
        if nome_artista.lower() in artista.nome.lower():
            artistas_encontrados.append(artista)
    return artistas_encontrados

def buscar_album(artistas: list[Artista], nome_album: str) -> list[tuple[Artista, list[Album]]]:
    """usca álbuns cujo nome contenha o texto pesquisado"""
    albuns_encontrados = []
    for artista in artistas:
        albuns = []
        album_encontrado = False
        for album in artista.albuns:
            if nome_album.lower() in album.nome.lower():
                albuns.append(album)
                album_encontrado = True
        if album_encontrado:
            albuns_encontrados.append((artista, albuns))
    return albuns_encontrados

def buscar_musica(artistas: list[Artista], nome_musica: str) -> list[tuple[Artista, dict[Album, list[Musica]]]]:
    """busca músicas cujo nome contenha o texto pesquisado"""
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