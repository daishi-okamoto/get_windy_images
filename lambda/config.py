# S3
S3BUCKET_WINDY = ""
S3FOLDER_WINDY = ""

# WINDY
"""
Overlay
-------
wind: 風
clouds: 雲量
hclouds: 上層雲
mclouds: 中層雲
lclouds: 下層雲
temp: 気温
pressure: 気圧
rh: 湿度
fog: 霧
rain: 雨
thunder: 雷雨
snowAccu: 新雪
waves: 波
"""
WINDY_OVERLAY = ["clouds", "hclouds", "mclouds", "lclouds", "temp", "rh", "wind", "rain", "fog"]
WINDY_AREAS = [
    {
        "area": "Hokkaido-1",
        "lat": 43.799,
        "lon": 143.553,
        "zoom": 9,
        "enable": True,
    },
    {
        "area": "Hokkaido-2",
        "lat": 42.281,
        "lon": 141.949,
        "zoom": 9,
        "enable": False,
    },
    {
        "area": "Tohoku",
        "lat": 39.796,
        "lon": 141.053,
        "zoom": 8,
        "enable": False,
    },
    {
        "area": "Kanto",
        "lat": 36.273,
        "lon": 138.521,
        "zoom": 8,
        "enable": True,
    },
    {
        "area": "Kansai",
        "lat": 34.434,
        "lon": 135.341,
        "zoom": 8,
        "enable": False,
    },
    {
        "area": "Kyusyu",
        "lat": 32.863,
        "lon": 133.369,
        "zoom": 8,
        "enable": True,
    },
]

# TMP FILE
TMP_DIR = "/tmp"

# AUTH
WINDY_MAIL = ""
WINDY_PW = ""
