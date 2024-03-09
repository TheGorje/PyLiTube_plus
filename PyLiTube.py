import os
import tempfile
from pathlib import Path
import json
import io
from time import sleep
import urllib
import requests
from pytube import Playlist, YouTube
import PySimpleGUI as sg
from PIL import Image
import ffmpeg

# define a paleta de cores
text_color = '#e3eae8'
background_color = '#121212'
alternative_background = "#000000"
primary_color = '#5e5e5e'
secondary_color = '#383838'
accent_color = '#3c7aae'
font_F = 'Helvetica'

# modifica um tema existente
sg.LOOK_AND_FEEL_TABLE['MyTheme'] = {'BACKGROUND': background_color,
                                        'TEXT': text_color,
                                        'INPUT': primary_color,
                                        'TEXT_INPUT': text_color,
                                        'SCROLL': accent_color,
                                        'BUTTON': (text_color, secondary_color),
                                        'PROGRESS': sg.DEFAULT_PROGRESS_BAR_COLOR,
                                        'BORDER': 1,'SLIDER_DEPTH': 0, 'PROGRESS_DEPTH':0,}
# define o novo tema customizado
sg.theme('MyTheme')


# armazena os vídeos baixados (titulo)
downloaded_videos = []

# armazena o estado de cada vídeo (estado)
video_states = {}

# carregar variaveis de configurações do arquivo JSON
with open('settings.json', 'r') as f:
    settings = json.load(f)

# salvar configurações de settings
def save_settings():
    with open('settings.json', 'w') as f:
        json.dump(settings, f)

# converte numeros inteiros para um formato de tempo H:M
def format_time(numero):
    horas = numero // 100
    minutos = numero % 100
    return f"{horas}:{minutos:02d}"
# converte numeros inteiros para numeros com pontuação
def format_views(numero):
    return f"{numero:,}".replace(",", ".")
# formatar o titulo do video para que o explorer reconheça
def format_title(filename):
    invalid_chars = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
    for char in invalid_chars:
        filename = filename.replace(char, '')
    return filename

def start_download(video, path, tipo):
    print('start_download')
    # escolhido Audio
    if tipo == 'audio':
        out_path = video.streams.filter(only_audio=True).first()
        extension = '.mp3'
        title = format_title(f'{out_path.title}{extension}')
    # escolhido Video
    elif tipo == 'video':
        out_path = video.streams.filter(progressive=True, file_extension='mp4').get_highest_resolution()
        extension = '.mp4'
        title = format_title(f'{out_path.title}{extension}')
    else:
        return None, 'Invalid type', None

    print(title)
    new_name = os.path.join(path, title)
    new_name = os.path.splitext(new_name)[0] + extension

    # verifica se o arquivo já existe
    if os.path.exists(new_name):
        print('File already exists:', new_name)
        status = 'Exists'
    else:
        # inicia o download do vídeo
        path_download = out_path.download(output_path=path)
        os.rename(path_download, new_name)
        status = 'Downloaded'
    return new_name, status, title


def convert_mp3(new_name):
    # cria um arquivo temporário com a extensão .mp3
    print('começou convert mp3')
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")

    # ffmpeg-python para converter o arquivo
    input_stream = ffmpeg.input(new_name)
    adjusted_audio = input_stream.filter('volume', '-5dB')
    output_stream = ffmpeg.output(adjusted_audio, temp_file.name, format='mp3')
    ffmpeg.run(output_stream, overwrite_output=True)

    # fecha o arquivo temporário
    temp_file.close()

    # substitui o arquivo original pelo arquivo temporário
    os.remove(new_name)
    os.rename(temp_file.name, new_name)
    print('--------------convert_mp3----------')


def downloader(link, path, downloaded_videos, video_states, window, tipo):
    # verifica se o diretório de saida existe, caso contrário, crie
    Path(path).mkdir(parents=True, exist_ok=True)

    # verifica se o link é de uma playlist ou de um vídeo único
    try:
        if 'com/playlist' in link:
            yt_playlist = Playlist(link)
            videos = yt_playlist.videos
            print(videos) # importante para o TRY EXECPT
        else:
            videos = [YouTube(link)]
            print(videos) # importante para o TRY EXECPT
    except urllib.error.HTTPError as erro:
        if erro.code == 404:
            # atualiza o valor do state, indicando o erro
            window['-STATE-'].update(erro, visible=True, text_color="red")
        else:
            # atualiza o valor do state, indicando o erro
            window['-STATE-'].update(erro, visible=True, text_color="red")
        return
    except Exception as e:
        # atualiza o valor do state, indicando o erro generico
        window['-STATE-'].update(e, visible=True, text_color="red")
        return

    # cria um novo layout para o popup
    layout_popup = [
        # titulo
        [sg.Text('', key='-TITLE-', font=(font_F,18))],
                        # imagem do da thumb do video
        [sg.Column([[sg.Image(data='', key='-IMAGE-', visible=False)]], vertical_alignment='top'),
            sg.Column([
                [sg.Text('', key='-AUTHOR-', font=(font_F, 12), text_color=("white"), visible=False)], # canal
                [sg.Text('', key='-DURATION-', font=(font_F, 12), text_color=("white"), visible=False)], # duração
                [sg.Text('', key='-VIEWS-', font=(font_F, 12), text_color=("white"), visible=False)], # visualizações
                [sg.Text('', key='-SIZE-MB-', font=(font_F, 12), text_color=("white"), visible=False)], # visualizações
            ])],
        # texto com o nome da playlist (se houver)
        [sg.Column([[sg.Text('', key='-PLAYLIST.NAME-', font=(font_F, 14), text_color=("white"), visible=False)]], justification='center')],
        # barra de progresso se for playlist
        [sg.ProgressBar(max_value=len(videos), orientation='h', size=(40, 20), key='-PROGRESS-', visible=False)],
        # número indicando o progresso da playlist (1/x)
        [sg.Text('', key='-PROGRESS.TEXT-', font=(font_F, 12), text_color=("white"), visible=False)],
        [sg.Button('Cancel', key='-CANCEL-')]
        ]
    window_popup = sg.Window('Download Progress',
                            layout_popup, finalize=True,
                            element_justification='center',
                            no_titlebar=True,
                            background_color=alternative_background
                            )
    window_popup.move_to_center()

    i = 0 # contador de video
    for video in videos:
        try:
            # sempre mostrar titulo
            window_popup['-TITLE-'].update( video.title, visible=True )
            # ocultar thumb [x]
            if settings['-OP1-'] is True:
                window_popup['-IMAGE-'].update( visible=False)
            else:
                # baixa imagem
                r = requests.get(video.thumbnail_url)
                image = Image.open(io.BytesIO(r.content))
                # redimensione a imagem
                baseheight = 100
                hpercent = (baseheight / float(image.size[1]))
                wsize = int((float(image.size[0]) * float(hpercent)))
                image = image.resize((wsize, baseheight), Image.ANTIALIAS)

                # salva a imagem em um objeto BytesIO
                bio = io.BytesIO()
                image.save(bio, format='PNG')

                # atualiza a interface
                window_popup['-IMAGE-'].update( data=bio.getvalue(),visible=True)
            # Mostra informações extras
            if settings['-OP2-'] is True:
                window_popup['-AUTHOR-'].update( video.author, visible=True)
                window_popup['-DURATION-'].update( f'Duration: {format_time(video.length)}', visible=True)
                window_popup['-VIEWS-'].update( f'Views: {format_views(video.views)}', visible=True)
                window_popup['-SIZE-MB-'].update( '' , visible=True)
            else:
                window_popup['-AUTHOR-'].update(visible=False)
                window_popup['-DURATION-'].update(visible=False)
                window_popup['-VIEWS-'].update(visible=False)
                window_popup['-SIZE-MB-'].update(visible=False)

            # recarrega a interface
            window_popup.Refresh()
           

            if len(videos) >=2: # playlist mode
                window_popup['-PLAYLIST.NAME-'].update( yt_playlist.title, visible=True )
                window_popup['-PROGRESS-'].update(i, visible=True)
                window_popup['-PROGRESS.TEXT-'].update(f'{i}/{len(videos)}', visible=True)

            # verifica se a janela do popup foi fechada ou click no "cancel"
            event_popup, values_popup = window_popup.read(timeout=5)
            if window_popup.was_closed() or event_popup == '-CANCEL-':
                break

            # recarregar a interface
            window_popup.Refresh()

            # baixar o video
            new_name, status, title = start_download(video, path, tipo)
            # converte em MP3
            if status == 'Downloaded' and tipo == 'audio':
                convert_mp3(new_name)

            # pegar o tamanho do arquivo após converter
            filesize_bytes = os.path.getsize( new_name ) / (1024 * 1024)
            # atualiza a interface
            if settings['-OP2-'] is True:
                window_popup['-SIZE-MB-'].update( f'{round(filesize_bytes, 2)} Mb')
            # recarrega a interface
            window_popup.Refresh()

            print('---------------------------')
            print(f"Completed ({i}) : {video.title}")

            # adiciona o titulo ao array de videos
            downloaded_videos.append( title )

            # atualiza o estado do vídeo
            video_states[ title ] = status

            # atualiza a lista na interface
            window['-VIDEOLIST-'].update([f'{v} ({video_states[v]})' for v in downloaded_videos])
            window.Refresh()

            # se o video for o último da lista
            if i == len(videos):
                sleep(1) # espera um pouco(1s) antes de fechar
                # atualiza o valor do state, indicando que o download terminou
                window['-STATE-'].update("Download Completed!", visible=True, text_color="green")
            i += 1
        except Exception as erro:
            print("Error:", erro)
            # atualiza o valor do state, indicando o erro
            sg.popup_error(erro)
            window['-STATE-'].update(erro, visible=True, text_color="red")
            window_popup.close()
            return
    window_popup.close()
    print("\nFinished.")



# layout da interface pysimplegui
layout = [
    # texto / (input para o link) / text para espaçamento / btn de options
    [sg.Text('Playlist or Video link: ', font=(font_F,12)), sg.InputText(key='-LINK-'),sg.Text('', size=(10, 1)),sg.Button('Settings', key="-SETTINGS-")],
    # botão para selecionar a pasta de saída
    [sg.Button('Select Output Folder', font=(font_F,12))],
    # texto indicando a saída do(s) arquivo(s)
    [sg.Text('', key='-FOLDER-', font=(font_F,12))],

    [sg.Text('', key='-EMPTY-', size=(2,1))], # pular um espaço

    # botao para começar o download
    [sg.Button('VIDEO', font=(font_F,12)), sg.Button('AUDIO', font=(font_F,12))],

    [sg.Column([[sg.Text('', key='-STATE-', font=(font_F,14), text_color=("green"), visible=False)]], justification='center')], # text que indica se está baixando ou não
    [sg.Listbox(values=[], # lista onde é mostrado cada video e seu estado
                size=(70, 10),
                font=(font_F,12),
                key='-VIDEOLIST-',
                enable_events=True)],
]

# layout de configurações da janela de configuração
def get_config_layout():
    return [
        [sg.Text('Download', font=(font_F, 12))],
        [sg.Checkbox('Hide Thumbnail (FAST)', key='-OP1-', default=settings['-OP1-'])],
        [sg.Checkbox('Show extra video information', key='-OP2-', default=settings['-OP2-'])],
        [sg.Checkbox('Open folder after download completion', key='-OP3-', default=settings['-OP3-'])],

        [sg.Canvas(size=(250, 1), background_color=primary_color, key='-CANVAS-')],

        [sg.Text('On item clicked in the list', font=(font_F, 12))],
        [sg.Checkbox('Open the output folder', key='-OP4-', default=settings['-OP4-'])],
        [sg.Checkbox('Open the file', key='-OP5-', default=settings['-OP5-'])],

        [sg.Button('Save'), sg.Button('Cancel'), sg.Button('Default')]
    ]

window = sg.Window('PyLiTube+',
                    layout,
                    element_justification='center',
                    icon="./src/PyLiTube_small.ico"
                )

while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED:
        break
    # interface de configurações
    elif event == '-SETTINGS-':
        window_config = sg.Window('Settings', get_config_layout(), finalize=True)
        while True:
            event_config, values_config = window_config.read()

            if event_config in (sg.WINDOW_CLOSED, 'Cancel') or window_config.was_closed():
                break
            elif event_config == 'Default':
                settings_default = ['-OP2-','-OP3-','-OP4-'] # default settings
                for option in settings:
                    if option in settings_default:
                        settings[option]= True
                    else:
                        settings[option] = False
                # salvar as configurações em um arquivo JSON(settings)
                save_settings()
                break
            elif event_config == 'Save':
                for option in values_config:
                    if option in settings:
                        settings[option] = values_config[option]
                # salvar as configurações em um arquivo JSON(settings)
                save_settings()
                print(settings)
                break
        window_config.close()

    if event == 'Select Output Folder':
        folder = sg.popup_get_folder('', no_window=True)
        if folder:
            window['-FOLDER-'].update(f"{folder}")

    elif event == '-VIDEOLIST-':
        if values['-VIDEOLIST-']:
            selected_item = values['-VIDEOLIST-'][0]

            # remove a parte de status: "(status)" do item selecionado
            selected_item = selected_item.rsplit(' ', 1)[0]

            # abrir pasta de saída?
            if settings['-OP4-'] is True:
                os.startfile(f"{folder}") # abre a pasta do arquivo

            # abrir aqruivo?
            if settings['-OP5-'] is True:
                audio_mp3 = f"{folder}/{format_title(selected_item)}"
                print(audio_mp3)
                if os.path.exists(audio_mp3): # verifica se o caminho é válido
                    os.startfile(audio_mp3) # abre o arquivo
                else:
                    sg.popup_error('Error To Open MP3')


    elif event == 'AUDIO':
        link = values['-LINK-'] # link da playlist ou video
        folder_text = window['-FOLDER-'].get() # output folder que foi escolhido

        # verifica se tanto o link quanto a pasta não estão vazios
        if link.strip() == '' or folder_text.strip() == '':
            sg.popup_error('fill in both fields')
        else:
            # reseta as variaveis que armazenam o nome do video e o status
            downloaded_videos = []
            video_states = {}

            # reseta o estado (state)
            window['-STATE-'].update('', visible=False)

            # inicia o download
            downloader(link, folder_text, downloaded_videos, video_states, window, 'audio')

            # abre o caminho onde selecionado, output (folder_text)
            if settings['-OP3-'] is True:
                os.startfile(f"{folder_text}")
    elif event == 'VIDEO':
        link = values['-LINK-'] # link da playlist ou video
        folder_text = window['-FOLDER-'].get() # output folder que foi escolhido

        # verifica se tanto o link quanto a pasta não estão vazios
        if link.strip() == '' or folder_text.strip() == '':
            sg.popup_error('fill in both fields')
        else:
            # reseta as variaveis que armazenam o nome do video e o status
            downloaded_videos = []
            video_states = {}

            # inicia o download
            downloader(link, folder_text, downloaded_videos, video_states, window, 'video')

            # abre o caminho onde selecionado, output (folder_text)
            if settings['-OP3-'] is True:
                os.startfile(f"{folder_text}")
window.close()