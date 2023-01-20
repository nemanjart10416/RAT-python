import socket,pyautogui

#HOST = '192.168.0.12'  # The server's hostname or IP address
HOST = '127.0.0.1'
PORT = 65432        # The port used by the server
buffer=1024

vnc=True

def posalji_poruku(poruka):
    sock.send(str(len(poruka)).encode("utf-8"))
    sock.recv(1)
    sock.send(str(poruka).encode("utf-8"))

def primi_poruku():
    duzina = int(sock.recv(buffer).decode("utf-8"))
    sock.send(b'1')
    poruka = sock.recv(duzina).decode("utf-8")
    return poruka

def konektuj():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))
    return client

sock=konektuj()

def live_view():
    odg=""
    try:
        pyautogui.screenshot('screenshot.png')
        f = open("screenshot.png", 'rb')
        bin = f.read()
        f.close()
        odg="ok"
    except Exception as e:
        odg=str(e)
        posalji_poruku(odg)
    if odg=="ok":
        posalji_poruku(odg)
        a=primi_poruku()
        bajtovi = bytes(bin)
        duzina = len(bajtovi)
        print(duzina)
        print("---------------------")
        posalji_poruku(str(duzina))
        a = primi_poruku()
        sock.send(bajtovi)
        ok = primi_poruku()





while vnc:
    live_view()


