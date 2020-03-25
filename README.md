# TrashBot
<img src="https://user-images.githubusercontent.com/45473923/77515062-3f68e480-6ebb-11ea-9940-b3d9d1c65b5c.jpg" width=45%> <img src="https://user-images.githubusercontent.com/45473923/77515204-78a15480-6ebb-11ea-8d40-defbb504d8e0.jpg" width=45%>    

## [DemoMovie1] Google Homeを使ったゴミ箱の操作  
[![IMAGE ALT TEXT HERE](http://img.youtube.com/vi/xtzoYeqc3O0/0.jpg)](http://www.youtube.com/watch?v=xtzoYeqc3O0)  
## システム
GoogleHome→ IFTTT→ slack→ ROS→ RaspberryPi→ Arduino
## 環境
Linux ubuntu16.04  
ROS kinetic  
RaspberryPi B  [OS:UbuntuMATE]  
* Slackアプリで、オリジナルのslackbotを作成
* IFTTTでMy Appletを作成し、GoogleHomeとslackをIFTTT経由で接続
* 下記のwebページを参考にPythonのslackbotライブラリをubuntuにインストール
* ubuntuとRaspberryPiはssh接続で、rosserial(ROSの通信パッケージ)を使用してロボット側とPC側がデータを送受信





## 参考文献
「ROSではじめるロボットプログラミング」著者:小倉 崇  
## 参考webページ
Qiita「Slackにボットを設置する」(2017年6月10日更新)  
https://azriton.github.io/2016/12/17/Slack%E3%81%AB%E3%83%9C%E3%83%83%E3%83%88%E3%82%92%E8%A8%AD%E7%BD%AE%E3%81%99%E3%82%8B/   

Qiita「GoogleHome mini から IFTTT 経由で Slack に投稿してみた件」(2018年2月12日更新)
https://qiita.com/KSxRDevelop/items/4aff0f1856c0c200c1a0

Azriton's blog「PythonのslackbotライブラリでSlackボットを作る」(2016年12月17日更新)  
https://qiita.com/sukesuke/items/1ac92251def87357fdf6  
  [GitHub] https://github.com/lins05/slackbot   
