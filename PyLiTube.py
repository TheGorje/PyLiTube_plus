import os
import ffmpeg
from pathlib import Path
from pytube import Playlist, YouTube
import PySimpleGUI as sg

# armazena os vídeos baixados (titulo)
downloaded_videos = []

# armazena o estado de cada vídeo (estado)
video_states = {}


def start_download(video, path):
    # inicia o download do vídeo
    out_path = video.streams.filter(
        only_audio=True).first().download(output_path=path)
    new_name = os.path.splitext(out_path)[0] + '.mp3'
    return out_path, new_name

def check_progress(out_path, new_name):
    # verifica se o arquivo já existe
    if os.path.exists(new_name):
        print('File already exists:', new_name)
        # Remova o arquivo original baixado, se já existir
        os.remove(out_path)
        return 'Exists'

    # ffmpeg-python para converter o arquivo
    input_stream = ffmpeg.input(out_path)
    output_stream = ffmpeg.output(input_stream, new_name)
    ffmpeg.run(output_stream, capture_stdout=True, capture_stderr=True)

    # remove o arquivo original baixado
    os.remove(out_path)
    return 'Downloaded'

def downloader(link, path, downloaded_videos, video_states, window):
    # verifica se o diretório de saida existe, caso contrário, crie
    Path(path).mkdir(parents=True, exist_ok=True)

    # verifica se o link é de uma playlist ou de um vídeo único
    if 'playlist' in link:
        yt_playlist = Playlist(link)
        videos = yt_playlist.videos
    else:
        videos = [YouTube(link)]

    i = 1 # contador de video
    for video in videos:
        try:
            out_path, new_name = start_download(video, path)

            # verifica o progresso do download
            status = check_progress(out_path, new_name)

            print('---------------------------')
            print(f"Completed ({i}) : {video.title}")

            # Adiciona o titulo ao array de videos
            downloaded_videos.append(video.title)

            # Atualiza o estado do vídeo
            video_states[video.title] = status

            # atualiza a lista na interface
            window['-VIDEOLIST-'].update([f'{v} ({video_states[v]})' for v in downloaded_videos])
            window.Refresh()

            i += 1
        except Exception as e:
            print("Error:", e)
            print('-.-.--.--.--.--.--.--.--.--.--.-')

            # Se ocorrer um erro, atualiza o estado do video para 'Erro'
            video_states[video.title] = 'Erro'
    print("\nFinished.")

sg.theme('DarkAmber')


# menu para a lista de arquivos baixados, executar em comandos (mouse1 e mouse2)

# layout da interface pysimplegui
layout = [
    [sg.Text('Playlist or Video link: ', font=(24)), sg.InputText(key='-LINK-')], # texto a esquerda, inpu del ink a direita
    [sg.Button('Select Output Folder', font=(24))], # botão para selecionar a pasta de saída
    [sg.Text('', key='-FOLDER-', font=(24))], # texto indicando a saída do(s) arquivo(s)
    [sg.Text('', key='-STATE-', font=(32), text_color=("white"))], # text que indica se está baixando ou não
    [sg.Listbox(values=[], # lista onde é mostrado cada item e seu estado
                size=(70, 10),
                font=(14),
                key='-VIDEOLIST-',
                enable_events=True)],
    [sg.Button('Ok'), sg.Button('Quit')]
]

window = sg.Window('PyLiTube MP3 Download', layout, element_justification='center')

while True:
    event, values = window.read()
    
    if event in (sg.WIN_CLOSED, 'Quit'):
        break

    if event == 'Select Output Folder':
        folder = sg.popup_get_folder('', no_window=True)
        if folder:
            window['-FOLDER-'].update(f"{folder}")

    elif event == '-VIDEOLIST-':
        # verifica se o item selecionado é válido
        if values['-VIDEOLIST-']:
            selected_item = values['-VIDEOLIST-'][0]

            # remove a parte de status: "(status)" do item selecionado
            selected_item = selected_item.rsplit(' ', 1)[0] #

            print(f"{folder}/{selected_item}.mp3")
            os.startfile(f"{folder}") # abre a pasta do arquivo
            os.startfile(f"{folder}/{selected_item}.mp3") # abre o arquivo


    elif event == 'Ok':
        link = values['-LINK-'] # link da playlist ou video
        folder_text = window['-FOLDER-'].get() # output que foi escolhido

        # verifica se tanto o link quanto a pasta não estão vazios
        if link.strip() == '' or folder_text.strip() == '':
            sg.popup_error('fill in both fields')
        else:
            # atualiza o STATE para "Baixando..."
            window['-STATE-'].update("Downloading...")
            window.Refresh()
            # reseta as variaveis que armazenam o nome do video e o status
            downloaded_videos = []
            video_states = {}
            # inicia o download
            downloader(link, folder_text, downloaded_videos, video_states, window)
            # atualiza o valor do state, indicando que o download terminou
            window['-STATE-'].update("Download Completed!")
            # abre o caminho onde selecionado, output (folder_text)
            os.startfile(f"{folder_text}")

window.close()
