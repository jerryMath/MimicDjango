import socket
import time
import pymysql
from jinja2 import Template


def f1(request):
    f = open('index.html', 'rb')
    data = f.read()
    f.close()
    return data


def f2(request):
    f = open('article.html', 'r', encoding='utf-8')
    data = f.read()
    f.close()

    ctime = time.time()
    data = data.replace("@@sw@@", str(ctime))

    return bytes(data, encoding='utf-8')


def f3(request):
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='jerryjerry', db='db666')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    cursor.execute("select id, first_name, last_name, age from employee_table")
    user_list = cursor.fetchall()
    cursor.close()
    conn.close()
    """
    [
        {'id': 101, 'first_name': 'John', 'last_name': 'Dive', 'age': 23}, 
        {'id': 102, 'first_name': 'Lebron', 'last_name': 'James', 'age': 33}
    ]

    <tr>
        <th>1</th>
        <th>@@sw@@</th>
        <th>root@gmail.com</th>
        <th>root@gmail.com</th>
    </tr>
    """
    content_list = []
    for row in user_list:
        tp = f"<tr><th>{row['id']}</th><th>{row['first_name']}</th><th>{row['last_name']}</th><th>{row['age']}</th></tr>"
        content_list.append(tp)
    content = "".join(content_list)

    f = open('userlist.html', 'r', encoding='utf-8')
    template = f.read()
    f.close()

    # rendering
    data = template.replace('@@content@@', content)
    return bytes(data, encoding='utf-8')


def f4(request):
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='jerryjerry', db='db666')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    cursor.execute("select id, first_name, last_name, age from employee_table")
    user_list = cursor.fetchall()
    cursor.close()
    conn.close()

    f = open('hostlist.html', 'r', encoding='utf-8')
    template = f.read()
    f.close()

    template = Template(template)
    data = template.render(user_list=user_list)
    return data.encode('utf-8')


routers = [
    ('/xxx', f1),
    ('/ooo', f2),
    ('/userlist.htm', f3),
    ('/host.htm', f4),
]


def run():
    sock = socket.socket()
    sock.bind(('127.0.0.1', 8080))
    sock.listen(5)

    while True:
        conn, addr = sock.accept()  
        data = conn.recv(8096)
        data = str(data, encoding='utf-8')
        headers, bodies = data.split('\r\n\r\n')
        temp_list = headers.split('\r\n')
        method, url, protocal = temp_list[0].split(' ')
        conn.send(b"HTTP/1.1 200 ok\r\n\r\n")

        func_name = None
        for item in routers:
            if item[0] == url:
                func_name = item[1]
                break

        if func_name is not None:
            response = func_name(data)
        else:
            response = b"404"

        conn.send(response)
        conn.close()


if __name__ == '__main__':
    run()