import requests
import json
def mathocr(file_path: str, uat: str = "") -> str:
    api_url = "https://server.simpletex.cn/api/latex_ocr"
    data = {}
    header = {"token": uat}
    file = [("file", (file_path, open(file_path, "rb")))]
    res = requests.post(api_url, files=file, data=data, headers=header)
    res_json = res.json()
    assert res_json["status"] == True, "Failed to get MathOCR result"

    return json.loads(res.text)["res"]["latex"]


