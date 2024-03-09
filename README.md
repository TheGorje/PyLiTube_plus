# PyLiTube MP3
![banner](.github/PyLitube_banner.png)
O **PyLiTube MP3** é um aplicativo em Python que permite aos usuários baixar videos individuais ou playlists do YouTube e tambpem convertê-las para o formato MP3.

Utilizando a biblioteca **PySimpleGUI**, o aplicativo oferece uma interface amigável onde os usuários podem facilmente selecionar os vídeos desejados e escolher um diretório de saída para suas músicas favoritas.

## Recursos

- **Download de Playlists ou Vídeos Individuais:** Insira links de playlists ou vídeos individuais do YouTube.
- **Conversão para MP3:** Utiliza o FFmpeg para converter os vídeos baixados para o formato MP3.
- **Seleção de Diretório de Saída:** Escolha o local onde deseja salvar os arquivos MP3/MP4.
- **Interface Gráfica Amigável:** A interface intuitiva permite que qualquer pessoa use a ferramenta sem dificuldades.

## Como Usar

1. **Instalação:**
   - Certifique-se de ter o Python 3.x instalado no seu sistema.
   - Execute o seguinte comando para instalar as bibliotecas necessárias: `pip install requests==2.31.0 pytube==15.0.0 PySimpleGUI==4.60.4 Pillow==9.2.0 ffmpeg-python==0.2.0`
   - Baixe (ou copie FFmpeg) e instale o FFmpeg. Certifique-se de adicionar o FFmpeg ao PATH do sistema.

2. **Instalação FFmpeg:**

    <details>
    <summary>Windows</summary>

    - **Mover o arquivo FFmpeg:** Mova a pasta [FFmpeg](./FFmpeg) para a raiz do seu sistema, geralmente o Disco Local (c:).
    - **Adicionar ao Caminho do Sistema:**
        - Abra o CMD como administrador “Prompt de Comando (Admin)”.
        - Execute o seguinte comando para adicionar o caminho do FFmpeg ao sistema:
        
        ```cmd
        setx /m PATH "C:\FFmpeg\bin;%PATH%"
        ```
    </details>

    <details>
    <summary>Linux</summary>

    - **Atualizar o sistema:** Abra o terminal e atualize o sistema com o seguinte comando:
    
        ```bash
        sudo apt-get update
        ```
    - **Instalar o FFmpeg:** Execute o seguinte comando para instalar o FFmpeg:
    
        ```bash
        sudo apt-get install ffmpeg
        ```
    - **Verificar a instalação:** Você pode verificar se o FFmpeg foi instalado corretamente com o seguinte comando:
    
        ```bash
        ffmpeg -version
        ```
    </details>

3. **Execução:**
    - Execute o arquivo `PyLiTube.py`.
    - Cole o link da **playlist** ou vídeo **individual** do YouTube na caixa de entrada.
    - Selecione um diretório de saída **"Select Output Folder"**.
    - Clique no botão **“VIDEO”** para iniciar o processo de download do video MP4.
    - Clique no botão **“AUDIO”** para iniciar o processo de download do audio mp3.
4. **Configuração (Settings)**
    - **Download**
        - **“Hide Thumbnail (FAST)”**: Esconde a imagem da thumb, assim não carregando a imagem e evitando esse processo.
        - **“Show extra video information”**: Ao baixar mostrará informações do video, como Canal, Duração, visualização e tamanho do arquivo final.
        - **“Open folder after download completion”**: Abre a pasta de saída, após o termino do download.
    - **On item clicked in the list**
        - **“Open the output folder”**: Ao clicar no item baixado, irá abrir a pasta de saída do arquivo.
        - **“Open the file”**: Ao clicar no item selecionado, irá abrir o arquivo, MP4 ou MP3.
    - **Botões**:
        - **“Save”**: Salva as configurações selecionadas e fecha a aba.
        - **“Cancel”**: Cancela qualquer alteração feita nas configurações.
        - **“Default”**: Reseta para as configurações originais.

## Observações

- Certifique-se de ter o FFmpeg instalado e configurado corretamente no seu sistema. Ele é necessário para a conversão (MP3).
- Os arquivos MP3 e MP4 serão salvos no diretório de saída especificado.
- Arquivos com o mesmo nome retornarão “Exists”.
- Arquivos com erros retornarão “Erro”.
- Arquivos baixados com sucesso retornarão “Downloaded”.
- Certifique-se de ter **playlist** no link `youtube.com/playlist` para baixar a playlist completa.
## Requisitos

- Python 3.x
- Bibliotecas: PySimpleGUI(v4.60.4), pytube(v15.0.0), request(2.31.0), Pillow(9.2.0) (verifique os [RE](./requirements.txt)).

# Licença
Este projeto é Licenciado por [IMT](./LICENSE).
