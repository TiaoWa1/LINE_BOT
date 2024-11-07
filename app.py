from flask import Flask, request, abort

from linebot.v3 import (
    WebhookHandler
)
from linebot.v3.exceptions import (
    InvalidSignatureError
)
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    TextMessage,
    Emoji,
    VideoMessage,
    AudioMessage,
    LocationMessage,
    StickerMessage,
    ImageMessage,
    ReplyMessageRequest,
    TemplateMessage,
    ConfirmTemplate,
    ButtonsTemplate,
    CarouselTemplate, CarouselColumn,
    ImageCarouselTemplate, ImageCarouselColumn,
    PostbackAction, URIAction, MessageAction, DatetimePickerAction, CameraAction, CameraRollAction, LocationAction,
    ReplyMessageResponse, PushMessageRequest, BroadcastRequest, MulticastRequest,
    FlexMessage, FlexContainer, 
    QuickReply, QuickReplyItem,
    MessagingApiBlob, RichMenuSize, RichMenuRequest, RichMenuArea, RichMenuBounds
)

## Webhook Event
from linebot.v3.webhooks import (
    MessageEvent,
    FollowEvent,
    PostbackEvent,
    TextMessageContent
)

import json, requests, os

app = Flask(__name__)

CHANNEL_ACCESS_TOKEN = os.getenv('CHANNEL_ACCESS_TOKEN')
configuration = Configuration(access_token=CHANNEL_ACCESS_TOKEN)
line_handler = WebhookHandler(os.getenv('CHANNEL_SECRET'))


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        line_handler.handle(body, signature)
    except InvalidSignatureError:
        app.logger.info("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'
# Rich Menu 
def create_rich_menu_1():
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        line_bot_blob_api = MessagingApiBlob(api_client)
        # 定義點擊區域與觸發active
        areas=[
            RichMenuArea(
                bounds=RichMenuBounds(
                    x=0,
                    y=0,
                    width=833,
                    height=843
                ),
                action=MessageAction(text="A")
            ),
            RichMenuArea(
                bounds=RichMenuBounds(
                    x=833,
                    y=0,
                    width=833,
                    height=843
                ),
                action=MessageAction(text="B")
            ),
            RichMenuArea(
                bounds=RichMenuBounds(
                    x=1666,
                    y=0,
                    width=833,
                    height=843
                ),
                action=MessageAction(text="C")
            ),
            RichMenuArea(
                bounds=RichMenuBounds(
                    x=0,
                    y=843,
                    width=833,
                    height=843
                ),
                action=MessageAction(text="D")
            ),
            RichMenuArea(
                bounds=RichMenuBounds(
                    x=833,
                    y=843,
                    width=833,
                    height=843
                ),
                action=MessageAction(text="E")
            ),
            RichMenuArea(
                bounds=RichMenuBounds(
                    x=1666,
                    y=843,
                    width=833,
                    height=843
                ),
                action=MessageAction(text="F")
            )
        ]
        # 定義 RichMenuRequest 物件
        rich_menu_to_create = RichMenuRequest(
            size=RichMenuSize(
                width=2500,
                height=1686
            ),
            selected=True,
            name="圖文選單",
            chatBarText="查看更多",
            areas=areas
        )
        # create_rich_menu 方法建立物件,透過.rich_menu_id 拿到id
        rich_menu_id = line_bot_api.create_rich_menu(
            rich_menu_request=rich_menu_to_create
        ).rich_menu_id
        
        with open('./static/4_resized.jpg', 'rb') as image:
            line_bot_blob_api.set_rich_menu_image(
                rich_menu_id=rich_menu_id,
                body=bytearray(image.read()),
                _headers={'Content-Type': 'image/png'}
            )
        
        line_bot_api.set_default_rich_menu(rich_menu_id)

def create_rich_menu_2():
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        line_bot_blob_api = MessagingApiBlob(api_client)

        # Create rich menu
        headers = {
            'Authorization': 'Bearer ' + CHANNEL_ACCESS_TOKEN,
            'Content-Type': 'application/json'
        }
        body = {
            "size": {
                "width": 2500,
                "height": 1686
            },
            "selected": True,
            "name": "圖文選單 1",
            "chatBarText": "查看更多資訊",
            "areas": [
                {
                "bounds": {
                    "x": 0,
                    "y": 0,
                    "width": 833,
                    "height": 843
                },
                "action": {
                    "type": "message",
                    "text": "範圍 1"
                }
                },
                {
                "bounds": {
                    "x": 833,
                    "y": 0,
                    "width": 833,
                    "height": 843
                },
                "action": {
                    "type": "message",
                    "text": "範圍 2"
                }
                },
                {
                "bounds": {
                    "x": 1666,
                    "y": 0,
                    "width": 833,
                    "height": 843
                },
                "action": {
                    "type": "message",
                    "text": "範圍 3"
                }
                },
                {
                "bounds": {
                    "x": 0,
                    "y": 843,
                    "width": 833,
                    "height": 843
                },
                "action": {
                    "type": "message",
                    "text": "範圍 4"
                }
                },
                {
                "bounds": {
                    "x": 833,
                    "y": 843,
                    "width": 833,
                    "height": 843
                },
                "action": {
                    "type": "message",
                    "text": "範圍 5"
                }
                },
                {
                "bounds": {
                    "x": 1666,
                    "y": 843,
                    "width": 833,
                    "height": 843
                },
                "action": {
                    "type": "message",
                    "text": "範圍 6"
                }
                }
            ]
        }
        response = requests.post('https://api.line.me/v2/bot/richmenu', headers=headers, data=json.dumps(body).encode('utf-8'))
        response = response.json()
        print(response)
        if "richMenuId" in response:
            rich_menu_id = response["richMenuId"]
        else:
            print("richMenuId not found in response:", response)

        # Upload rich menu image
        with open('static/4_resized.jpg', 'rb') as image:
            line_bot_blob_api.set_rich_menu_image(
                rich_menu_id=rich_menu_id,
                body=bytearray(image.read()),
                _headers={'Content-Type': 'image/png'}
            )

        line_bot_api.set_default_rich_menu(rich_menu_id)

create_rich_menu_1()



## 監聽Webhook Event時，使用handler裝飾器，並將監聽的內容加入
# 接收加入好友事件(FollowEvent)
@line_handler.add(FollowEvent)
def handle_follow(event):
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        line_bot_api.reply_message(
            ReplyMessageRequest(
                replyToken=event.reply_token,
                messages=[
                    TextMessage(
                        text="嗨 $",
                        emojis=[
                            Emoji(index=2, productId="5ac21e6c040ab15980c9b444", emojiId="005"),
                        ]
                    )
                ]
            )
        )



# ## Quick Reply 練習
# @line_handler.add(MessageEvent, message=TextMessageContent)
# def handle_message(event):
#     text = event.message.text
#     with ApiClient(configuration) as api_client:
#         line_bot_api = MessagingApi(api_client)
#         if text == "quick reply":
#             postback_icon = request.root_url + "/static/1.jpg"
#             postback_icon = postback_icon.replace("http", "https")
#             message_icon = request.root_url + "/static/2.jpg"
#             message_icon = message_icon.replace("http", "https")
#             datetime_icon = request.root_url + "/static/3.jpg"
#             datetime_icon = datetime_icon.replace("http", "https")
#             date_icon = request.root_url + "/static/4.jpg"
#             date_icon = date_icon.replace("http", "https")
#             time_icon = request.root_url + "/static/5.jpg"
#             time_icon = time_icon.replace("http", "https")

#             quickReply = QuickReply(
#                 items=[
#                     QuickReplyItem(
#                         action=PostbackAction(
#                             label="Postback",
#                             data="postback",
#                             displayText="postback"
#                         ),
#                         imageUrl=postback_icon
#                     ),
#                     QuickReplyItem(
#                         action=MessageAction(
#                             label="message",
#                             text="message"
#                         ),
#                         imageUrl=message_icon
#                     ),
#                     QuickReplyItem(
#                         action=DatetimePickerAction(  # DatetimePickerAction 也是一種 Postbackevent
#                             label="Date",
#                             data="date",
#                             mode="date"
#                         ),
#                         imageUrl=date_icon
#                     ),
#                     QuickReplyItem(
#                         action=DatetimePickerAction(
#                             label="Time",
#                             data="time",
#                             mode="time"
#                         ),
#                         imageUrl=time_icon
#                     ),
#                     QuickReplyItem(
#                         action=DatetimePickerAction(
#                             label="Datetime",
#                             data="datetime",
#                             mode="datetime",
#                             initial="2024-01-01T00:00",
#                             max="2025-01-01T00:00",
#                             min="2023-01-01T00:00"
#                         ),
#                         imageUrl=datetime_icon
#                     ),
#                     QuickReplyItem(
#                         action=CameraAction(label="camera")
#                     ),
#                     QuickReplyItem(
#                         action=CameraRollAction(label="camera roll")
#                     ),
#                     QuickReplyItem(
#                         action=LocationAction(label="Location")
#                     )
#                 ]
#             )

#             line_bot_api.reply_message(
#                 ReplyMessageRequest(
#                     replyToken=event.reply_token,
#                     messages=[TextMessage(
#                         quickReply=quickReply,
#                         text='請選擇項目'
#                     )]
#                 )
#             )
# ## Postback Event 回應
# @line_handler.add(PostbackEvent)
# def handle_postback(event):
#     with ApiClient(configuration) as api_client:
#         line_bot_api = MessagingApi(api_client)
#         postback_data = event.postback.data # 取 postbackevent 用於判斷
#         if postback_data == "postback":
#             line_bot_api.reply_message(
#                 ReplyMessageRequest(
#                     replyToken=event.reply_token,
#                     messages=[TextMessage(text="Postback 回應")]
#                 )
#             )
#         elif postback_data == "date":
#             date = event.postback.params['date'] # 取值用來回應
#             line_bot_api.reply_message(
#                 ReplyMessageRequest(
#                     replyToken=event.reply_token,
#                     messages=[TextMessage(text=date)]
#                 )
#             )
#         elif postback_data == "time":
#             time = event.postback.params['time']
#             line_bot_api.reply_message(
#                 ReplyMessageRequest(
#                     replyToken=event.reply_token,
#                     messages=[TextMessage(text=time)]
#                 )
#             )
#         else:
#             datetime = event.postback.params['datetime']
#             line_bot_api.reply_message(
#                 ReplyMessageRequest(
#                     replyToken=event.reply_token,
#                     messages=[TextMessage(text=datetime)]
#                 )
#             )


# # Flex Message 練習
# @line_handler.add(MessageEvent, message=TextMessageContent)
# def handle_message(event):
#     text = event.message.text
#     with ApiClient(configuration) as api_client:
#         line_bot_api = MessagingApi(api_client)
#         if text == 'flex':
#             line_flex_json = {
#                 "type": "bubble",
#                 "hero": {
#                     "type": "image",
#                     "url": "https://cdn.discordapp.com/attachments/846291467595939900/1190989700257824791/948441691977830490.jpg?ex=672d5658&is=672c04d8&hm=5ee7422beff6a69c30180648ac37286a4699b93dfc4097b8d08c719e7dc331eb&",
#                     "size": "full",
#                     "aspectRatio": "4:3",
#                     "aspectMode": "cover"
#                 },
#                 "body": {
#                     "type": "box",
#                     "layout": "vertical",
#                     "contents": [
#                     {
#                         "type": "text",
#                         "text": "Dog",
#                         "weight": "bold",
#                         "size": "xl",
#                         "contents": [
#                         {
#                             "type": "span",
#                             "text": "Dog"
#                         },
#                         {
#                             "type": "span",
#                             "text": " is sad",
#                             "size": "md"
#                         }
#                         ]
#                     },
#                     {
#                         "type": "box",
#                         "layout": "baseline",
#                         "margin": "md",
#                         "contents": [
#                         {
#                             "type": "icon",
#                             "size": "sm",
#                             "url": "https://developers-resource.landpress.line.me/fx/img/review_gold_star_28.png"
#                         },
#                         {
#                             "type": "icon",
#                             "size": "sm",
#                             "url": "https://developers-resource.landpress.line.me/fx/img/review_gold_star_28.png"
#                         },
#                         {
#                             "type": "icon",
#                             "size": "sm",
#                             "url": "https://developers-resource.landpress.line.me/fx/img/review_gold_star_28.png"
#                         },
#                         {
#                             "type": "icon",
#                             "size": "sm",
#                             "url": "https://developers-resource.landpress.line.me/fx/img/review_gold_star_28.png"
#                         },
#                         {
#                             "type": "icon",
#                             "size": "sm",
#                             "url": "https://developers-resource.landpress.line.me/fx/img/review_gold_star_28.png"
#                         },
#                         {
#                             "type": "text",
#                             "text": "5.0",
#                             "size": "sm",
#                             "color": "#999999",
#                             "margin": "md",
#                             "flex": 0
#                         }
#                         ]
#                     },
#                     {
#                         "type": "box",
#                         "layout": "vertical",
#                         "margin": "lg",
#                         "spacing": "sm",
#                         "contents": [
#                         {
#                             "type": "box",
#                             "layout": "baseline",
#                             "spacing": "sm",
#                             "contents": [
#                             {
#                                 "type": "text",
#                                 "text": "Address",
#                                 "color": "#aaaaaa",
#                                 "size": "sm",
#                                 "flex": 1
#                             },
#                             {
#                                 "type": "text",
#                                 "text": "Fell so sad",
#                                 "wrap": True,
#                                 "color": "#666666",
#                                 "size": "sm",
#                                 "flex": 3
#                             }
#                             ]
#                         }
#                         ]
#                     }
#                     ]
#                 },
#                 "footer": {
#                     "type": "box",
#                     "layout": "horizontal",
#                     "contents": [
#                     {
#                         "type": "button",
#                         "action": {
#                         "type": "uri",
#                         "label": "Github",
#                         "uri": "https://github.com/TiaoWa1"
#                         },
#                         "style": "primary",
#                         "margin": "md"
#                     },
#                     {
#                         "type": "button",
#                         "action": {
#                         "type": "uri",
#                         "label": "Youtube",
#                         "uri": "https://www.youtube.com/@%E6%B0%B4%E7%89%9B-i3f"
#                         },
#                         "style": "secondary",
#                         "margin": "md"
#                     }
#                     ]
#                 }
#             }
#             line_flex_str = json.dumps(line_flex_json)
#             line_bot_api.reply_message(
#                 ReplyMessageRequest(
#                     replyToken=event.reply_token,
#                     messages=[FlexMessage(alt_text='詳細說明', contents=FlexContainer.from_json(line_flex_str))]
#                 )
#             )



# # Template Message 練習
# @line_handler.add(MessageEvent, message=TextMessageContent)
# def handle_message(event):
#     text = event.message.text
#     with ApiClient(configuration) as api_client:
#         line_bot_api = MessagingApi(api_client)

#         # Confirm Template
#         if text == 'Confirm':
#             confirm_template = ConfirmTemplate(
#                 text="今天學習了嗎?",
#                 actions=[
#                     MessageAction(label='否', text='否!'),
#                     MessageAction(label='是', text='是!')
#                 ]
#             )
#             template_message = TemplateMessage(
#                 altText='confirm alt Text', # 使用者接收到的訊息
#                 template=confirm_template
#             )
#             line_bot_api.reply_message(
#                 ReplyMessageRequest(
#                     replyToken=event.reply_token,
#                     messages=[template_message]
#                 )
#             )
#         # Button Template
#         elif text == 'Buttons':
#             url = request.root_url + '/static/POP.jpg'
#             url = url.replace("http", "https")
#             app.logger.info("url=" + url)
#             button_template = ButtonsTemplate(
#                 thumbnailImageUrl=url,  # 縮圖路徑
#                 title="示範",
#                 text='詳細說明',
#                 actions=[
#                     URIAction(label='連結', uri="https://github.com/TiaoWa1"),
#                     PostbackAction(label='回傳值', data='ping', displayText='傳了'), # 點下後觸發PostBackEvent,displaytext表示讓使用者傳送
#                     MessageAction(label="傳'哈囉'", text="哈囉"),
#                     DatetimePickerAction(label="選擇時間", data="時間", mode="datetime") # 讓使用者選擇日期
#                 ]
#             )
#             button_message = TemplateMessage(
#                 altText='Button alt Text',
#                 template=button_template
#             )
#             line_bot_api.reply_message(
#                 ReplyMessageRequest(
#                     replyToken=event.reply_token,
#                     messages=[button_message]
#                 )
#             )
#         # Carousel Template
#         elif text == 'Carousel':
#             url= request.root_url + '/static'
#             url = url.replace("http", "https")
#             app.logger.info("url=" + url)
#             carousel_template = CarouselTemplate(
#                 columns=[
#                     CarouselColumn(
#                         thumbnailImageUrl=url+'/1.jpg',
#                         title="第一項",
#                         text="這是第一項的描述",
#                         actions=[
#                             URIAction(
#                                 label="按我前往Google",
#                                 uri="https://www.google.com/"
#                             )
#                         ]
#                     ),
#                     CarouselColumn(
#                         thumbnailImageUrl=url+'/2.jpg',
#                         title="第二項",
#                         text="這是第二項的描述",
#                         actions=[
#                             URIAction(
#                                 label="按我前往我的Github",
#                                 uri="https://github.com/TiaoWa1"
#                             )
#                         ]
#                     )
#                 ]
#             )
#             carousel_message = TemplateMessage(
#                 altText='這是Carousel Template',
#                 template=carousel_template
#             )
#             line_bot_api.reply_message(
#                 ReplyMessageRequest(
#                     replyToken=event.reply_token,
#                     messages=[carousel_message]
#                 )
#             )
#         # Imagecarousel Template
#         elif text == 'Imagecarousel':
#             url = request.url_root + '/static'
#             url = url.replace("http", "https")
#             app.logger.info("url=" + url)
#             imagecarousel_template = ImageCarouselTemplate(
#                 columns=[
#                     ImageCarouselColumn(
#                         imageUrl=url+"/1.jpg",
#                         # 要注意 ImageCarouselColumn 的 action 只能放一種,所以不能用陣列的形式
#                         action=URIAction( 
#                             label="Google",
#                             uri="https://www.google.com/"
#                         )
#                     ),
#                     ImageCarouselColumn(
#                         imageUrl=url+"/2.jpg",
#                         action=URIAction(
#                             label="Github",
#                             uri="https://github.com/TiaoWa1"
#                         )
#                     ),
#                     ImageCarouselColumn(
#                         imageUrl=url+"/3.jpg",
#                         action=URIAction(
#                             label="Youtube",
#                             uri="https://www.youtube.com/@%E6%B0%B4%E7%89%9B-i3f"
#                         )
#                     ),
#                     ImageCarouselColumn(
#                         imageUrl=url+"/4.jpg",
#                         action=URIAction(
#                             label="Twitch",
#                             uri="https://www.twitch.tv/bears0711"
#                         )
#                     )
#                 ]
#             )
#             imagecarousel_message = TemplateMessage(
#                 altText="這是 ImageCaurousel Template",
#                 template=imagecarousel_template
#             )
#             line_bot_api.reply_message(
#                 ReplyMessageRequest(
#                     replyToken=event.reply_token,
#                     messages=[imagecarousel_message]
#                 )
#             )


# # Message Type 練習
# @line_handler.add(MessageEvent, message=TextMessageContent)
# def handle_message(event):
#     text = event.message.text
#     with ApiClient(configuration) as api_client:
#         line_bot_api = MessagingApi(api_client)

#         if text == '文字':
#             line_bot_api.reply_message(
#                 ReplyMessageRequest(
#                     reply_token=event.reply_token,
#                     messages=[TextMessage(text="這是文字訊息")]
#                 )
#             )
#         elif text == '表情符號':
#             emote = [
#                 Emoji(index=0, productId="5ac2213e040ab15980c9b447", emojiId="114"),
#                 Emoji(index=12, productId="5ac2213e040ab15980c9b447", emojiId="117")
#             ]
#             line_bot_api.reply_message(
#                 ReplyMessageRequest(
#                     replyToken=event.reply_token,
#                     messages=[TextMessage(text='$ LINE 表情符號 $', emojis=emote)]
#                 )
#             )
#         elif text == '貼圖':
#             line_bot_api.reply_message(
#                 ReplyMessageRequest(
#                     replyToken=event.reply_token,
#                     messages=[StickerMessage(packageId="789", stickerId="10855")]
#                 )
#             )
#         elif text == '圖片':
#             url = request.url_root + '/static/Hi.gif'
#             url = url.replace("http", "https")
#             app.logger.info("url=" + url)
#             line_bot_api.reply_message(
#                 ReplyMessageRequest(
#                     replyToken=event.reply_token,
#                     messages=[ImageMessage(originalContentUrl=url, previewImageUrl=url)]
#                 )
#             )
#         elif text == '影片':
#             url = request.url_root + '/static/ZEUS.mp4'
#             url = url.replace("http", "https")
#             app.logger.info("url=" + url)
#             line_bot_api.reply_message(
#                 ReplyMessageRequest(
#                     replyToken=event.reply_token,
#                     messages=[VideoMessage(originalContentUrl=url, previewImageUrl=url)]
#                 )
#             )
#         elif text == '音訊':
#             url = request.url_root + '/static/guigo.mp3'
#             url = url.replace("http", "https")
#             app.logger.info("url=" + url)
#             time_long = 60000 # 毫秒
#             line_bot_api.reply_message(
#                 ReplyMessageRequest(
#                     replyToken=event.reply_token,
#                     messages=[AudioMessage(originalContentUrl=url, duration=time_long)]
#                 )
#             )
#         elif text == "位置":
#             line_bot_api.reply_message(
#                 ReplyMessageRequest(
#                     replyToken=event.reply_token,
#                     messages=[
#                         LocationMessage(title="Location", address="Taipei", latitude=25.0475, longitude=121.5173)
#                     ]
#                 )
#             )
#         else:
#             line_bot_api.reply_message(
#                 ReplyMessageRequest(
#                     replyToken=event.reply_token,
#                     messages=[TextMessage(text=event.message.text)]
#                 )
#             )

# # Sending Message 練習
# @line_handler.add(MessageEvent, message=TextMessageContent)
# def message_text(event):
#     with ApiClient(configuration) as api_client:
#         line_bot_api = MessagingApi(api_client)

#         # Reply Message
#         line_bot_api.reply_message(
#             ReplyMessageRequest(
#                 reply_token=event.reply_token,
#                 messages=[TextMessage(text = 'reply message')]
#             )
#         )

#         result = line_bot_api.reply_message_with_http_info(
#             ReplyMessageRequest(
#                 replyToken=event.reply_token,
#                 messages=[TextMessage(text = "reply message with http info")]
#             )
#         )

#         # Push Message
#         line_bot_api.push_message_with_http_info(
#             PushMessageRequest(
#                 to=event.source.user_id,
#                 messages=[TextMessage(text = "Push!")]
#             )
#         )

#         # Broadcast Message
#         line_bot_api.broadcast_with_http_info(
#             BroadcastRequest(
#                 messages=[TextMessage(text="Broadcast!")]
#             )
#         )

#         # Multicast Message
#         line_bot_api.multicast_with_http_info(
#             MulticastRequest(
#                 to=[event.source.user_id],
#                 messages=[TextMessage(text="Multicast!")]
#             )
#         )

# # 接收訊息事件(MessageEvent)，訊息事件可以多傳入一個message參數，其中需要放入指定的訊息種類
# @line_handler.add(MessageEvent, message=TextMessageContent)
# def handle_message(event):
#     with ApiClient(configuration) as api_client:
#         line_bot_api = MessagingApi(api_client)
#         if event.message.text == 'postback':
#             buttons_template = ButtonsTemplate(
#                 title='Postback Sample',
#                 text='Postback Action',
#                 actions=[
#                     PostbackAction(label='Postback Action', text='Postback Action Button Clicked!', data="postback")
#                 ])
#             template_message = TemplateMessage(
#                 alt_text='Postback Sample',
#                 template=buttons_template
#             )
#             line_bot_api.reply_message(
#                 ReplyMessageRequest(
#                     reply_token=event.reply_token,
#                     messages=[template_message]
#                 )
#             )

# @line_handler.add(PostbackAction)
# def handle_postback(event):
#     # data 來自 PostbackAction 行
#     if event.postback.data == 'postback':
#         print('Postback event is triggered')



# @line_handler.add(MessageEvent, message=TextMessageContent)
# def handle_message(event):
#     with ApiClient(configuration) as api_client:
#         line_bot_api = MessagingApi(api_client)
#         line_bot_api.reply_message_with_http_info(
#             ReplyMessageRequest(
#                 reply_token=event.reply_token,
#                 # 接收使用者傳來的訊息，並用相同訊息回應
#                 messages=[TextMessage(text=event.message.text)]
#             )
#         )


if __name__ == "__main__":
    app.run()