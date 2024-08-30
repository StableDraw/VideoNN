from video_nn_interface_virtual import ChatBot

class ChatBotConsumer:
    def __init__(self):
        self.chat_bot = ChatBot()


    def get_text_to_text_response(self, message):
        print(message)

        response = {
            "orderId": message['orderId'],
            "text": self.chat_bot.text_to_text(message['text'], message['userId']),
            "errorMsg": message['errorMsg']
        }

        return response;

    def get_reset_response(self, message):
        print(message)

        self.chat_bot.reset(message['userId']);

        response = {
            "orderId": message['orderId'],
            "errorMsg": message['errorMsg']
        }

        return response
