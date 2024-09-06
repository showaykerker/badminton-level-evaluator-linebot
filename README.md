# badminton-level-evaluator-linebot

## 專案緣起

某個晚上突然想到就把頭洗下去了...

![](imgs/screenshot.jpg)

## 使用方法

1. 在 Line 上加入好友：https://lin.ee/WSIa0i6
2. 從選單點選 "開始測試" 來進行評估
3. 根據提示回答問題
4. 獲得您的羽球技能等級評估結果


## 問卷設計

本問卷依照台灣羽球推廣協會制定的分級制度表設計問卷，判斷流程如下

### 新手階 （1~3級）

```mermaid

graph TD
    A[開始] --> B{"1）熟悉規則和禮儀?"}
    B -->|否| Z1[1級]
    B -->|是| C{"2）高球來回?"}
    C -->|少於10拍| Z1
    C -->|10拍或以上| D{"3）發球成功率?"}
    D -->|低於50%| Z1
    D -->|50-90%| Z2[2級]
    D -->|90%以上| E{"4）正確握拍?"}
    E -->|否| Z3[3級]
    E -->|是| F[繼續到初階評估]

    A:::nextStage
    Z1:::determinedLevel --> END[結束]
    Z2:::determinedLevel --> END
    Z3:::determinedLevel --> END
    F:::nextStage
    END:::stopStage

    classDef nextStage       fill:#FFD1A4,stroke:#FF9224,stroke-width:2px,color:#642100;
    classDef determinedLevel fill:#A6FFA6,stroke:#00EC00,stroke-width:2px,color:#467500;
    classDef stopStage       fill:#A3D1D1,stroke:#5CADAD,stroke-width:2px,color:#484891;

```

### 初階 （4~5級）

```mermaid

graph TD
    A[從新手階評估繼續] --> F{"5）長球能力?"}
    F -->|都不符合| Z3[3級]
    F -->|男後場/女中後場| G{"6）基本腳步和輪轉?"}
    G -->|完全不懂| Z4[4級]
    G -->|略懂不熟練| Z5[5級]
    G -->|熟悉並應用| H[繼續到初中階評估]

    A:::nextStage
    Z3:::determinedLevel --> END
    Z4:::determinedLevel --> END
    Z5:::determinedLevel --> END
    H:::nextStage
    END:::stopStage

    classDef nextStage       fill:#FFD1A4,stroke:#FF9224,stroke-width:2px,color:#642100;
    classDef determinedLevel fill:#A6FFA6,stroke:#00EC00,stroke-width:2px,color:#467500;
    classDef stopStage       fill:#A3D1D1,stroke:#5CADAD,stroke-width:2px,color:#484891;

```

### 初中階 （6~7級）

```mermaid

graph TD
    A[從初階評估繼續] --> H{"7）殺球切球長球?"}
    H -->|會用但不穩定| Z6[6級]
    H -->|七成以上穩定| I{"8）防守能力?"}
    I -->|基本無變化| Z7[7級]
    I -->|有變化或有威脅| J[繼續到中階評估]

    J:::nextStage
    A:::nextStage
    Z6:::determinedLevel --> END[結束]
    Z7:::determinedLevel --> END
    END:::stopStage

    classDef nextStage       fill:#FFD1A4,stroke:#FF9224,stroke-width:2px,color:#642100;
    classDef determinedLevel fill:#A6FFA6,stroke:#00EC00,stroke-width:2px,color:#467500;
    classDef stopStage       fill:#A3D1D1,stroke:#5CADAD,stroke-width:2px,color:#484891;

```

### 中階以上（8~18級）

```mermaid

graph TD
    A[從初中階評估繼續] --> J{"9）球路準確性?"}
    J -->|七成以上| Z8[8級]
    J -->|三種九成以上| K{"10）戰略和輪轉?"}
    K -->|基本熟悉| Z9[9級]
    K -->|能活用| L{"11）反拍和防守?"}
    L -->|熟練有威脅| Z11[11級]
    L -->|侵略性強| Z13["13-18級"]

    A:::nextStage
    Z8:::determinedLevel --> END[結束]
    Z9:::determinedLevel --> END
    Z11:::determinedLevel --> END
    Z13:::determinedLevel --> END
    END:::stopStage

    classDef nextStage       fill:#FFD1A4,stroke:#FF9224,stroke-width:2px,color:#642100;
    classDef determinedLevel fill:#A6FFA6,stroke:#00EC00,stroke-width:2px,color:#467500;
    classDef stopStage       fill:#A3D1D1,stroke:#5CADAD,stroke-width:2px,color:#484891;

```

## 技術棧

- 後端：Python
- 框架：Flask
- 部署：Heroku
- 介面：Line Bot


## 參考連結

- [台灣羽球推廣協會分級制度](https://www.facebook.com/2020TAIWANBADMINTON/photos/pb.100068630171046.-2207520000/324577532494995/?type=3)
- [Line Messaging API](https://developers.line.biz/en/docs/messaging-api/)
- [Python + Line bot 從頭開始建立一個 Line 機器人，部署到 Heroku！ | by Molly M | Medium](https://molly1024.medium.com/python-%E8%88%87-line-bot-%E5%BE%9E%E9%A0%AD%E9%96%8B%E5%A7%8B%E5%BB%BA%E7%AB%8B%E4%B8%80%E5%80%8B-line-%E6%A9%9F%E5%99%A8%E4%BA%BA-%E9%83%A8%E7%BD%B2%E5%88%B0-heroku-51512b04cb7b)

## 貢獻

歡迎提交 Pull Requests 或開 Issues 來幫助改進這個專案。

## 授權

本專案採用 MIT 授權。詳見 [LICENSE](LICENSE) 文件。