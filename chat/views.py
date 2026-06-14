from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Message

@login_required(login_url='login')
def chat(request):
    messages = Message.objects.all().order_by('created_at')
    context = {
        'messages': messages,
    }
    return render(request, 'chat/chat.html', context)

@login_required(login_url='login')
@require_http_methods(["POST"])
@csrf_exempt
def send_message(request):
    try:
        data = json.loads(request.body)
        content = data.get('content', '').strip()
        
        if not content:
            return JsonResponse({'error': 'Message cannot be empty'}, status=400)
        
        message = Message.objects.create(
            sender=request.user,
            content=content
        )
        
        return JsonResponse({
            'success': True,
            'message': {
                'id': message.id,
                'sender': message.sender.username,
                'content': message.content,
                'created_at': message.created_at.strftime('%Y-%m-%d %H:%M:%S')
            }
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@login_required(login_url='login')
def get_messages(request):
    messages = Message.objects.all().order_by('created_at')
    messages_data = [
        {
            'id': msg.id,
            'sender': msg.sender.username,
            'content': msg.content,
            'created_at': msg.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'is_owner': msg.sender == request.user
        }
        for msg in messages
    ]
    return JsonResponse({'messages': messages_data})
