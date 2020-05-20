# TrashBot
<img src="https://user-images.githubusercontent.com/45473923/77515062-3f68e480-6ebb-11ea-9940-b3d9d1c65b5c.jpg" width=45%> <img src="https://user-images.githubusercontent.com/45473923/77515204-78a15480-6ebb-11ea-8d40-defbb504d8e0.jpg" width=45%>  

<br>

### Circuit and computer(Jetson TX2)
<img src="https://user-images.githubusercontent.com/45473923/78958526-374bae80-7b23-11ea-9ee6-f56fe79a21de.jpg" width=30%> <img src="https://user-images.githubusercontent.com/45473923/78962638-af1fd600-7b2f-11ea-9034-4c745c0b5cde.jpg" width=30%>

<br>

### Smart Home Environment
<img src="https://user-images.githubusercontent.com/45473923/78908121-9aeec100-7abc-11ea-971d-9fd3ff177858.png" width=70%>

<br>

### voice control
<img src="https://user-images.githubusercontent.com/45473923/78961691-4f283000-7b2d-11ea-8d56-19393890b61a.PNG" width=50%>

<br>

## System OverView
<img src="https://user-images.githubusercontent.com/45473923/78907860-39c6ed80-7abc-11ea-8537-0f150055defa.PNG" width=70%>

<br>

# Semicircle Area
<img src="https://user-images.githubusercontent.com/45473923/78907355-8bbb4380-7abb-11ea-99a8-8bd49760954a.png" width=45%>

<br>

## Demo Movie  
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
