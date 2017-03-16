from re import sub
from time import sleep
import sys

class Player(object):
    '''Rappresentazione dei giocatori ad oggetti. Conterrà il nome del giocatore e delle presenze'''
    def __init__(self, name, presenze):
        self.name = name
        self.presenze = presenze
    def __str__(self):
        return self.name + "=" + str(self.presenze)
    def incrementaPresenza(self):
        '''Incrementa di uno le presenze del giocatore'''
        self.presenze += 1
    def getPresenze(self):
        '''Ritorna le presenze'''
        return self.presenze
    def getName(self):
        '''Ritorna il nome'''
        return self.name


def openFileAndPrint(name):
    '''Tenta di aprire il file specificato su name'''
    try:
        with open(name+'.txt') as f:
            tmp = f.read() #decodifica il file
            tmp = sub('[^a-zA-Z\u00C0-\u00F6\u00F8-\u00FF\n\0-9\=]', ' ', tmp) #regex per togliere ogni caratteraccio
    except:
        print("Impossibile aprire il file " + name) #Dovesse non leggerlo bene, cattura l'eccezione e manda l'errore
        SystemExit
    theIndex = tmp.find("Presenze aggiornate al ") # Dovesse essere già stato modificato, cerca la prima occorrenza di "Presenze aggiornate al "
    if theIndex >= 0: # Se c'è una ricorrenza...
        tmp = tmp[:theIndex] # Allora la tolgo
    return tmp # Ritorno la stringa decodificata e pulita

def getPlayerObjects(presenzeLst, playersLst):
    '''Metodo che prende in input la lista delle presenze e dei giocatori e ritorna una lista dei giocatori fatta ad oggetti'''
    lstToReturn = []
    for i in range(len(presenzeLst)):
        lstToReturn.append(Player(playersLst[i], presenzeLst[i]))
    return lstToReturn

def createPresenceOnlyLst(varToUse):
    ''' Funzione che ritorna una lista con le presenze dei giocatori'''
    presenzeLst = sub('[^0-9\n]', '', varToUse) # Mi preparo la stringa per estrapolare solo i numeri di presenze
    presenzeLst = presenzeLst.split('\n') # Mi creo la lista con solo le presenze.
    presenzeLst.remove('') # Mi scappa uno spazio vuoot. Non so perché. Quindi lo rimuovo
    for i in range(len(presenzeLst)):
        presenzeLst[i] = int(presenzeLst[i]) #Converto ad integer l'elemento i-simo
    return presenzeLst

def createNamesOnlyLst(varToUse):
    '''Funzione che ritorna una lista con il nome dei giocatori '''
    playersLst = sub('[^a-zA-Z\u00C0-\u00F6\u00F8-\u00FF\n]', '', varToUse) # Mi preparo la stringa per estrapolare solo i nomi
    playersLst = playersLst.split('\n') # Mi creo la lista con solo le persone.
    playersLst.remove('') # Mi scappa uno spazio vuoot. Non so perché. Quindi lo rimuovo
    return playersLst

def increasePresences(playersLst, convocati):
    '''Funzione che prende in input la lista dei giocatori (O.O.) e dei convocati, incrementa le presenze e ritorna la lista dei giocatori moddata'''
    for i in range(len(convocati)):
        theIndex = search(playersLst, convocati[i]) # Cerca la corrispondenza del giocatore i-simo
        if theIndex >= 0: # Se l'ho trovata...
            playersLst[theIndex].incrementaPresenza() # ... aumento le presenze di quel giocatore
    return playersLst # Fine funzione. Ritorno la lista aggiornata

def search(playersLst, player):
    '''Funzione che prende in input la lista dei giocatori (O.O.) ed il giocatore che si intende cercare'''
    for i in range(len(playersLst)):
        if player == playersLst[i].getName(): # Se il giocatore che mi interessa è uguale all'i-simo giocatore in analisi...
            return i # Ne ritorno l'indice
    return -1 # Se non trovo corrispondenza, torno invece -1

def finalize(playersOfTheTeam):
    '''Funzione che finalizza tutti i cambiamenti fatti in un nuovo file'''
    import time
    tempo = time.strftime("%d %b %Y") # Setto la data in una variabile
    with open('Presenze aggiornate al ' + tempo + '.txt', 'w') as f:
        # Apro un nuovo file che si chiamerà "Presenze aggiornate al <tempo>.txt" e...
        for i in range(len(playersOfTheTeam)):
            #...salvo ogni giocatore con la nuova presenza
            f.write(playersOfTheTeam[i].getName() +"="+str(playersOfTheTeam[i].getPresenze())+"\n")
        #Metto infine, in fondo al file, una didascalia per segnare l'ultima data di aggiornamento
        f.write('Presenze aggiornate al ' + tempo)
    print("Finito!")

def checkTraguardi(playersOfTheTeam):
    '''Metodo che controlla se i giocatori hanno raggiunto un multiplo di 50 come presenze'''
    for i in range(len(playersOfTheTeam)):
        if playersOfTheTeam[i].getPresenze() % 50 == 0: # Se un giocatore ha raggiunto un multiplo di 50 come presenze...
            print(playersOfTheTeam[i].getName() + " ha raggiunto " + playersOfTheTeam[i].getPresenze() + " presenze!")
            #Lo stampo

print("Benvenuto al conta presenze!")
sleep(0.5)
name = input("Mi dici per favore come si chiama il file delle presenze, senza l'estensione?\n")
openedFile = openFileAndPrint(name) # Il file in todo
presenzeLst = createPresenceOnlyLst(openedFile[:]) # La var con solo il numero di presenze dei giocatori
playersLst = createNamesOnlyLst(openedFile[:]) # La var con solo il nome dei giocatori
# Ho scelto di fare due liste perché tanto avranno sempre la stessa lunghezza

playersOfTheTeam = getPlayerObjects(presenzeLst, playersLst) # Creo la lista O.O. dei giocatori

convocati = sys.argv[1:] # Salvo in una lista tutti i giocatori passati da CLI
increasePresences(playersOfTheTeam, convocati) # Incremento le presenze...
checkTraguardi(playersOfTheTeam) # ... Guardo se qualcuno ha raggiunto un multiplo di 50 come presenze...
finalize(playersOfTheTeam) #... e salvo il file
