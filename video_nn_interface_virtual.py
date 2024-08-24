import random



class ChatBot:
    '''
    Чат-бот: нейронка, способная генерировать текстовые ответы на текстовые сообщения пользователя, учитывая контекст беседы
    '''
    def __init__(self):
        '''
        Инициализация класса нейронки для начала общения
        '''
        
        self.history = []
        self.counter = 0


    def reset(self, user_id: str):
        '''
        Метод, обновляющий беседу с пользователем
        Принимает строковый id пользователя
        '''

        self.history = []
        self.counter = 0

    
    def get_history(self, user_id: str):
        '''
        Метод, позволяющий получить историю переписки пользователя
        Принимает строковый id пользователя
        Возвращает список строк
        '''

        return self.history


    def text_to_text(self, prompt: str, user_id: str) -> str:
        '''
        Метод, генерирующий текстовый ответ на текстовый запрос
        Принимает текст и строковый id идентификатор пользователя
        Возвращает текст
        '''

        if self.counter % 2 == 0:
            response = "--User message " + str(self.counter)
        else:
            response = "--NN message " + str(self.counter)

        self.counter += 1
        self.history.append(response)

        return response
    


def text_to_audio(prompt: str) -> bytes:
    '''
    Генерация аудио по тексту
    Принимает промпт в виде текста
    Возвращает wav аудиофайл в виде строки байт
    '''

    with open("audio.wav", "rb") as f:
        output = f.read()

    return output


def text_to_video(prompt: str, is_long: bool = False) -> bytes:
    '''
    Генерация видео по тексту
    Принимает промпт в виде текста и флаг is_long, отвечающий за то, длинное видео будет генерироваться или короткое
    Возвращает mp4 видеофайл в виде строки байт
    '''

    with open("video.mp4", "rb") as f:
        output = f.read()

    return output


def cut_media(media: bytes, cut_list: list) -> bytes:
    '''
    Обрезка медиа (видео или аудио)
    Принимает медиа (видео или аудио) в виде строки байт, а также список словарей обрезки в формате [{"start": 0.0, "end": 0.0}, {"start": 0.0, "end": 0.0}, ]
    Возвращает обрезанное медиа (видео или аудио) в виде строки байт
    '''

    files = ["audio.wav", "video.mp4"]

    with open(files[random.randint(0, 1)], "rb") as f:
        output = f.read()

    return output