# speech-to-text-line-bot 

## 起源

總是有很多時刻沒辦法打開手機音量去聆聽那些~~愛傳語音的人的~~語音訊息，或是不太愛打字的族群。所以如果有個可以自動讀取 Line 語音並將他轉成文字的話，就可以解決在某個場合上無法聆聽語音訊息的狀況，並可立即知道語音內容是什麼。~~不用再偷偷摸摸的到旁邊偷聽語音訊息了。~~

該 Line Bot 服務基於使用 `FastAPI` 配合 `SpeechRecognition` 來達到期望的目的。本來預期期望是使用 `Google Cloud Speech API` 來達成目標，但由於荷包不允許，所以改以另一種解決方案來處理這個問題。

## 功能

利用 Line ，向該 Line@ Service 傳送語音訊息，該 Service 將會將此語音訊息轉換為文字，並將文字結果回傳給使用者。

## 安裝

請更改 `Config.ini` 內 Token 資訊後喚起 `Uvicorn` or 使用 `Docker` 進行發佈。

## DEMO

![DEMO](https://user-images.githubusercontent.com/16682813/195927328-540c7771-8045-47fd-a7e1-b36a5ff1034d.gif)
