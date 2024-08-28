import pika

from RabbitService.rabbit_consumers import *
from RabbitService.consumers.chat_bot_consumer import ChatBotConsumer
from RabbitService.consumers.video_editor_consumer import VideoEditorConsumer

def main():
    # Устанавливаем соединение с сервером RabbitMQ
    credentials = pika.PlainCredentials('rmuser', 'rmpassword')
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port='5672', virtual_host='/', credentials=credentials))
    channel = connection.channel()

    # register consumers
    chat_bot_consumer = ChatBotConsumer()
    video_editor_consumer = VideoEditorConsumer()

    consumers = [
        Consumer("StableDraw.Contracts.NeuralChatContracts.Requests:ITextToTextRequest",
        "StableDraw.Contracts.NeuralChatContracts.Replies:ITextToTextReply",
        chat_bot_consumer.get_text_to_text_response),
        
        Consumer("StableDraw.Contracts.NeuralChatContracts.Requests:IResetChatRequest",
        "StableDraw.Contracts.NeuralChatContracts.Replies:IResetChatReply",
        chat_bot_consumer.get_reset_response),

        Consumer("StableDraw.Contracts.NeuralChatContracts.Requests:ITextToVideoRequest",
        "StableDraw.Contracts.NeuralChatContracts.Replies:ITextToVideoReply",
        video_editor_consumer.get_text_to_video_response),

        Consumer("StableDraw.Contracts.NeuralChatContracts.Requests:ITextToAudioRequest",
        "StableDraw.Contracts.NeuralChatContracts.Replies:ITextToAudioReply",
        video_editor_consumer.get_text_to_audio_response),

        Consumer("StableDraw.Contracts.NeuralChatContracts.Requests:ICutMediaRequest",
        "StableDraw.Contracts.NeuralChatContracts.Replies:ICutMediaReply",
        video_editor_consumer.get_cut_media_response),
    ]

    rabbitService = RabbitConsumerService(channel, consumers)

    channel.basic_consume(queue='neural_chat_consumer',
                        on_message_callback=rabbitService.rabbit_message_callback)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    # Начинаем прослушку
    channel.start_consuming()


main()