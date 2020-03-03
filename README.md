# TrashBot
<img src="https://user-images.githubusercontent.com/45473923/59561834-b1c0b480-905f-11e9-84ee-f94e76e47afc.jpg" width=45%> <img src="https://user-images.githubusercontent.com/45473923/59561968-42e45b00-9061-11e9-8ad9-93dd3e409b4a.jpg" width=45%>    

## [DemoMovie1] Google Homeを使ったゴミ箱の操作  
[![IMAGE ALT TEXT HERE](http://img.youtube.com/vi/Yut2F3ufk2o/0.jpg)](http://www.youtube.com/watch?v=Yut2F3ufk2o)  
## システム
GoogleHome→ IFTTT→ slack→ ROS→ RaspberryPi→ Arduino

## 環境
Linux ubuntu16.04  
ROS kinetic  
RaspberryPi B  [OS:UbuntuMATE]  
* Slackアプリで、オリジナルのslackbotを作成
* IFTTTでMy Appletを作成し、GoogleHomeとslackをIFTTT経由で接続
* 下記のwebページを参考にPythonのslackbotライブラリをubuntuにインストール
* 実行ファイルは、/usr/local/lib/python2.7/dist-packages/slackbotの中にrun.pyを作成  
(vimの保存コマンドは、:w !sudo tee %)
* /usr/local/lib/python2.7/dist-packages/slackbotの中にslackbot_settings.pyを作成し、  
オリジナルのslackbotのAPIトークンを書き込む
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

Autumn-Color.com「Pythonでファイルをオープンしてから２次元配列で返すモジュール」(2017年1月5日更新)  
https://www.autumn-color.com/archives/509  
