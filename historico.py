import pickle
from pathlib import Path
from datetime import datetime
from logger import Logger

CAMINHO_HISTORICO = "historico.pkl"

class HistoricoReproducao:
    """
    Gerencia o histórico de reprodução de músicas.

    Atributos:
        logger (Logger): A instância do logger.
        registros (list[dict]): A lista de registros do histórico.
    """
    def __init__(self):
        self.logger = Logger()
        self.registros = self._carregar_historico()

    def adicionar_registro(self, nome_musica: str, artista: str, data_hora=None):
        """
        Adiciona um novo registro ao histórico.

        Args:
            nome_musica (str): O nome da música.
            artista (str): O nome do artista.
            data_hora (datetime, optional): A data e hora da reprodução. Se None, usa o tempo atual.
        """
        registro = {
            'musica': nome_musica,
            'artista': artista,
            'data_hora': data_hora if data_hora else datetime.now()
        }
        self.registros.append(registro)
        self._salvar_historico()
        self.logger.info(f"Registro adicionado ao histórico: {nome_musica} - {artista}")

    def limpar_historico(self):
        """Limpa todos os registros do histórico."""
        self.registros = []
        self._salvar_historico()
        self.logger.info("Histórico de reprodução limpo.")

    def obter_historico(self, limite: int = None) -> list[dict]:
        """
        Retorna os registros do histórico, opcionalmente limitados aos mais recentes.

        Args:
            limite (int, optional): O número máximo de registros a serem retornados.

        Returns:
            list[dict]: A lista de registros do histórico.
        """
        if limite and len(self.registros) > limite:
            return self.registros[-limite:]
        return self.registros

    def _salvar_historico(self):
        """Salva os registros do histórico em um arquivo pickle."""
        try:
            with open(CAMINHO_HISTORICO, 'wb') as arquivo:
                pickle.dump(self.registros, arquivo)
        except Exception as e:
            self.logger.error(f"Erro ao salvar histórico: {e}")

    def _carregar_historico(self) -> list[dict]:
        """
        Carrega os registros do histórico de um arquivo pickle.

        Returns:
            list[dict]: A lista de registros carregados ou uma lista vazia em caso de erro.
        """
        try:
            if Path(CAMINHO_HISTORICO).exists():
                with open(CAMINHO_HISTORICO, 'rb') as arquivo:
                    return pickle.load(arquivo)
            return []
        except Exception as e:
            self.logger.error(f"Erro ao carregar histórico: {e}")
            return []