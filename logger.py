from threading import Lock
import logging
import os
from typing import Dict, Optional

class SingletonMeta(type):
    _instancias: Dict[type, object] = {}
    _lock: Lock = Lock()

    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instancias:
                instancia = super().__call__(*args, **kwargs)
                cls._instancias[cls] = instancia
        return cls._instancias[cls]
    
class Logger(metaclass=SingletonMeta):
    def __init__(self, nome: str = "Logger", arquivo_log: Optional[str] = None):
        self._logger = logging.getLogger(nome)
        self._logger.setLevel(logging.DEBUG)
        
        for handler in self._logger.handlers[:]:
            self._logger.removeHandler(handler)

        formatador = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(threadName)s - %(message)s'
        )

        # Handler para console
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatador)
        self._logger.addHandler(console_handler)

        if arquivo_log:
            if os.path.exists(arquivo_log):
                with open(arquivo_log, 'w'):
                    pass
            
            file_handler = logging.FileHandler(arquivo_log)
            file_handler.setFormatter(formatador)
            self._logger.addHandler(file_handler)
        
        self._log_lock = Lock()

    def log(self, nivel: int, mensagem: str, *args, **kwargs):
        with self._log_lock:
            self._logger.log(nivel, mensagem, *args, **kwargs)
        
    def debug(self, mensagem: str, *args, **kwargs):
        with self._log_lock:
            self._logger.debug(mensagem, *args, **kwargs)

    def info(self, mensagem: str, *args, **kwargs):
        with self._log_lock:
            self._logger.info(mensagem, *args, **kwargs)

    def warning(self, mensagem: str, *args, **kwargs):
        with self._log_lock:
            self._logger.warning(mensagem, *args, **kwargs)
        
    def error(self, mensagem: str, *args, **kwargs):
        with self._log_lock:
            self._logger.error(mensagem, *args, **kwargs)