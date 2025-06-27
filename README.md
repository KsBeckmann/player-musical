# 🎵 Player Musical

## Sobre o Projeto
O Projeto SoundWave é um protótipo de um player de músicas funcional desenvolvido em Python. Este player foi construído como parte do Estudo Dirigido da disciplina de Programação Avançada, aplicando conceitos como Orientação a Objetos, manipulação de arquivos, serialização de dados e concorrência para criar uma aplicação robusta e modular.

## ✨ Funcionalidades
### Gerenciamento de Biblioteca:

Adicione músicas, álbuns e artistas à sua biblioteca pessoal.

Organize as músicas de forma hierárquica (Artista > Álbum > Música).

Busque facilmente por artistas, álbuns ou músicas.

Remova músicas, álbuns ou artistas da biblioteca.

### Reprodução de Áudio:

Utilize o player para tocar, parar e controlar o volume das suas músicas favoritas (.mp3, .wav, etc.).

A reprodução de playlists é feita em uma thread separada para não bloquear a interface principal.

### Playlists Personalizadas:

Crie, renomeie e remova playlists.

Adicione ou remova músicas de qualquer playlist.

Ordene as músicas dentro de uma playlist por nome ou mova-as para a posição desejada.

### Persistência de Dados:

Toda a sua biblioteca de músicas e playlists são salvas em disco e carregadas automaticamente ao iniciar o programa, usando serialização com pickle.

As configurações do usuário, como o nível de volume, também são salvas.

O histórico das últimas músicas tocadas é mantido e pode ser consultado ou limpo.

### Logging:

As principais ações do sistema são registradas em um arquivo de log (reprodutor.log) para facilitar a depuração.

## 📂 Estrutura do Projeto
O código é organizado em módulos, cada um com uma responsabilidade bem definida, seguindo as boas práticas de modularização.

### main.py

Ponto de entrada da aplicação. Instancia e inicia o menu principal.

### menu.py

Contém toda a lógica da interface do usuário via linha de comando (CLI), gerenciando a navegação e a interação com o usuário.

### classes.py

Define as classes principais do modelo de dados: Musica, Album, Artista e Reprodutor.

### playlist.py

Contém a classe Playlist, responsável por gerenciar as coleções de músicas.

### historico.py

Implementa a classe HistoricoReproducao para salvar e carregar o histórico de músicas tocadas.

### utils.py

Módulo com funções auxiliares para salvar e carregar dados (pickle), copiar arquivos de música, limpar a tela, etc.

### logger.py

Implementa um logger com o padrão de projeto Singleton para registrar eventos da aplicação de forma centralizada e thread-safe.

### tests/

Diretório que contém os testes unitários para garantir a qualidade e o funcionamento correto dos diferentes módulos.


## 🧪 Como Executar os Testes
Para garantir que todos os componentes do sistema estão funcionando como esperado, você pode rodar a suíte de testes automatizados.

No terminal, a partir da raiz do projeto (player-musical), execute o seguinte comando:

python -m unittest discover tests

O unittest irá descobrir e executar todos os testes dentro da pasta tests, exibindo os resultados no console.

## 🚀 Como Executar o Programa
Para executar o SoundWave em sua máquina, siga os passos abaixo.

Pré-requisitos
Python 3.9 ou superior

1. Clone o Repositório
Primeiro, clone ou faça o download dos arquivos do projeto para o seu computador.

2. Navegue até a Pasta do Projeto
Abra um terminal e navegue até o diretório onde você salvou os arquivos.

```
cd caminho/para/player-musical
```

3. Instale as Dependências
Instale a única dependência necessária (pygame) executando o seguinte comando:

```
pip install -r requirements.txt
```

4. Execute a Aplicação
Com as dependências instaladas, inicie o programa:

```
python main.py
```

Pronto! O menu principal do SoundWave aparecerá no seu terminal.