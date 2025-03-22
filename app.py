import json
import os
import school_api_lib
import urllib.request
import urllib.error
from urllib.parse import urljoin
import auth

auth.auth() #完成认证

def serve_file(environ, start_response, file_path):
    # 确保文件存在
    if os.path.isfile(file_path):
        try:
            with open(file_path, 'rb') as f:
                file_content = f.read()
            
            # 确定文件类型
            content_type = 'application/octet-stream'  # 默认为二进制文件类型
            if file_path.endswith('.html'):
                content_type = 'text/html'
            elif file_path.endswith('.txt'):
                content_type = 'text/plain'
            elif file_path.endswith('.json'):
                content_type = 'application/json'
            
            status = '200 OK'
            headers = [('Content-type', content_type)]
            start_response(status, headers)
            return [file_content]
        
        except Exception as e:
            # 文件读取失败，返回错误信息
            status = '500 Internal Server Error'
            headers = [('Content-type', 'application/json')]
            start_response(status, headers)
            return [json.dumps({"status": "error", "message": str(e)}).encode('utf-8')]
    
    # 如果文件不存在，返回 404 错误
    status = '404 Not Found'
    headers = [('Content-type', 'text/plain')]
    start_response(status, headers)
    return [b"Not Found"]

def simple_app(environ, start_response):
    # 获取脚本所在目录
    base_dir = os.path.dirname(os.path.abspath(__file__))  # 获取当前脚本所在的目录

    # 获取请求路径
    path = environ.get('PATH_INFO', '')
    
    # 如果请求的是根目录（/），返回 index.html 文件
    if path == '/':
        file_path = os.path.join(base_dir, 'index.html')
        return serve_file(environ, start_response, file_path)
    
    # 如果请求的是其他文件，拼接文件路径
    safe_path = os.path.normpath(path.lstrip('/'))  # 移除路径中的多余斜杠，并规范化路径
    file_path = os.path.join(base_dir, safe_path)  # 拼接脚本所在目录和请求的文件路径
    
    # 调用 serve_file 函数来返回文件
    return serve_file(environ, start_response, file_path)

def uinlookup_handler(environ):
    # 处理 /api/uinlookup 请求
    if environ['REQUEST_METHOD'] == 'POST':
        try:
            # 获取请求体内容（POST 数据）
            content_length = int(environ.get('CONTENT_LENGTH', 0))
            post_data = environ['wsgi.input'].read(content_length) if content_length > 0 else b""
            
            # 尝试将内容解析为JSON
            data = json.loads(post_data.decode('utf-8'))
            
            # 从JSON中获取字段（如：'uin'）
            uin = data.get('uin', None)
            
            if uin:
                # 如果提供了uin参数，调用51校园API来获取数据
                user_info = school_api_lib.get_user_info(school_api_lib.lookup_card_id_by_account(uin))
                response = user_info
            else:
                # 如果没有提供uin参数，返回错误
                response = {
                    "status": "error",
                    "message": "UIN parameter is missing"
                }
        except Exception as e:
            # 异常处理
            response = {
                "status": "error",
                "message": str(e)
            }
    else:
        # 如果不是POST请求
        response = {
            "status": "error",
            "message": "Invalid request method"
        }
    
    return response


def handle_api_request(environ, start_response):
    # 获取请求路径
    path = environ.get('PATH_INFO', '')
    
    # 根据路径做不同的处理
    if path.startswith('/api/'):
        if path == '/api/uinlookup':
            # 获取响应内容
            response = uinlookup_handler(environ)
            
            # 设置响应头
            status = '200 OK'
            headers = [('Content-type', 'application/json'),
                       ('Access-Control-Allow-Origin', '*'), 
                       ('Access-Control-Allow-Methods', 'GET, POST, OPTIONS'),  
                       ('Access-Control-Allow-Headers', 'Content-Type')]
            start_response(status, headers)
            
            # 返回 JSON 响应
            return [json.dumps(response,ensure_ascii=False).encode('utf-8')]
        
        # 如果路径是 /api/*，并且没有匹配到具体的 handler，可以返回一个简单的API响应
        status = '200 OK'
        headers = [('Content-type', 'text/plain')]
        start_response(status, headers)
        return [f"API path requested: {path}".encode('utf-8')]
    
    # 如果路径不匹配API，返回404
    status = '404 Not Found'
    headers = [('Content-type', 'text/plain')]
    start_response(status, headers)
    return [b"Not Found"]

def forward_uimages_request(environ, start_response):
    # 获取请求路径
    path = environ.get('PATH_INFO', '')
    
    if path.startswith('/uimages/'):
        # 构建转发的 URL
        new_url = urljoin("http://iapis.51school.com", path)
        
        # 移除 'Referer' 头
        headers = {key: value for key, value in environ.items() if key.startswith('HTTP_')}
        headers.pop('HTTP_REFERER', None)  # 删除 Referer 头
        
        # 转发请求
        try:
            req = urllib.request.Request(new_url, headers=headers)
            with urllib.request.urlopen(req) as response:
                # 获取响应内容
                response_content = response.read()
                status = f"{response.status} {response.reason}"
                headers = [('Content-type', response.getheader('Content-Type', 'application/octet-stream'))]
                start_response(status, headers)
                return [response_content]
        except urllib.error.URLError as e:
            # 如果请求出错，返回错误信息
            status = '500 Internal Server Error'
            headers = [('Content-type', 'application/json')]
            start_response(status, headers)
            return [json.dumps({"status": "error", "message": str(e)}).encode('utf-8')]
    
    # 如果路径不以 `/uimages/` 开头，返回 404 错误
    status = '404 Not Found'
    headers = [('Content-type', 'text/plain')]
    start_response(status, headers)
    return [b"Not Found"]

def app(environ, start_response):
    # 如果路径是 /uimages/，转发到 iapis.51school.com
    if environ.get('PATH_INFO', '').startswith('/uimages/'):
        return forward_uimages_request(environ, start_response)

    # 判断路径是否以/api/开头，如果是，调用handle_api_request函数
    if environ.get('PATH_INFO', '').startswith('/api/'):
        return handle_api_request(environ, start_response)
    
    # 如果请求的是根目录（/），返回 index.html 文件
    path = environ.get('PATH_INFO', '')
    if path == '/':
        base_dir = os.path.dirname(os.path.abspath(__file__))  # 获取当前脚本所在的目录
        file_path = os.path.join(base_dir, 'index.html')
        return serve_file(environ, start_response, file_path)
    
    # 默认返回简单的"Hello, World!"响应
    status = '200 OK'
    headers = [('Content-type', 'text/plain')]
    start_response(status, headers)
    return [b"51Neo-V2 Backend"]

if __name__ == "__main__":
    from wsgiref.simple_server import make_server
    # 创建一个WSGI服务器，绑定到8000端口
    httpd = make_server('', 8000, app)
    print("正在启动中...")
    print(r"""______     _                           
/\  ___\  /' \                          
\ \ \__/ /\_, \    ___      __    ___   
 \ \___``\/_/\ \ /' _ `\  /'__`\ / __`\ 
  \/\ \L\ \ \ \ \/\ \/\ \/\  __//\ \ \ \
   \ \____/  \ \_\ \_\ \_\ \____\ \____/
    \/___/    \/_/\/_/\/_/\/____/\/___/ 
欢迎使用51Neo          
""")
    httpd.serve_forever()
