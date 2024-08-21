from InternLMChat.internlm import InternLMChat
from AnimateDiffLightning.animate_diff_lightning import external_text_to_video, image_array_to_binary_video
from StableAudio.stable_audio import StableAudio
from ToonCrafter.toon_crafter import gen_scenes_transition
from MultichannelRealESRGAN.RealESRGAN import RealESRGAN_upscaler as upscaler
from VideoEditor.video_editor import VideoEditor
from math import ceil
from tqdm import tqdm



#from TGWriter.tg_writer import TGWriter




def video_script_to_prompts(video_response: str) -> list:
    '''
    Метод для преобразования ответа от нейронки в список промптов для генерации сцен клипов
    '''

    prompt_list = []

    while True:
        pos = video_response.find("\n")
        while pos == 0:
            video_response = video_response[1:]
            pos = video_response.find("\n")

        if pos == -1:
            break

        prompt = video_response[:pos]

        while prompt[-1] in (".", " "):
            prompt = prompt[:-1]

        video_response = video_response[pos + 1:]

        prompt_list.append(prompt)

    is_count = True

    for i, prompt in enumerate(prompt_list):
        if prompt[0] != str(i + 1):
            is_count = False
            break

    if is_count:
        for i, prompt in enumerate(prompt_list):
            prompt = prompt[1:]
            while prompt[0] in (")", ".", " "):
                prompt = prompt[1:]
        prompt_list[i] = prompt

    return prompt_list



def text_to_long_video(prompt: str) -> bytes:
    '''
    Функция для генерации длинных видео
    Принимает текстовое описание видео
    Возвращает mp4 видео в виде массива байт
    '''

    '''
    tg = TGWriter() #Временная штука для печати в ТГ о статусе генерации для отладки
    print("Генерация начата")
    tg.print_msg("Генерация начата")
    '''


    #Генерация промптов для нейронок:
    ic = InternLMChat() #Инициализируем чат-бот

    segments_duration = 2 #Длина сегментов видео

    video_prompt = f"I\'m creating an anime clip by a neural network that generates video. The theme of my video is \"{prompt}\". The clip consists of short {segments_duration} second segments. Please write short, bright one sentence prompts for the neural network that would describe each segment of this clip separately. Describe each segment separately, as prompt for neural network. Write each prompt from the next line and no additional information. Don't describe changes of plan and camera movements. No segment numbers, only prompts separated by \n symbol"

    video_response, history = ic.text_to_text(prompt = video_prompt, history = []) #Генерируем описание для видео

    video_prompts = video_script_to_prompts(video_response = video_response) #Преобразуем ответ от нейронки в список промптов


    '''
    print("1. Промпты:")
    tg.print_msg("1. Промпты:")
    for prompt in video_prompts:
        print(prompt)
        tg.print_msg(prompt)
    '''


    audio_prompt = "Write a one short, bright one sentence description prompt to generate background ambient audio for all this clip"

    audio_response, _ = ic.text_to_text(prompt = audio_prompt, history = history) #Генерируем описание для видео

    if audio_response[-1] == ".":
        audio_response = audio_response[:-1]


    '''
    print(audio_response)
    tg.print_msg(audio_response)
    print("2. Аудио")
    tg.print_msg("2. Аудио")
    '''

    #Генерация аудио:
    clip_len = int(ceil(2.0 * len(video_prompts) + 2 * (len(video_prompts) - 1))) #Вычисляем длину необходимого клипа, в секундах

    sa = StableAudio()
    audio = sa.text_to_audio(prompt = audio_response, duration = clip_len) #Генерируем аудио по тексту


    '''
    print("3. Видео")
    tg.print_msg("3. Видео")
    c = 1
    '''


    #Генерация видеофрагментов:
    video_segments_list = []

    for prompt in tqdm(video_prompts):
        output, _ = external_text_to_video(prompt = prompt, output_type = "frames")
        video_segments_list.append(output) #Генерируем список кортежей видеоклипов и ключевых кадров
        '''
        tg.print_msg(str(c) + "/" + str(len(video_prompts)))
        c += 1
        '''



    '''
    print("4. Переходы")
    tg.print_msg("4. Переходы")
    c = 1
    '''

    #Генерация переходов между сценами:
    final_segments_list = []

    for i in tqdm(range(len(video_segments_list) - 1)):
        output = gen_scenes_transition(prompt = "an anime scene", frame_1 = video_segments_list[i][-1], frame_2 = video_segments_list[i + 1][0], return_video = False)
        final_segments_list.append(video_segments_list[i])
        final_segments_list.append(output)
        '''
        tg.print_msg(str(c) + "/" + str(len(video_segments_list) - 1))
        c += 1
        '''
    final_segments_list.append(video_segments_list[-1])


    '''
    print("6. Апскейл")
    tg.print_msg("6. Апскейл")
    c = 1
    '''

    #Апскейл кадров видео:
    params = {
            "model": "RealESRGAN_x4plus_anime_6B",    #Модель для обработки ("RealESRGAN_x4plus" - модель x4 RRDBNet, "RealESRNet_x4plus" - модель x4 RRDBNet, "RealESRGAN_x4plus_anime_6B" - модель x4 RRDBNet с 6 блоками, "RealESRGAN_x2plus" - модель x2 RRDBNet, "realesr-animevideov3" - модель x4 VGG-стиля (размера XS), "realesr-general-x4v3" - модель x4 VGG-стиля (размера S)) 
            "denoise_strength": 0.0,            #Сила удаления шума. 0 для слабого удаления шума (шум сохраняется), 1 для сильного удаления шума. Используется только для модели "realesr-general-x4v3"
            "outscale": 4,                      #Величина того, во сколько раз увеличть разшрешение изображения (модель "RealESRGAN_x2plus" x2, остальные x4)
            "tile": 0,                          #Размер плитки, 0 для отсутствия плитки во время тестирования
            "tile_pad": 10,                     #Заполнение плитки
            "pre_pad": 0,                       #Предварительный размер заполнения на каждой границе
            "face_enhance": False,               #Использовать GFPGAN улучшения лиц
            "version": "RestoreFormer",         #Версия модели для улучшения лиц. Только если выбран "face_enhance: True. Возможне значения: "1.1", "1.2", "1.3", "1.4", "RestoreFormerGFPGAN", "RestoreFormer". Модель 1.1 тестовая, но способна колоризировать. Модель 1.2 обучена на большем количестве данных с предобработкой, не способна колоризировать, генерирует достаточно чёткие изображения с красивым магияжем, однако иногда результат генерации выглядит не натурально. Модель 1.3 основана на модели 1.2, генерирует более натурально выглядящие изображения, однако не такие чёткие, выдаёт лучие результаты на более низкокачественных изображениях, работает с относительно высококачественными изображениями, может иметь повторяющееся (дважды) восстановление. Модель 1.4 обеспечивает немного больше деталей и лучшую идентичность. Модель RestoreFormer создана специально для улучшения лиц, "RestoreFormer_GFPGAN" обеспечивает более чёткую, однако менее натуралистичную обработку и иногда создаёт артифакты.
            "input_is_latent": True,            #Скрытый ли вход. Только для Только если выбран "face_enhance: True и "version" от 1.1 до 1.4. Если выбран, то результат менее насыщенный и чёткий, но более наруральный
            "fp32": True,                       #Использовать точность fp32 во время вывода. По умолчанию fp16 (половинная точность)
            "alpha_upsampler": "realesrgan",    #Апсемплер для альфа-каналов. Варианты: "realesrgan" | "bicubic", Только для "face_enhance" == False
            "gpu-id": None,                     #Устройство gpu для использования (по умолчанию = None) может быть 0, 1, 2 для обработки на нескольких GPU
            "seed": 42,                         #Начальное инициализирующее значение
            #на данный момент "max_dim": pow(1024, 2) ((для всех моделей, кроме "RealESRGAN_x2plus") и "outscale": 4), и pow(2048, 2) (для модели "RealESRGAN_x2plus" и "outscale": 2)
        }

    upscaled_list = []

    for clip in tqdm(final_segments_list):
        for frame in clip:
            new_frame = upscaler(frame, params)
            upscaled_list.append(new_frame)
        '''
        tg.print_msg(str(c) + "/" + str(len(final_segments_list)))
        c += 1
        '''


    '''
    print("7. Преобразование кадров в видео")
    tg.print_msg("7. Преобразование кадров в видео")
    '''

    '''
    #Преобразование кадров в видеоклипы:
    final_video_list = []
    for clip in tqdm(final_segments_list):
        video = image_array_to_binary_video(video = clip[0], fps = clip[1], video_codec = "libx264", is_image_list = True)
        final_video_list.append(video)
    '''
    #Преобразование кадров в видеоклипы:
    video_output = image_array_to_binary_video(video = upscaled_list, fps = 8, video_codec = "libx264", is_image_list = True)
    #final_video_list.append(video)

    
    '''
    print("8. Объединение")
    tg.print_msg("8. Объединение")
    '''


    #Объединение фрагментов воедино:
    ve = VideoEditor()
    #video_output = ve.merge_videos(videos_list = final_video_list) #Объеденяем все видео воедино
    final_video_output = ve.merge_video_and_audio(binary_video = video_output, binary_audio = audio) #Объедденяем видео с аудио







    return final_video_output



if __name__ == "__main__":

    prompt = "diving"

    output = text_to_long_video(prompt = prompt)

    with open("output.mp4", "wb") as f:
        f.write(output)