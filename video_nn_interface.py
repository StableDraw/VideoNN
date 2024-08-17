from VideoEditor.video_editor import VideoEditor
from StableAudio.stable_audio import StableAudio



class ChatBot:
    '''
    Чат-бот: нейронка, способная генерировать текстовые ответы на текстовые сообщения пользователя, учитывая контекст беседы
    '''

    def __init__(self):
        '''
        Инициализация класса нейронки для начала общения
        '''
        pass


    def reset(self):
        '''
        Метод, обновляющий беседу
        '''
        self.is_started = False #Была ли начата беседа


    def text_to_text(self, prompt: str, id: str) -> str:
        '''
        Метод, генерирующий текстовый ответ на текстовый запрос
        Принимает текст и строковый id идентификатор пользователя
        Возвращает текст
        '''

        if self.is_started == False:
            self.is_started = True
            #Первый запрос к нейронке, запоминаем историю
        else:
            #Второй запрос к нейронке
            pass

        text = "Some text" #Заглушка

        return text
    


def text_to_audio(prompt: str) -> bytes:
    '''
    Генерация аудио по тексту
    Принимает промпт в виде текста
    Возвращает waw аудиофайл в виде строки байт
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

    with open("AnimateDiffLightning\\output.mp4", "rb") as f:
        output = f.read()

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