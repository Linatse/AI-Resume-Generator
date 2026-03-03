from flask import Flask, request, jsonify
import requests
import json
import os

# 初始化Flask应用
app = Flask(__name__)

# -------------------------- 配置项（替换成你的API Key） --------------------------
4530cfdb-9dae-429c-9f0b-8595595e7fa3
DOUBAO_API_URL = "https://api.doubao.com/v1/chat/completions"
# ------------------------------------------------------------------------

@app.route('/api/generate-resume', methods=['POST'])
def generate_resume():
    try:
        # 获取前端传入的参数
        data = request.get_json()
        personal_info = data.get('personal_info', '')
        job_requirement = data.get('job_requirement', '')

        # 校验参数
        if not personal_info or not job_requirement:
            return jsonify({"error": "个人背景和招聘需求不能为空"}), 400

        # 构造豆包API的请求参数
        prompt = f"""请根据以下个人背景信息和招聘需求，生成一份格式规范、贴合岗位的简历。
要求：
1. 简历结构包含：基本信息、核心能力、职场工作内容、项目/工作经历；
2. 严格基于用户提供的真实信息，不得编造任何内容；
3. 重点突出与招聘需求匹配的能力和经历，弱化无关信息；
4. 语言正式、简洁，符合职场简历规范；
5. 分点清晰，格式易读。

【个人背景信息】
{personal_info}

【招聘需求】
{job_requirement}"""

        # 调用豆包API
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {DOUBAO_API_KEY}"
        }

        payload = {
            "model": "doubao-pro",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7,
            "max_tokens": 2000
        }

        response = requests.post(DOUBAO_API_URL, headers=headers, data=json.dumps(payload))
        response.raise_for_status()
        result = response.json()
        resume_content = result['choices'][0]['message']['content']

        return jsonify({"resume": resume_content})

    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"API调用失败：{str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": f"系统错误：{str(e)}"}), 500

# Vercel原生适配（无需vercel-wsgi）
application = app  # Vercel会自动识别application变量作为WSGI入口

# 本地运行入口
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
