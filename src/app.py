"""
1. Encontrar arquivos de extensão de vídeo recursivamente
2. Salvar endereços desses arquivos em um array
3. Passar pelo array fazendo as verificações
4. Gurdar as informações (e fazer um relatório?)

A: Verificações:
-> Resolução [ deve ser no mínimo HD (1280x720) e proporção 16:9 (~1,7) e até 7 minutos (420)
"""

import tkinter as tk
from tkinter import filedialog
from utils import *

"""
Seleciona a pasta onde serão feitas as verificações
"""


def select_root_folder():
    root = tk.Tk()
    root.withdraw()
    return filedialog.askdirectory()


if __name__ == '__main__':
    caminhos_videos = []
    limite_de_tamanho_em_MB = 500
    pasta_raiz = select_root_folder()
    print("\n-----------------------------------------------------------------------------\n")
    print(f"Varrendo a pasta {pasta_raiz}")
    print(f"Buscando arquivos maiores que o limite de {limite_de_tamanho_em_MB} MB...")
    verify_file_size(pasta_raiz, limite_de_tamanho_em_MB)
    print("\n-----------------------------------------------------------------------------\n")
    print("Buscando pastas vazias...\n-----------------------------------------------------------------------------\n")
    encontra_pastas_vazias(pasta_raiz)
    print("\n-----------------------------------------------------------------------------\n")
    lista_videos = encontrar_videos_recursivamente_nas_subpastas(pasta_raiz)
    print(lista_videos)


    def retorna_tempo_medio_vetor_videos(vetor_videos):
        tempo_total = 0
        qtd_videos = 0
        for video in vetor_videos:
            clip = VideoFileClip(video)
            tempo_total += clip.duration
            qtd_videos += 1
            print()


    retorna_tempo_medio_vetor_videos(lista_videos)

    '''
    for video in lista_videos:
        change_volume_in_section(video, 7, -1, 1.5, renomeia_editado(video))
    '''

    #@todo: avaliação extensão: deve ser mp4, mínimo de 1280x720 de resolução