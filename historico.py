import pickle
from pathlib import Path
from datetime import datetime
from logger import Logger

CAMINHO_HISTORICO = "historico.pkl"

class HistoricoReproducao:
    def __init__(self):
        self.logger = Logger()
        self.registros = self.carregar_historico()

    def adicionar_registro(self, nome_musica: str, artista: str, data_hora=None):
        registro = {
            'musica': nome_musica,
            'artista': artista,
            'data_hora': data_hora if data_hora else datetime.now()
        }
        self.registros.append(registro)
        self.salvar_historico()
        self.logger.info(f"Registro adicionado ao histórico: {nome_musica} - {artista}")
    
    def limpar_historico(self):
        self.registros = []
        self.salvar_historico()
        self.logger.info("Histórico de reprodução limpo")

    def obter_historico(self, limite=None):
        if limite and len(self.registros) > limite:
            return self.registros[-limite:]
        return self.registros
    
    def salvar_historico(self):
        try:
            with open(CAMINHO_HISTORICO, 'wb') as arquivo:
                pickle.dump(self.registros, arquivo)
        except Exception as e:
            self.logger.error("Erro ao salvar histórico: {e}")
    
    def carregar_historico(self):
        try:
            if Path(CAMINHO_HISTORICO).exists():
                with open(CAMINHO_HISTORICO, 'rb') as arquivo:
                    return pickle.load(arquivo)
            return []
        except Exception as e:
            self.logger.error(f"Erro ao carregar histórico: {e}")
            return []