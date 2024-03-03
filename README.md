# PyLiTube MP3
![banner](.\src\PyLitube_banner.png)
O **PyLiTube MP3** é um aplicativo em Python que permite aos usuários baixar músicas individuais ou playlists do YouTube e convertê-las para o formato MP3.

Utilizando a biblioteca **PySimpleGUI**, o aplicativo oferece uma interface amigável onde os usuários podem facilmente selecionar os vídeos desejados e escolher um diretório de saída para suas músicas favoritas.

## Recursos

- **Download de Playlists ou Vídeos Individuais:** Insira links de playlists ou vídeos individuais do YouTube.
- **Conversão para MP3:** Utiliza o FFmpeg para converter os vídeos baixados para o formato MP3.
- **Seleção de Diretório de Saída:** Escolha o local onde deseja salvar os arquivos MP3.
- **Interface Gráfica Amigável:** A interface intuitiva permite que qualquer pessoa use a ferramenta sem dificuldades.

## Como Usar

1. **Instalação:**
   - Certifique-se de ter o Python 3.x instalado no seu sistema.
   - Execute o seguinte comando para instalar as bibliotecas necessárias: `pip install PySimpleGUI==4.60.4 pytube==15.0.0`
   - Baixe (ou copie FFmpeg) e instale o FFmpeg. Certifique-se de adicionar o FFmpeg ao PATH do sistema.

2. **Instalação FFmpeg:**

    <details>
    <summary>Windows</summary>

    1. **Mover o arquivo FFmpeg:** Mova a pasta [FFmpeg](./FFmpeg) para a raiz do seu sistema, geralmente o Disco Local (c:).
    2. **Adicionar ao Caminho do Sistema:**
        - Abra o CMD como administrador “Prompt de Comando (Admin)”.
        - Execute o seguinte comando para adicionar o caminho do FFmpeg ao sistema:
        
        ```cmd
        setx /m PATH "C:\FFmpeg\bin;%PATH%"
        ```
    </details>

    <details>
    <summary>Linux</summary>

    1. **Atualizar o sistema:** Abra o terminal e atualize o sistema com o seguinte comando:
    
        ```bash
        sudo apt-get update
        ```
    2. **Instalar o FFmpeg:** Execute o seguinte comando para instalar o FFmpeg:
    
        ```bash
        sudo apt-get install ffmpeg
        ```
    3. **Verificar a instalação:** Você pode verificar se o FFmpeg foi instalado corretamente com o seguinte comando:
    
        ```bash
        ffmpeg -version
        ```
    </details>

3. **Execução:**
    1. Execute o arquivo `PyLiTube.py`.
    2. Cole o link da **playlist** ou vídeo **individual** do YouTube na caixa de entrada.
    3. Selecione um diretório de saída **"Select Output Folder"**.
    4. Clique no botão **“Ok”** para iniciar o processo.

## Observações

- Certifique-se de ter o FFmpeg instalado e configurado corretamente no seu sistema. Ele é necessário para a conversão (MP3).
- Os arquivos MP3 serão salvos no diretório de saída especificado.
- Arquivos com o mesmo nome retornarão “Exists”.
- Arquivos com erros retornarão “Erro”.
- Arquivos baixados com sucesso retornarão “Downloaded”.

## Requisitos

- Python 3.x
- Bibliotecas: PySimpleGUI (v4.60.4), pytube (v15.0.0) (verifique os requirements.txt)

# Licença
Este projeto é Licenciado por [IMT](./LICENSE).