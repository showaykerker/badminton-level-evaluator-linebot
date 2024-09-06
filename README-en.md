# badminton-level-evaluator-linebot

## Project Origin

One night, I suddenly had this idea and dove right in...

![](imgs/screenshot.jpg)

## How to Use

1. Add as a friend on Line: https://lin.ee/WSIa0i6
2. Select "Start Test" from the menu to begin the evaluation
3. Answer the questions as prompted
4. Receive your badminton skill level assessment result

## Questionnaire Design

This questionnaire is designed based on the classification system established by the Taiwan Badminton Promotion Association. The assessment process is as follows:

### Beginner Stage (Levels 1-3)

```mermaid
graph TD
    A[Start] --> B{"1.Familiar with rules and etiquette?"}
    B -->|No| Z1[Level 1]
    B -->|Yes| C{"2.High clear rally?"}
    C -->|Less than 10 shots| Z1
    C -->|10 shots or more| D{"3.Serve success rate?"}
    D -->|Less than 50%| Z1
    D -->|50-90%| Z2[Level 2]
    D -->|Above 90%| E{"4.Correct grip?"}
    E -->|No| Z3[Level 3]
    E -->|Yes| F[Continue to Elementary assessment]

    A:::nextStage
    Z1:::determinedLevel --> END[End]
    Z2:::determinedLevel --> END
    Z3:::determinedLevel --> END
    F:::nextStage
    END:::stopStage

    classDef nextStage       fill:#FFD1A4,stroke:#FF9224,stroke-width:2px,color:#642100;
    classDef determinedLevel fill:#A6FFA6,stroke:#00EC00,stroke-width:2px,color:#467500;
    classDef stopStage       fill:#A3D1D1,stroke:#5CADAD,stroke-width:2px,color:#484891;
```

### Elementary Stage (Levels 4-5)

```mermaid
graph TD
    A[Continue from Beginner assessment] --> F{"5.Long shot ability?"}
    F -->|None apply| Z3[Level 3]
    F -->|Male backco

urt/Female mid-backcourt| G{"6.Basic footwork and rotation?"}
    G -->|No understanding| Z4[Level 4]
    G -->|Basic understanding| Z5[Level 5]
    G -->|Familiar and applied| H[Continue to Elementary-Intermediate assessment]

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

### Elementary-Intermediate Stage (Levels 6-7)

```mermaid
graph TD
    A[Continue from Elementary assessment] --> H{"7.Smash, drop shot, and long shot?"}
    H -->|Can use but unstable| Z6[Level 6]
    H -->|Over 70% stable| I{"8.Defense ability?"}
    I -->|Basic, no variation| Z7[Level 7]
    I -->|Varied or threatening| J[Continue to Intermediate assessment]

    J:::nextStage
    A:::nextStage
    Z6:::determinedLevel --> END[End]
    Z7:::determinedLevel --> END
    END:::stopStage

    classDef nextStage       fill:#FFD1A4,stroke:#FF9224,stroke-width:2px,color:#642100;
    classDef determinedLevel fill:#A6FFA6,stroke:#00EC00,stroke-width:2px,color:#467500;
    classDef stopStage       fill:#A3D1D1,stroke:#5CADAD,stroke-width:2px,color:#484891;
```

### Intermediate and Above (Levels 8-18)

```mermaid
graph TD
    A[Continue from Elementary-Intermediate assessment] --> J{"9.Shot accuracy?"}
    J -->|Over 70%| Z8[Level 8]
    J -->|Over 90% for three types| K{"10.Strategy and rotation?"}
    K -->|Basic familiarity| Z9[Level 9]
    K -->|Can apply effectively| L{"11.Backhand and defense?"}
    L -->|Proficient and threatening| Z11[Level 11]
    L -->|Highly aggressive| Z13["Levels 13-18"]

    A:::nextStage
    Z8:::determinedLevel --> END[End]
    Z9:::determinedLevel --> END
    Z11:::determinedLevel --> END
    Z13:::determinedLevel --> END
    END:::stopStage

    classDef nextStage       fill:#FFD1A4,stroke:#FF9224,stroke-width:2px,color:#642100;
    classDef determinedLevel fill:#A6FFA6,stroke:#00EC00,stroke-width:2px,color:#467500;
    classDef stopStage       fill:#A3D1D1,stroke:#5CADAD,stroke-width:2px,color:#484891;
```

## Tech Stack

- Backend: Python
- Framework: Flask
- Deployment: Heroku
- Interface: Line Bot

## References

- [Taiwan Badminton Promotion Association Classification System](https://www.facebook.com/2020TAIWANBADMINTON/photos/pb.100068630171046.-2207520000/324577532494995/?type=3)
- [Line Messaging API](https://developers.line.biz/en/docs/messaging-api/)
- [Python + Line bot: Building a Line bot from scratch and deploying to Heroku! | by Molly M | Medium](https://molly1024.medium.com/python-%E8%88%87-line-bot-%E5%BE%9E%E9%A0%AD%E9%96%8B%E5%A7%8B%E5%BB%BA%E7%AB%8B%E4%B8%80%E5%80%8B-line-%E6%A9%9F%E5%99%A8%E4%BA%BA-%E9%83%A8%E7%BD%B2%E5%88%B0-heroku-51512b04cb7b)

## Contributions

Pull requests and issue reports are welcome to help improve this project.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.