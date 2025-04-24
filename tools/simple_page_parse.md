# 🌐 HWS Web Scraper Plugin

> This plugin allows you to extract html element values in webpages.  

---

## 🔧 How It Works

1. **Input a URL**  
   The plugin fetches the webpage using the provided URL.

2. **Parse element text from HTML**  
   It extracts html element content using BeautifulSoup.
```python
soup = BeautifulSoup(resp.text, 'html.parser')
element_tag = "html script#__NEXT_DATA__" # use jquery selector
current_element = soup.select_one(element_tag)
```

3. **Specify a JSON path**

   if element content text is a json body, you should give 'paths' variable in the Coze Plugin Params.  
   Provide a `#`-separated path to locate the desired value inside the JSON structure.
```python
target_value = json_data
for key in paths.split("#"):
   if key.isdigit() and len(key) < 6:
      key = int(key)
   target_value = target_value[key]
return str(target_value)
```
   if it is not a json body, the Plugin will return element content text directly.

4. **Return the result**  
   The plugin returns the value found at that path.  
   Note: if the element content is text, you can pass the text to Coze LLM to further analyze.

## try on coze workflow
![](../_images/simple_page_parse_demo.png)

---

## 📥 Example Input

```json
{
  "http_url": "https://wise.com/us/currency-converter/usd-to-cny-rate",
  "element_tag": "html script#__NEXT_DATA__",
  "paths": "props#pageProps#model#rate#value"
}
```

## 📤 Example Output
```json
{
  "data": "7.25725"
}
```

## 🧭 Path Syntax
Use # to navigate through keys and array indexes:


|**Path**|**Meaning**|
|---|---|
|data#products#0#price|json['data']['products'][0]['price']|
|a#b#1#c|json['a']['b'][1]['c']|
Note: Array indexes must be digits (e.g., "0", "1").

## ✅ Requirements

- requests, 
- beautifulsoup4