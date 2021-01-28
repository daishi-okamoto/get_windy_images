# README
windy.com が提供するリアルタイム天気予報サービスの画像を取得し、AWS Lambdaを使いS3にアーカイブする機能を提供する。

## 前提条件
AWS Lambdaで実行するのを想定して作成している。
また、Lambda連携はserverless frameworkを使用を前提としている。

## セットアップ
以下の手順は、EC2を使ってセットアップする手順とする。

1. EC2インスタンス(Linux)にSSHログインし、git cloneする。
```
$ cd <任意の展開元ディレクトリ>
$ git clone git@github.com:daishi-okamoto/get_windy.git
```

2. Lambda Layerのセットアップ
```
$ cd <展開元ディレクトリ>/get_windy_images/selenium-layer

Lambdaロールを設定する。(S3 write権限)
$ vi serverless.yml
provider.role = <Lambda Role>

$ sls deploy
deploy中にErrorが発生しないことを確認。
```

3. Lambda関数のセットアップ
```
$ cd <展開元ディレクトリ>/get_windy_images/lambda

S3情報と取得対象の設定を行う。
# TODO: 環境変数化したい。
$ vi config.py
S3BUCKET_WINDY = <S3バケット名>
S3FOLDER_WINDY = <S3ディレクトリ名>
WINDY_OVERLAY = <Windyの取得対象Overlay>
WINDY_AREAS = <※Windyの取得対象地域>
※取得対象地域はenable = Trueの地域。

$ sls deploy
deploy中にErrorが発生しないことを確認。
```

4. 対象のlambda関数を呼び出す設定を行う。
* (例)EventBridgeでルールを作成する。

セットアップ完了

## おまけ(個人用メモ)
Linuxサーバ上でChromeを使う場合のChromeとChromeDriverのインストール方法は以下を参考に。

1. Google Chromeをインストールする。
```
$ sudo yum -y install https://dl.google.com/linux/direct/google-chrome-stable_current_x86_64.rpm
$ sudo yum list installed | grep google-chrome
google-chrome-stable.x86_64        88.0.4324.96-1                    @google-chrome
```

2. ChromeDriverをインストールする。(chromeと同じバージョンのものをインストール)
```
$ wget https://chromedriver.storage.googleapis.com/88.0.4324.96/chromedriver_linux64.zip
$ unzip https://chromedriver.storage.googleapis.com/88.0.4324.96/chromedriver_linux64.zip
$ mv chromedriver /usr/local/bin/
$ rm -f https://chromedriver.storage.googleapis.com/88.0.4324.96/chromedriver_linux64.zip
```

## 参考
### Windy
https://www.windy.com
### serverless setup
https://blog.ikedaosushi.com/entry/2018/12/22/231421
