import socket


def f1(request):
    f = open('index.html', 'rb')
    data = f.read()
    f.close()
    return data


def f2(request):
    f = open('page.html', 'rb')
    data = f.read()
    f.close()
    return data


routers = [
    ('/xxx', f1),
    ('/ooo', f2)
]


def run():
    sock = socket.socket()
    sock.bind(('127.0.0.1', 8080))
    sock.listen(5)

    while True:
        conn, _ = sock.accept()

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
