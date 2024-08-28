import base64
from video_nn_interface_virtual import text_to_audio, text_to_video, cut_media

class VideoEditorConsumer:
    def get_text_to_video_response(self, message):
        print(message)
        
        response = {
            "orderId": message['orderId'],
            "video": base64.b64encode(text_to_video(message['text'], message['isLong'])).decode('utf-8'),
            "errorMsg": message['errorMsg']
        }

        return response;

    def get_text_to_audio_response(self, message):
        print(message)

        response = {
            "orderId": message['orderId'],
            "audio": base64.b64encode(text_to_audio(message['text'])).decode('utf-8'),
            "errorMsg": message['errorMsg']
        }

        return response

    def get_cut_media_response(self, message):
        print(message)

        response = {
            "orderId": message['orderId'],
            "media": cut_media(message['media'], message['cuts']),
            "errorMsg": message['errorMsg']
        }

        return response