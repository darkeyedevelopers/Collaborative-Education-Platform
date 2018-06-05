import json

from channels import Group
from channels.auth import channel_session_user


@channel_session_user
def ws_connect(message):

    print 'connecting..'
    message.reply_channel.send({
        'accept': True
    })


@channel_session_user
def ws_receive(message):
    print "Receive"
    data = json.loads(message.content.get('text'))
    class_name = str(data.get('class_name'))
    class_name=class_name.replace(" ","_")
    print class_name,'added'
    Group(class_name).add(message.reply_channel)
    message.channel_session['class_group'] = class_name

@channel_session_user
def ws_disconnect(message):

    print 'disconnecting..'
    user_group = message.channel_session['class_group']
    Group(user_group).discard(message.reply_channel)