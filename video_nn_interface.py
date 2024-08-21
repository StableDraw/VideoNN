from VideoEditor.video_editor import VideoEditor
from StableAudio.stable_audio import StableAudio
from AnimateDiffLightning.animate_diff_lightning import external_text_to_video
from InternLMChat.internlm import InternLMChat, reset_history, get_history
from long_video_gen import text_to_long_video


class ChatBot():
    '''
    Чат-бот: нейронка, способная генерировать текстовые ответы на текстовые сообщения пользователя, учитывая контекст беседы
    '''

    def reset(self, user_id: str):
        '''
        Метод, обновляющий беседу с пользователем
        Принимает строковый id пользователя
        '''

        reset_history(user_id = user_id) #Очищяем историю переписки для пользователя

    
    def get_history(self, user_id: str):
        '''
        Метод, позволяющий получить историю переписки пользователя
        Принимает строковый id пользователя
        Возвращает список строк истории переписки пользователя
        '''

        history = get_history(user_id = user_id) #Получаем историю переписки пользователя

        return history


    def text_to_text(self, prompt: str, user_id: str) -> str:
        '''
        Метод, генерирующий текстовый ответ на текстовый запрос
        Принимает текст и строковый id идентификатор пользователя
        Возвращает текст
        '''

        ic = InternLMChat()

        response = ic.do_chat(prompt = prompt, user_id = user_id)

        return response
    


def text_to_audio(prompt: str) -> bytes:
    '''
    Генерация аудио по тексту
    Принимает промпт в виде текста
    Возвращает wav аудиофайл в виде строки байт
    '''

    sa = StableAudio()

    output = sa.text_to_audio(prompt = prompt, duration = 30) #Генерируем аудио по тексту

    return output



def text_to_video(prompt: str, is_long: bool = False) -> bytes:
    '''
    Генерация видео по тексту
    Принимает промпт в виде текста и флаг is_long, отвечающий за то, длинное видео будет генерироваться или короткое
    Возвращает mp4 видеофайл в виде строки байт
    '''

    if not is_long: #Если это обычная генерация видео
        output = external_text_to_video(prompt = prompt)
    else: #Генерация длинного видео
        output = text_to_long_video(prompt = prompt)

    return output



def cut_media(media: bytes, cut_list: list) -> bytes:
    '''
    Обрезка медиа (видео или аудио)
    Принимает медиа (видео или аудио) в виде строки байт, а также список словарей обрезки в формате [{"start": 0.0, "end": 0.0}, {"start": 0.0, "end": 0.0}, ]
    Возвращает обрезанное медиа (видео или аудио) в виде строки байт
    '''

    ve = VideoEditor()
    
    output = ve.cut_media(media = media, cut_list = cut_list) #Обрезаем медиа

    return output