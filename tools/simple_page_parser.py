import json
import requests
from bs4 import BeautifulSoup
from dataclasses import dataclass

# ===== 数据类定义 =====
@dataclass
class Input:
    http_url: str
    paths: str
    element_tag: str

@dataclass
class Args:
    input: Input

@dataclass
class Output:
    data: str

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


# ===== 页面抓取并解析 JSON =====
def download_webpage_and_parse_json(url, element_tag, paths):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
    }
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, 'html.parser')
    # 使用jquery 选择器，选中tag内容
    current_element = soup.select_one(element_tag)
    if paths:
        try:
            # 如果内容符合 JSON 格式，则尝试解析
            json_data = json.loads(current_element.string)
            return fetch_data_from_webpage_json(json_data, paths)
        except (json.JSONDecodeError, TypeError):
            # 如果解析失败，则返回 None 或者处理其他逻辑
            print('content is not formatted in json')
    else:
        return current_element.string


# ===== 主处理函数 =====
def handler(args: Args) -> Output:
    url = args.input.http_url
    paths = args.input.paths
    element_tag = args.input.element_tag
    parsed_value = download_webpage_and_parse_json(url, element_tag, paths)
    return Output(data=parsed_value)

# ===== 测试运行 =====
if __name__ == "__main__":
    url = "https://wise.com/us/currency-converter/usd-to-cny-rate"
    paths = "props#pageProps#model#rate#value"
    element_tag = "html script#__NEXT_DATA__"
    args = Args(input=Input(http_url=url, paths=paths, element_tag=element_tag))
    print(handler(args))