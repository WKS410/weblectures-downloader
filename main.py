import os
import requests
import subprocess
from os import pathsep, environ, remove, makedirs

# Define algunas constantes
ARIA2C_EXE = 'aria2c.exe'
MKVMERGE_EXE = 'mkvmerge.exe'
TEMP_VIDEO = 'temp_video.mp4'
TEMP_AUDIO = 'temp_audio.aac'

# Obtiene la ruta del directorio actual del script
script_dir = os.path.dirname(os.path.realpath(__file__))

# Construye las rutas completas de los ejecutables de Aria2c y Mkvmerge
aria2c_path = os.path.join(script_dir, ARIA2C_EXE)
mkvmerge_path = os.path.join(script_dir, MKVMERGE_EXE)

# Imprime información sobre la URL de descarga y los tokens de autenticación
print('\nTest URL: https://weblectures.ru.nl/api/v2/medias/modes/?oid=v126417e8cae4unljb9h&html5=webm_ogg_ogv_oga_mp4_m4a_mp3_m3u8&yt=yt&embed=embed&_=1679427203039')

with open("links.txt", encoding="UTF-8") as f:
    links = f.read().splitlines()
    for index, link in enumerate(links[1:]):
        print(f"downloading {link}")
        # Get course name from first line of links.txt
        course_name = links[0]
        # Output file name includes course name and lecture number
        output_file = f"{course_name} - L{index+1}.mp4"
        csrftoken = input('\ncsrftoken: ')
        mssessionid = input('\nmssessionid: ')

        # Define los encabezados para la solicitud de descarga
        headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7',
            'Connection': 'keep-alive',
            'Cookie': f'csrftoken={csrftoken}; mssessionid={mssessionid}',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
        }

        try:
            # Realiza la solicitud de descarga
            response = requests.get(link, headers=headers).json()

            # Extrae la URL del video y la URL del audio del JSON de respuesta
            track_video = response['1080p']['resource']['url']
            track_audio = response['audio']['tracks'][0]['url']

            # Descarga el video y el audio utilizando Aria2c
            subprocess.run([aria2c_path, track_video, '-o', TEMP_VIDEO])
            subprocess.run([aria2c_path, track_audio, '-o', TEMP_AUDIO])

            # Fusiona el video y el audio utilizando Mkvmerge
            subprocess.run([mkvmerge_path, '--output', f'{output_file}.mkv', '--language', '0:und', TEMP_VIDEO, '--language', '0:und', TEMP_AUDIO])

    # Borra los archivos temporales de video y audio
    remove(TEMP_VIDEO)
    remove(TEMP_AUDIO)

    print('\n¡La descarga y fusión del video y el audio se completaron correctamente!')
