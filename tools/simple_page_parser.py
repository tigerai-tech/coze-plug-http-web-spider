import json
import requests
from bs4 import BeautifulSoup
from dataclasses import dataclass

# ===== 数据类定义 =====
@dataclass
class Input:
    http_url: str
    paths: str

@dataclass
class Args:
    input: Input

@dataclass
class Output:
    data: str

# ===== 页面抓取并解析 JSON =====
def download_webpage_and_parse_json(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
    }
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, 'html.parser')
    script_tag = soup.find('script', id="__NEXT_DATA__")
    if not script_tag:
        raise Exception("未找到 __NEXT_DATA__ 脚本标签")

    return json.loads(script_tag.string)

# ===== 按路径提取数据 =====
def fetch_data_from_webpage_json(json_data, paths):
    # todo : check json data formation , choose your correct target value paths
    print(json_data)
    target_value = json_data
    for key in paths.split("#"):
        if key.isdigit() and len(key) < 6:
            key = int(key)
        target_value = target_value[key]
    return str(target_value)

# ===== 主处理函数 =====
def handler(args: Args) -> Output:
    url = args.input.http_url
    paths = args.input.paths
    json_data = download_webpage_and_parse_json(url)
    target_value = fetch_data_from_webpage_json(json_data, paths)
    return Output(data=target_value)

# ===== 测试运行 =====
if __name__ == "__main__":
    url = "https://wise.com/us/currency-converter/usd-to-cny-rate"
    paths = "props#pageProps#model#rate#value"
    args = Args(input=Input(http_url=url, paths=paths))
    print(handler(args))