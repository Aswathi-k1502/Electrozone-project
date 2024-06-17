from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from chat_app.models import Message
from .serializers import MessageSerializer
import nltk
from nltk.chat.util import Chat, reflections

pairs = [
    (r'hi|hello', ['Hello!', 'Hi there!']),
    (r'how are you?', ['I am fine, thank you.', 'Doing well, thank you!']),
]

chatbot = Chat(pairs, reflections)


@api_view(['POST'])
def chatbot_response(request):
    user_message = request.data.get('message')
    bot_response = chatbot.respond(user_message)
    if not bot_response:
        bot_response = "I am sorry, I do not understand that."
    message = Message(user_message=user_message, bot_response=bot_response)
    message.save()
    serializer = MessageSerializer(message)
    return Response(serializer.data, status=status.HTTP_200_OK)
