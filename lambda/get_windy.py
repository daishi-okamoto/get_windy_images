from datetime import datetime, timedelta
from selenium import webdriver
# from PIL import Image, ImageFilter
# import chromedriver_binary
import boto3
import config
import time


class ChromeDriver():
    """
    ChromeDriver Class
    """
    def __init__(self):
        pass

    def open(self, lambda_flg: bool):
        """
        Open Chrome driver
        """
        # Chromeオプションを設定する
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-gpu")
        # options.add_argument("--window-size=1000x1000")
        options.add_argument("--window-size=1704x1078")
        options.add_argument("--disable-application-cache")
        options.add_argument("--disable-infobars")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--no-sandbox")
        options.add_argument("--hide-scrollbars")
        options.add_argument("--enable-logging")
        options.add_argument("--log-level=0")
        options.add_argument("--v=99")
        options.add_argument("--single-process")
        options.add_argument("--ignore-certificate-errors")

        if lambda_flg:
            # chrome driverを読み込む
            options.binary_location = "/opt/headless-chromium"
            driver = webdriver.Chrome("/opt/chromedriver", options=options)
        else:
            driver = webdriver.Chrome(options=options)

        self.driver = driver

    def close(self):
        """
        Close Chrome driver
        """
        self.driver.close()


class Windy():
    """
    Windy Class
    """
    def __init__(
        self,
        area: str,
        overlay: str,
        latitude: float,
        longitude: float,
        zoom: int
    ):
        """
        初期化処理。
        area: エリア名
        overlay: 天候のタイプ
        latitude: 緯度
        longitude: 経度
        zoom: ズーム(3-18) 8くらいが使いやすい
        """
        self.area = area
        self.overlay = overlay
        self.latitude = latitude
        self.longitude = longitude
        self.zoom = zoom
        self.url = "https://www.windy.com/?{yyyy}-{mm}-{dd}-{hh},{overlay},{lat},{lon},{zoom},p:off"
        # self.url = "https://www.windy.com/ja/?{yyyy}-{mm}-{dd}-{hh},{overlay},{lat},{lon},{zoom},p:off"

    def set_date(self, date: datetime):
        """
        日時セット
        """
        self.yyyy = date.year
        self.mm = "{:02}".format(date.month)
        self.dd = "{:02}".format(date.day)
        self.hh = "{:02}".format(date.hour)

        url_date = date - timedelta(hours=9)
        self.url_yyyy = str(url_date.year)
        self.url_mm = "{:02}".format(url_date.month)
        self.url_dd = "{:02}".format(url_date.day)
        self.url_hh = "{:02}".format(url_date.hour)

    def save_images(self, chrome, options=None):
        """
        画像データの保存
        """
        # URLをフォーマット
        format_url = self.url.format(
            yyyy=self.url_yyyy,
            mm=self.url_mm,
            dd=self.url_dd,
            hh=self.url_hh,
            overlay=self.overlay,
            lat=self.latitude,
            lon=self.longitude,
            zoom=self.zoom
        )

        # Chromeでフォーマット済みURLを開く(headless)
        chrome.driver.get(format_url)

        time.sleep(5)
        # Chromeで開いたページのスクリーンショットをtmpディレクトリに保存する
        chrome.driver.save_screenshot(
            f"{config.TMP_DIR}/{self.filename}")

    def create_filename(self):
        """
        保存用のファイル名文字列生成
        """
        self.filename = f"windy_{self.overlay}_{self.area}_{self.yyyy}"\
            f"{self.mm}{self.dd}{self.hh}.png"

    # def resize_image(self):
        #
        # 不要になりそう。
        #
        # """
        # 画像ファイルのリサイズ
        # """
        # image = Image.open(f"{config.TMP_DIR}/{self.filename}")
        # resized_image = image.resize((852, 539), Image.LANCZOS)
        # resized_image.save(f"{config.TMP_DIR}/{self.filename}")

    def upload_s3(self, **kwargs):
        """
        S3アップロード
        """
        s3 = boto3.resource("s3")

        save_dir = f"{config.S3FOLDER_WINDY}"\
            f"{self.overlay}/{self.area}/"\
            f"{self.yyyy}/{self.mm}/{self.dd}/"\

        s3.meta.client.upload_file(
            Filename=f"{config.TMP_DIR}/{self.filename}",
            Bucket=config.S3BUCKET_WINDY,
            Key=save_dir + self.filename,
            ExtraArgs=kwargs
        )


def lambda_handler(event, context):
    """
    lambdaイベントハンドラ関数
    """
    main(lambda_flg=True)


def main(lambda_flg=False):
    """
    メイン処理
    """
    # ChromeDriver接続
    chrome = ChromeDriver()
    chrome.open(lambda_flg)

    for area in config.WINDY_AREAS:
        if area["enable"] is False:
            continue
        for overlay in config.WINDY_OVERLAY:
            windy = Windy(
                area["area"],
                overlay,
                area["lat"],
                area["lon"],
                area["zoom"]
            )

            date = get_date()
            windy.set_date(date)
            windy.create_filename()

            windy.save_images(chrome)

            windy.upload_s3(ACL="public-read")

    chrome.close()


def get_date(UTC=False) -> datetime:
    """
    日付取得関数
    """
    if UTC:
        date = datetime.now() + timedelta(hours=9)
    else:
        date = datetime.now()

    return date


if __name__ == "__main__":
    main()
