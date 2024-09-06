from linebot.v3.messaging.models import (
    FlexMessage,
    FlexBubble,
    FlexComponent,
    FlexBox,
    Action
)
more_info = """
羽球等級評估機器人

- 問卷依據台灣羽球推廣協會制定的雙打標準設計。
- 詳細判斷流程可參考下列連結中的 questions.json。
- 目前測試中，歡迎直接在聊天視窗提供意見與建議或是貢獻程式碼。

Version：v0.5.1
Author: Showaykerker
GitHub: https://github.com/showaykerker/badminton-level-evaluator-linebot
"""

image_url = "https://scontent-tpe1-1.xx.fbcdn.net/v/t1.6435-9/198038327_324577535828328_6570501766066799730_n.png?_nc_cat=106&ccb=1-7&_nc_sid=f727a1&_nc_ohc=7XJgFbkmYaYQ7kNvgFhG5By&_nc_ht=scontent-tpe1-1.xx&oh=00_AYAwde3o-2Vo2uJLv6c1N6qk_LEha6hAKPUjQGQjVpfm3Q&oe=67026F24"

# https://www.facebook.com/2020TAIWANBADMINTON/photos/pb.100068630171046.-2207520000/324577532494995/?type=3