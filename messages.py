from linebot.v3.messaging.models import (
    FlexMessage,
    FlexBubble,
    FlexComponent,
    FlexBox,
    Action
)
more_info = """
羽球等級評估機器人

版本：v0.2
Author: Showaykerker
"""

_level_table_flex_message_content = {
    "type": "bubble",
    "hero": FlexComponent(**{
        "type": "image",
        "url": "https://scontent-tpe1-1.xx.fbcdn.net/v/t1.6435-9/198038327_324577535828328_6570501766066799730_n.png?_nc_cat=106&ccb=1-7&_nc_sid=f727a1&_nc_ohc=7XJgFbkmYaYQ7kNvgFhG5By&_nc_ht=scontent-tpe1-1.xx&oh=00_AYAwde3o-2Vo2uJLv6c1N6qk_LEha6hAKPUjQGQjVpfm3Q&oe=67026F24",
        "margin": "none",
        "size": "full",
        "align": "center",
        "gravity": "center",
        "animated": True,
        "offsetTop": "xxl",
        "offsetBottom": "xxl"
    }),
    "body": FlexBox(**{
        "type": "box",
        "layout": "vertical",
        "contents": [
            FlexComponent(**{
                "type": "button",
                "action": Action(**{
                    "type": "uri",
                    "label": "圖片來源：台灣羽球推廣協會",
                    "uri": "https://www.facebook.com/2020TAIWANBADMINTON/photos/pb.100068630171046.-2207520000/324577532494995/?type=3"
                }),
                "position": "relative",
                "margin": "xl"
            })
        ]
    })
}

level_table_flex_message_content = {
  "type": "bubble",
  "hero": {
    "type": "image",
    "url": "https://scontent-tpe1-1.xx.fbcdn.net/v/t1.6435-9/198038327_324577535828328_6570501766066799730_n.png?_nc_cat=106&ccb=1-7&_nc_sid=f727a1&_nc_ohc=7XJgFbkmYaYQ7kNvgFhG5By&_nc_ht=scontent-tpe1-1.xx&oh=00_AYAwde3o-2Vo2uJLv6c1N6qk_LEha6hAKPUjQGQjVpfm3Q&oe=67026F24",
    "margin": "none",
    "size": "full",
    "align": "center",
    "gravity": "center",
    "animated": True,
    "offsetTop": "xxl",
    "offsetBottom": "xxl"
  },
  "body": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "button",
        "action": {
          "type": "uri",
          "label": "圖片來源：台灣羽球推廣協會",
          "uri": "https://www.facebook.com/2020TAIWANBADMINTON/photos/pb.100068630171046.-2207520000/324577532494995/?type=3"
        },
        "position": "relative",
        "margin": "xl"
      }
    ]
  }
}