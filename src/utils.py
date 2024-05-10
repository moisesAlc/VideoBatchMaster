from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.editor import *
import os

""" Verifica se um arquivo tem as extensões suportadas"""
def arquivo_extensoes_suportadas(nome_arquivo):
    return nome_arquivo[-4:] in ['.mp4', '.avi', '.mkv']

""" Renomeia arquivo de x.y para x - editado.y"""
# @todo ao invés de mudar o nome do arquivo, salvar em uma pasta editadas com o mesmo nome...
def renomeia_editado(nome_video):
    extensao = nome_video[-4:]
    return  nome_video[:-4] + " - editado"  + extensao

""" De ZZ segundos para XX minuto(s) e YY segundo(s)"""
def formataMinutosSegundos(duracao_segundos):
    duration_in_seconds = int(duracao_segundos)
    minutos = duration_in_seconds // 60
    segundos = duration_in_seconds % 60
    return f"{minutos} minuto(s) e {segundos} segundo(s)"

""" Imprime informações sobre o vídeo"""
def get_video_info(filepath):
    # cria um objeto VideoFileClip
    clip = VideoFileClip(filepath)

    # video_info = object()
    # video_info.duration = clip.duration
    print("\tTaxa de Frames:", clip.fps)
    print("\tResolução:", clip.size)

    print("\tDuração:", formataMinutosSegundos(clip.duration))
    clip.close()
    return clip.duration

""" Encontra vídeos recursivamente na pasta e subpastas,
    Imprime na tela o tempo conjunto dos vídeos encontrados
    e Retorna um array com os caminhos para os vídeos"""
def encontrar_videos_recursivamente_nas_subpastas(path):
    tempo_total_videos = 0.0
    videos = []
    for dirpath, dirnames, filenames in os.walk(path):

        #print('Directory:', dirpath)
        for nome_arquivo in filenames:
            '''
            # print('  File:', os.path.join(dirpath, file))
            #if is_video(str(file)) and (not ("edit" in file or "EDIT - " in file)):
            '''
            if arquivo_extensoes_suportadas(str(nome_arquivo)) :
                videos.append(dirpath.replace('\\','/') + '/'+nome_arquivo)
                print(nome_arquivo, end=" ")
                tempo_total_videos += get_video_info(os.path.join(dirpath, nome_arquivo))
        '''for dirr in dirnames:
            for dirpath2ndlevel, dirnames2ndlevel, filenames2ndlevel in os.walk(dirr):
                for file2ndlevel in filenames2ndlevel:
                    # print('  File:', os.path.join(dirpath2ndlevel, file2ndlevel))
                    print('  File 2nd level:', file2ndlevel)
                for dirrr in dirnames2ndlevel:
                    print(dirrr)
        '''
        '''for extension in video_extensions:
            # use fnmatch to match files with video extensions
            for filename in fnmatch.filter(filenames, extension):
                print(filename)
                # print the absolute path of the video file
                print(os.path.abspath(os.path.join(root, filename)))'''
    print("Tempo Total: ", formataMinutosSegundos(tempo_total_videos))
    return videos

""" Verifica se foram encontrados arquivos maiores que o tamanho limite"""
def verify_file_size(folder_arg, limit_size_in_mb:int):
    found_files_bigger_than_limit_size = False
    found_files_arr = []
    for root_folder, directories, files in os.walk(folder_arg):
        for file in files:
            file_path = os.path.join(root_folder, file)
            file_size = os.path.getsize(file_path)
            size_mb = file_size / (1024 * 1024)  # Converter para MB

            if size_mb > limit_size_in_mb:
                found_files_bigger_than_limit_size = True
                found_files_arr.append(file_path)
    if (found_files_bigger_than_limit_size):
        print(f"Foram encontrados arquivos maiores que {limit_size_in_mb:.2f} MB em {folder_arg}:")
        for found_file in found_files_arr:
            print(f"O arquivo {found_file} tem ({size_mb:.2f} MB).")
    else:
        print(f"Não foram encontrados arquivos maiores que {limit_size_in_mb:.2f} MB em {folder_arg}.")

"""
Finds empty folders recursively
"""
def encontra_pastas_vazias(path):
    empty_directories = []
    for root, dirs, files in os.walk(path, topdown=False):
        for dir_name in dirs:
            folder_path = os.path.join(root, dir_name)
            if not os.listdir(folder_path):
                # folder_path:str = folder_path
                print("Pasta vazia encontrada: ", folder_path[len(root_path) + 1:])
                empty_directories.append(folder_path)
    if not empty_directories:
        print(f"Foram encontradas pastas vazias em {path}:")
        for empty_folder in empty_directories:
            print(f"A pasta {empty_folder} está vazia.")
    else:
        print(f"Não foram encontradas pastas vazias em {path}.")

# volume_multiplier => Fator pelo qual o volume será multiplicado (1.0 mantém o volume original)
def change_volume_in_section(video_path, start_time, end_time, volume_multiplier, output_path):
    # Carrega o vídeo
    video = VideoFileClip(video_path)



    # Define o trecho do vídeo em que o volume será aumentado
    if end_time == -1:
        video_section = video.subclip(start_time, video.duration)
    else:
        video_section = video.subclip(start_time, end_time)

    # Aumenta o volume do trecho do vídeo
    video_section = video_section.volumex(volume_multiplier)

    # Obtém o trecho do vídeo antes do ponto de início
    pre_section = video.subclip(0, start_time)

    # Obtém o trecho do vídeo após o ponto final
    post_section = video.subclip(end_time, video.duration)

    # Concatena os trechos do vídeo
    final_video = concatenate_videoclips([pre_section, video_section, post_section])

    # Mantém as configurações originais do vídeo (resolução e taxa de quadros)
    final_video = final_video.set_make_frame(video.make_frame)
    final_video = final_video.set_duration(video.duration)

    # Salva o vídeo resultante com alta qualidade usando o codec libx264
    final_video.write_videofile(output_path, codec='libx264', bitrate="5000k")

    # Fecha o vídeo carregado
    video.close()
    final_video.close()
