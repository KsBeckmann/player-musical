import logging
import os
from threading import Lock
from typing import Dict, Optional

class SingletonMeta(type):
    """
    metaclasse e padrão de projeto singleton para garantir que uma classe tenha apenas uma instância

    atributos:
        _instancias (Dict[type, object]): dicionário para armazenar as instâncias das classes
        _lock (Lock): objeto de bloqueio para garantir a segurança em ambientes com múltiplas trheads
    """
    _instancias: Dict[type, object] = {}
    _lock: Lock = Lock()

    def __call__(cls, *args, **kwargs):
        """
        cria ou retorna a instância única da classe
        """
        with cls._lock:
            if cls not in cls._instancias:
                instancia = super().__call__(*args, **kwargs)
                cls._instancias[cls] = instancia
        return cls._instancias[cls]

class Logger(metaclass=SingletonMeta):
    """
    classe de Logger que utiliza o padrão Singleton para centralizar o logging

    atributos:
        _logger (logging.Logger): a instância do logger
        _log_lock (Lock): objeto de bloqueio para operações de log
    """
    def __init__(self, nome: str = "Logger", arquivo_log: Optional[str] = None):
        """
        inicializa o logger

        args:
            nome (str): nome do logger
            arquivo_log (Optional[str]): caminho do arquivo de log. Se None, o log não será salvo em arquivo
        """
        self._logger = logging.getLogger(nome)
        self._logger.setLevel(logging.DEBUG)

        # remove handlers existentes para evitar duplicação de logs
        for handler in self._logger.handlers[:]:
            self._logger.removeHandler(handler)

        formatador = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(threadName)s - %(message)s'
        )

        if arquivo_log:
            # limpa o arquivo de log ao iniciar
            if os.path.exists(arquivo_log):
                with open(arquivo_log, 'w'):
                    pass

            file_handler = logging.FileHandler(arquivo_log)
            file_handler.setFormatter(formatador)
            self._logger.addHandler(file_handler)
        else:
            # adiciona um NullHandler se nenhum arquivo de log for especificado
            self._logger.addHandler(logging.NullHandler())

        self._log_lock = Lock()

    def log(self, nivel: int, mensagem: str, *args, **kwargs):
        """
        registra uma mensagem de log com um nível específico

        args:
            nivel (int): o nível do log 
            mensagem (str): a mensagem a ser registrada
        """
        with self._log_lock:
            self._logger.log(nivel, mensagem, *args, **kwargs)

    def debug(self, mensagem: str, *args, **kwargs):
        """registra uma mensagem de debug"""
        with self._log_lock:
            self._logger.debug(mensagem, *args, **kwargs)

    def info(self, mensagem: str, *args, **kwargs):
        """registra uma mensagem de informação"""
        with self._log_lock:
            self._logger.info(mensagem, *args, **kwargs)

    def warning(self, mensagem: str, *args, **kwargs):
        """registra uma mensagem de aviso:"""
        with self._log_lock:
            self._logger.warning(mensagem, *args, **kwargs)

    def error(self, mensagem: str, *args, **kwargs):
        """registra uma mensagem de erro"""
        with self._log_lock:
            self._logger.error(mensagem, *args, **kwargs)