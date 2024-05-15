from flask import Flask, redirect
import subprocess
import json
import ssl


cdn_domain=None

app = Flask('steam-cdn-redir')

#node_path='C:\\Program Files\\nodejs\\node.exe'
node_path='node'
get_token_js_path=r"node_modules\steam-user\examples\returntoken.js"
# 启动Node.js服务器
node_process = subprocess.Popen(
    [
        node_path,
        get_token_js_path,
    ],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True,
)


# 等待Node.js服务器登录完成
def wait_for_login(username='username',password='password'):
    # 构建要发送的数据
    data = json.dumps({"username": username, "password": password})

    # 发送数据到Node.js服务器
    node_process.stdin.write(data + "\n")
    node_process.stdin.flush()

    while True:
        line = node_process.stdout.readline()
        if "Steam login successful. Ready to accept input." in line:
            print(line.strip())
            break
        elif "Steam login failed" in line:
            print(line.strip())
            exit(1)  # 如果登录失败，则退出
        else:
            print(line.strip())


# 等待Steam登录成功
# 这里传入的用户名密码并没有被使用，js实际上是匿名登录，以防之后出问题所以进行预留
wait_for_login('username','password')

def call_node_function(appid, depotid, vhost):
    # 构建要发送的数据
    data = json.dumps({"appid": appid, "depotid": depotid, "vhost": vhost})

    # 发送数据到Node.js服务器
    node_process.stdin.write(data + "\n")
    node_process.stdin.flush()

    # 读取Node.js服务器的响应
    result = node_process.stdout.readline()
    return json.loads(result)

@app.route('/<path:subpath>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def redirect_to_another_url(subpath):
    try:
        depotID = int(subpath.split('/')[1])
        #这里的appID经测试可以是任意的，不影响token的获取和下载
        appID=553850
        token = call_node_function(appID, depotID, cdn_domain)["token"]
    except:
        token=''
    subpath=subpath+token
    target_url = f"http://{cdn_domain}/{subpath}"
    print(target_url)
    return redirect(target_url, code=302)

def run(crt=None,key=None,password='1234',debug=False):
    if cdn_domain is None:
        raise ValueError("未指定CDN")
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(crt, keyfile=key, password=password)
    app.debug=debug
    app.run(host='127.0.0.1', port=443, ssl_context=context)

if __name__ == '__main__':
    #run(r'E:\Softwares\caddyv2\ca1.crt', r'E:\Softwares\caddyv2\ca1.key')
    run(r'ca.crt', r'ca.key','1234')
    #app.run(host='127.0.0.1', port=443, ssl_context=(r'E:\Softwares\caddyv2\ca1.crt', r'E:\Softwares\caddyv2\ca1.key'))
