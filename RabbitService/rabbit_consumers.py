import json

class Consumer :
   def __init__(self, exchange_input, exchange_output, response_function):  
      self.exchange_input = exchange_input  
      self.exchange_output = exchange_output
      self.response_function = response_function

class RabbitConsumerService :
   def __init__(self, channel, consumers):
      self.channel = channel  
      self.consumers = consumers

   def generate_responce(self, body, message, exchange):
      response = {
         "messageId": body['messageId'],
         "conversationId": body['conversationId'],
         "sourceAddress": body['sourceAddress'],
         "destinationAddress": body['destinationAddress'],
         "requestId": body['requestId'],
         "messageType": ['urn:message:' + exchange],
         "message": message
      }

      return json.dumps(response)

   def rabbit_message_callback(self, ch, method, properties, body):
      # print(f"\n\n{ch}\n\n")
      print(f"\n\n{method}\n\n")
      # print(f"\n\n{properties}\n\n")
   
      for consumer in self.consumers:
         if consumer.exchange_input == method.exchange:     
            try:
               data = json.loads(body)
               response = self.generate_responce(json.loads(body), consumer.response_function(data['message']), consumer.exchange_output)
               self.channel.basic_publish(exchange=consumer.exchange_output, routing_key='', body=response)
               print(f"OK: {consumer.exchange_output}\n")
               self.channel.basic_ack(delivery_tag=method.delivery_tag)
               return
            except:     
               print(f'ERROR ACK: exchange "{method.exchange}"\n')
               self.channel.basic_ack(delivery_tag=method.delivery_tag)
               return

      # if we caught different exchange, we going to send it back
      print(f'NACK: exchange "{method.exchange}" is not support by this consumer\n')
      self.channel.basic_nack(delivery_tag=method.delivery_tag)
      return
