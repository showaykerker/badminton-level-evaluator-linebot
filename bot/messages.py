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
- 詳細判斷流程可參考下列連結中的README。
- 歡迎直接在聊天視窗提供意見與建議或是貢獻程式碼。
- 近期計畫將服務改寫成Discord Bot。Line Bot將在移至Discord後停止使用。

Version：v0.5.6
Author: showaykerker
GitHub: https://github.com/showaykerker/badminton-level-evaluator-linebot
"""

image_url = "https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjKNSEJ5TzR_DhW6Vge15SC1rOg17dleYbfsU66L2vZZ2j-09pdy2yaZ1evmrYJH36skVnxcRQzb6w_AQgrkUeiFyVDxe5isKtwxkWiS9tteF-r14b_EyKgzo_ZeUrmgwkN0p7NZQWXZGaH/w448-h640/%25E7%25A8%258B%25E5%25BA%25A6%25E5%2588%2586%25E7%25B4%259A%25E8%25AA%25AA%25E6%2598%258E.png"

# https://www.facebook.com/2020TAIWANBADMINTON/photos/pb.100068630171046.-2207520000/324577532494995/?type=3
