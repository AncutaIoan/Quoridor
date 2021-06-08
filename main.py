import time

import pygame, sys

ADANCIME_MAX = 1

tip_joc=''
tups=[]

def elem_identice(lista):
    if (all(elem == lista[0] for elem in lista[1:])):
        return lista[0] if lista[0] != Joc.GOL else False
    return False


class Celula:
    # coordonatele nodurilor ()
    grosimeZid = 11  # numar impar
    fundalCelula = (255, 255, 255)
    culoareLinii = (0, 0, 0)
    afisImagini = True

    def __init__(self, left, top, w, h, display, lin, col):
        self.dreptunghi = pygame.Rect(left, top, w, h)
        self.display = display
        self.zid = [None, None, None, None]
        # zidurile vor fi pe pozitiile 0-sus, 1-dreapta, 2-jos, 3-stanga
        self.cod = 0
        if lin > 0:
            self.zid[0] = pygame.Rect(left, top - 1 - self.__class__.grosimeZid // 2, w, self.__class__.grosimeZid)
        else:
            self.cod += 2 ** 0
        if col < 9 - 1:
            self.zid[1] = pygame.Rect(left + w - self.__class__.grosimeZid // 2, top, self.__class__.grosimeZid, h)
        else:
            self.cod += 2 ** 1
        if lin < 9 - 1:
            self.zid[2] = pygame.Rect(left, top + h - self.__class__.grosimeZid // 2, w, self.__class__.grosimeZid)
        else:
            self.cod += 2 ** 2
        if col > 0:
            self.zid[3] = pygame.Rect(left - 1 - self.__class__.grosimeZid // 2, top, self.__class__.grosimeZid, h)
        else:
            self.cod += 2 ** 3

    # print(self.zid)
    # 0001 zid doar sus
    # 0011 zid sus si dreapta etc
    def deseneaza(self):
        pygame.draw.rect(self.display, self.__class__.fundalCelula, self.dreptunghi)
        # masti=[1,2,4,8]
        masca = 1
        for i in range(4):
            if self.cod & masca:
                if self.zid[i]:
                    pygame.draw.rect(self.display, self.__class__.culoareLinii, self.zid[i])
            masca *= 2

class Joc:
    """
    Clasa care defineste jocul. Se va schimba de la un joc la altul.
    """
    NR_COLOANE = 9
    JMIN = None
    JMAX = None
    GOL = '#'
    culoareEcran = (0, 0, 0)
    dimCelula = 50
    paddingCelula = 5
    dimImagine = dimCelula - 2 * paddingCelula
    coordP1=4
    coordP2=76
    @classmethod
    def initializeaza(cls, display, NR_COLOANE=9, dim_celula=100):
        cls.display = display
        cls.dim_celula = dim_celula
        cls.x_img = pygame.image.load('cercalb.png')
        cls.x_img = pygame.transform.scale(cls.x_img, (dim_celula, dim_celula))
        cls.zero_img = pygame.image.load('cercrosu.png')
        cls.zero_img = pygame.transform.scale(cls.zero_img, (dim_celula, dim_celula))
        cls.celuleGrid = []  # este lista cu patratelele din grid
        cls.matrZids = []
        for linie in range(NR_COLOANE):
            for coloana in range(NR_COLOANE):
                patr1 = pygame.Rect(coloana * (dim_celula + 1), linie * (dim_celula + 1), dim_celula, dim_celula)
                patr = Celula(display=display, left=coloana * (cls.dim_celula + 1),
                       top=linie * (cls.dim_celula + 1), w=cls.dim_celula, h=cls.dim_celula,
                       lin=linie, col=coloana)
                cls.celuleGrid.append(patr)
                #cls.matrZids.append(patr)

    def deseneaza_grid(self, marcaj=None):  # tabla de exemplu este ["#","x","#","0",......]

        for ind in range(len(self.matr)):
            linie = ind // 9  # // inseamna div
            coloana = ind % 9

            if marcaj == ind:
                # daca am o patratica selectata, o desenez cu rosu
                culoare = (255, 0, 0)
            else:
                # altfel o desenez cu alb
                culoare = (255, 255, 255)
            #pygame.draw.rect(self.__class__.display, culoare, self.__class__.celuleGrid[ind])  # alb = (255,255,255)
            self.__class__.celuleGrid[ind].deseneaza()
            if self.matr[ind] == 'x':
                self.__class__.display.blit(self.__class__.x_img, (
                coloana * (self.__class__.dim_celula + 1), linie * (self.__class__.dim_celula + 1)))
            elif self.matr[ind] == '0':
                self.__class__.display.blit(self.__class__.zero_img, (
                coloana * (self.__class__.dim_celula + 1), linie * (self.__class__.dim_celula + 1)))
        pygame.display.flip()  # obligatoriu pentru a actualiza interfata (desenul)

    # pygame.display.update()

    def __init__(self, tabla=None):
        self.matr = tabla or [self.__class__.GOL] * 81
        self.matr[self.coordP1]='x'
        self.matr[self.coordP2]='0'
    @classmethod
    def jucator_opus(cls, jucator):
        return cls.JMAX if jucator == cls.JMIN else cls.JMIN

    def final(self):
        rez=(self.matr.index(Joc.JMIN)>72 or self.matr.index(Joc.JMAX)<9)
        if (rez):
            return 'ceva'
        elif self.__class__.GOL not in self.matr:
            return 'remiza'
        else:
            return False

    def mutari(self, jucator_opus):
        l_mutari = []
        indJo=self.matr.index(jucator_opus)
        for i in range(len(self.matr)):
            if (i == indJo - 1 and [i, 1] not in tups and (i%9!=0 and i%9!=8)) or \
                    (i == indJo + 1 and [i, 3] not in tups and (i%9!=0 and i%9!=8)) or \
                    (i == indJo + 9 and [i, 0] not in tups) or \
                    (i == indJo - 9 and [i, 2] not in tups):
                if self.matr[i] == self.__class__.GOL:
                    matr_tabla_noua = list(self.matr)
                    matr_tabla_noua[i] = jucator_opus
                    l_mutari.append(Joc(matr_tabla_noua))

        return l_mutari

    # linie deschisa inseamna linie pe care jucatorul mai poate forma o configuratie castigatoare
    # practic e o linie fara simboluri ale jucatorului opus
    def linie_deschisa(self, lista, jucator):
        jo = self.jucator_opus(jucator)
        # verific daca pe linia data nu am simbolul jucatorului opus
        if not jo in lista:
            return 1
        return 0

    def linii_deschise(self, jucator):
        return (self.linie_deschisa(self.matr[0:3], jucator)
                + self.linie_deschisa(self.matr[3:6], jucator)
                + self.linie_deschisa(self.matr[6:9], jucator)
                + self.linie_deschisa(self.matr[0:9:3], jucator)
                + self.linie_deschisa(self.matr[1:9:3], jucator)
                + self.linie_deschisa(self.matr[2:9:3], jucator)
                + self.linie_deschisa(self.matr[0:9:4], jucator)  # prima diagonala
                + self.linie_deschisa(self.matr[2:8:2], jucator))  # a doua diagonala

    def estimeaza_scor(self, adancime):
        t_final = self.final()
        # if (adancime==0):
        if t_final == self.__class__.JMAX:
            return (99 + adancime)
        elif t_final == self.__class__.JMIN:
            return (-99 - adancime)
        elif t_final == 'remiza':
            return 0
        else:
            return (self.linii_deschise(self.__class__.JMAX) - self.linii_deschise(self.__class__.JMIN))

    def __str__(self):
        sir = (" ".join([str(x) for x in self.matr[0:9]]) + "\n" +
               " ".join([str(x) for x in self.matr[9:18]]) + "\n" +
               " ".join([str(x) for x in self.matr[18:27]]) + "\n" +
               " ".join([str(x) for x in self.matr[27:36]]) + "\n" +
               " ".join([str(x) for x in self.matr[36:45]]) + "\n" +
               " ".join([str(x) for x in self.matr[45:54]]) + "\n" +
               " ".join([str(x) for x in self.matr[54:63]]) + "\n" +
               " ".join([str(x) for x in self.matr[63:72]]) + "\n" +
               " ".join([str(x) for x in self.matr[72:81]]) + "\n")

        return sir


class Stare:
    """
    Clasa folosita de algoritmii minimax si alpha-beta
    Are ca proprietate tabla de joc
    Functioneaza cu conditia ca in cadrul clasei Joc sa fie definiti JMIN si JMAX (cei doi jucatori posibili)
    De asemenea cere ca in clasa Joc sa fie definita si o metoda numita mutari() care ofera lista cu configuratiile posibile in urma mutarii unui jucator
    """

    def __init__(self, tabla_joc, j_curent, adancime, parinte=None, estimare=None):
        self.tabla_joc = tabla_joc
        self.j_curent = j_curent

        # adancimea in arborele de stari
        self.adancime = adancime

        # estimarea favorabilitatii starii (daca e finala) sau al celei mai bune stari-fiice (pentru jucatorul curent)
        self.estimare = estimare

        # lista de mutari posibile din starea curenta
        self.mutari_posibile = []

        # cea mai buna mutare din lista de mutari posibile pentru jucatorul curent
        self.stare_aleasa = None

    def mutari(self):
        l_mutari = self.tabla_joc.mutari(self.j_curent)
        juc_opus = Joc.jucator_opus(self.j_curent)
        l_stari_mutari = [Stare(mutare, juc_opus, self.adancime - 1, parinte=self) for mutare in l_mutari]

        return l_stari_mutari

    def __str__(self):
        sir = str(self.tabla_joc) + "(Juc curent:" + self.j_curent + ")\n"
        return sir


""" Algoritmul MinMax """


def min_max(stare):
    if stare.adancime == 0 or stare.tabla_joc.final():
        stare.estimare = stare.tabla_joc.estimeaza_scor(stare.adancime)
        return stare
    indexjc=stare.tabla_joc.matr.index(stare.j_curent)
    # calculez toate mutarile posibile din starea curenta
    stare.mutari_posibile = stare.mutari()

    # aplic algoritmul minimax pe toate mutarile posibile (calculand astfel subarborii lor)
    mutariCuEstimare = [min_max(mutare) for mutare in stare.mutari_posibile]

    if stare.j_curent == Joc.JMAX:
        # daca jucatorul e JMAX aleg starea-fiica cu estimarea maxima
        stare.stare_aleasa = max(mutariCuEstimare, key=lambda x: x.estimare)
    else:
        # daca jucatorul e JMIN aleg starea-fiica cu estimarea minima
        stare.stare_aleasa = min(mutariCuEstimare, key=lambda x: x.estimare)
    stare.estimare = stare.stare_aleasa.estimare
    stare.tabla_joc.matr[indexjc]='#'
    return stare


def alpha_beta(alpha, beta, stare):
    if stare.adancime == 0 or stare.tabla_joc.final():
        stare.estimare = stare.tabla_joc.estimeaza_scor(stare.adancime)
        return stare
    indexjc=stare.tabla_joc.matr.index(stare.j_curent)

    if alpha > beta:
        return stare  # este intr-un interval invalid deci nu o mai procesez

    stare.mutari_posibile = stare.mutari()

    if stare.j_curent == Joc.JMAX:
        estimare_curenta = float('-inf')

        for mutare in stare.mutari_posibile:
            # calculeaza estimarea pentru starea noua, realizand subarborele
            stare_noua = alpha_beta(alpha, beta, mutare)

            if (estimare_curenta < stare_noua.estimare):
                stare.stare_aleasa = stare_noua
                estimare_curenta = stare_noua.estimare
            if (alpha < stare_noua.estimare):
                alpha = stare_noua.estimare
                if alpha >= beta:
                    break

    elif stare.j_curent == Joc.JMIN:
        estimare_curenta = float('inf')

        for mutare in stare.mutari_posibile:

            stare_noua = alpha_beta(alpha, beta, mutare)

            if (estimare_curenta > stare_noua.estimare):
                stare.stare_aleasa = stare_noua
                estimare_curenta = stare_noua.estimare

            if (beta > stare_noua.estimare):
                beta = stare_noua.estimare
                if alpha >= beta:
                    break
    stare.estimare = stare.stare_aleasa.estimare
    stare.tabla_joc.matr[indexjc]='#'

    return stare


def afis_daca_final(stare_curenta, curentj):
    final = stare_curenta.tabla_joc.final()
    if (final):
        if (final == "remiza"):
            print("Remiza!")
        else:
            print("A castigat " + curentj)

        return True

    return False


def main():
    # initializare algoritm
    raspuns_valid = False
    while not raspuns_valid:
        tip_algoritm = input("Algorimul folosit? (raspundeti cu 1 sau 2)\n 1.Minimax\n 2.Alpha-beta\n ")
        if tip_algoritm in ['1', '2']:
            raspuns_valid = True
        else:
            print("Nu ati ales o varianta corecta.")
    #initilizare tip joc
    raspuns_valid = False
    while not raspuns_valid:
        tip_joc = input("Algorimul folosit? (raspundeti cu 1 sau 2)\n 1.Player vs Computer\n 2.Computer vs Computer\n 3.Player vs Player\n ")
        if tip_joc in ['1', '2', '3']:
            raspuns_valid = True
        else:
            print("Nu ati ales o varianta corecta.")
    # initializare jucatori
    raspuns_valid = False
    while not raspuns_valid:
        Joc.JMIN = input("Doriti sa jucati cu x sau cu 0? ").lower()
        if (Joc.JMIN in ['x', '0']):
            raspuns_valid = True
        else:
            print("Raspunsul trebuie sa fie x sau 0.")


    Joc.JMAX = '0' if Joc.JMIN == 'x' else 'x'

    # initializare tabla
    tabla_curenta = Joc();
    print("Tabla initiala")
    print(str(tabla_curenta))

    # creare stare initiala
    stare_curenta = Stare(tabla_curenta, 'x', ADANCIME_MAX)

    # setari interf grafica
    pygame.init()
    pygame.display.set_caption('x si 0')
    # dimensiunea ferestrei in pixeli
    ecran = pygame.display.set_mode(size=(908, 908))  # N *100+ N-1
    Joc.initializeaza(ecran)
    #tups=[]
    de_mutat = False
    tabla_curenta.deseneaza_grid()
    if tip_joc=='1':
        while True:

            if (stare_curenta.j_curent == Joc.JMIN):
                # muta jucatorul
                # [MOUSEBUTTONDOWN, MOUSEMOTION,....]
                # l=pygame.event.get()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()  # inchide fereastra
                        sys.exit()
                    elif event.type == pygame.MOUSEBUTTONDOWN:

                        pos = pygame.mouse.get_pos()  # coordonatele clickului
                        zidGasit = []
                        adev=0
                        for np in range(len(Joc.celuleGrid)):
                                    if Joc.celuleGrid[np].zid[0] and Joc.celuleGrid[np].zid[0].collidepoint(pos):
                                        zidGasit.append((Joc.celuleGrid[np], 0, Joc.celuleGrid[np].zid[0]))
                                        adev = 1
                                        tups.append([np,0])
                                    if Joc.celuleGrid[np].zid[1] and Joc.celuleGrid[np].zid[1].collidepoint(pos):
                                        zidGasit.append((Joc.celuleGrid[np], 1, Joc.celuleGrid[np].zid[1]))
                                        adev = 1
                                        tups.append([np, 1])

                                    if Joc.celuleGrid[np].zid[2] and Joc.celuleGrid[np].zid[2].collidepoint(pos):
                                        zidGasit.append((Joc.celuleGrid[np], 2,Joc.celuleGrid[np].zid[2]))
                                        adev = 1
                                        tups.append([np,2])

                                    if Joc.celuleGrid[np].zid[3] and Joc.celuleGrid[np].zid[3].collidepoint(pos):
                                        zidGasit.append((Joc.celuleGrid[np], 3, Joc.celuleGrid[np].zid[3]))
                                        adev = 1
                                        tups.append([np, 3])

                        celuleAfectate = []
                        if 0 < len(zidGasit) <= 2:
                            for (cel, iz, zid) in zidGasit:
                                pygame.draw.rect(Joc.display, Celula.culoareLinii, zid)
                                cel.cod |= 2 ** iz
                                celuleAfectate.append(cel)
                            # doar de debug
                            print("\nMatrice interfata: ")
                            for l in range(9):
                                for c in range(9):
                                    print(Joc.celuleGrid[l*9+c].cod, end=" ")
                                print()

                        pygame.display.update()
                        if adev==0:
                            for np in range(len(Joc.celuleGrid)):

                                if Joc.celuleGrid[np].dreptunghi.collidepoint(
                                        pos):  # verifica daca punctul cu coord pos se afla in dreptunghi(celula)
                                    linie = np // 9
                                    coloana = np % 9
                                    ###############################
                                    if stare_curenta.tabla_joc.matr[np] == Joc.JMIN:
                                        if (de_mutat and linie == de_mutat[0] and coloana == de_mutat[1]):
                                            # daca am facut click chiar pe patratica selectata, o deselectez
                                            de_mutat = False
                                            stare_curenta.tabla_joc.deseneaza_grid()
                                        else:
                                            de_mutat = (linie, coloana)
                                            # desenez gridul cu patratelul marcat
                                            stare_curenta.tabla_joc.deseneaza_grid(np)
                                    if stare_curenta.tabla_joc.matr[np] == Joc.GOL:
                                        if de_mutat:
                                            #### eventuale teste legate de mutarea simbolului
                                            stare_curenta.tabla_joc.matr[de_mutat[0] * 9 + de_mutat[1]] = Joc.GOL
                                            de_mutat = False
                                        # plasez simbolul pe "tabla de joc"
                                        indPlayer=stare_curenta.tabla_joc.matr.index(Joc.JMIN)
                                        if (linie * 9 + coloana==indPlayer-1 and [linie*9+coloana,1] not in tups) or \
                                                (linie * 9 + coloana==indPlayer+1 and [linie*9+coloana,3] not in tups) or \
                                                (linie * 9 + coloana==indPlayer+9 and [linie*9+coloana,0] not in tups) or \
                                                (linie * 9 + coloana==indPlayer-9 and [linie*9+coloana,2] not in tups):
                                            stare_curenta.tabla_joc.matr[indPlayer]='#'
                                            stare_curenta.tabla_joc.matr[linie * 9 + coloana] = Joc.JMIN
                                            Joc.coordP1=linie * 9 + coloana
                                            # afisarea starii jocului in urma mutarii utilizatorului
                                            print("\nTabla dupa mutarea jucatorului")
                                            print(str(stare_curenta))

                                            stare_curenta.tabla_joc.deseneaza_grid()
                                            # testez daca jocul a ajuns intr-o stare finala
                                            # si afisez un mesaj corespunzator in caz ca da

                                            if (afis_daca_final(stare_curenta,stare_curenta.j_curent)):
                                                break

                                            # S-a realizat o mutare. Schimb jucatorul cu cel opus
                                            stare_curenta.j_curent = Joc.jucator_opus(stare_curenta.j_curent)


            # --------------------------------
            else:  # jucatorul e JMAX (calculatorul)
                # Mutare calculator
                indexjs=stare_curenta.tabla_joc.matr.index(stare_curenta.j_curent)

                #indexos=stare_curenta.tabla_joc.matr.index()
                # preiau timpul in milisecunde de dinainte de mutare
                t_inainte = int(round(time.time() * 1000))
                if tip_algoritm == '1':
                    stare_actualizata = min_max(stare_curenta)
                else:  # tip_algoritm==2
                    stare_actualizata = alpha_beta(-500, 500, stare_curenta)
                stare_curenta.tabla_joc = stare_actualizata.stare_aleasa.tabla_joc
                stare_curenta.tabla_joc.matr[indexjs]='#'

                print("Tabla dupa mutarea calculatorului")
                print(str(stare_curenta))
                Joc.coordP2 = stare_curenta.tabla_joc.matr.index(stare_curenta.j_curent)
                stare_curenta.tabla_joc.deseneaza_grid()
                # preiau timpul in milisecunde de dupa mutare

                t_dupa = int(round(time.time() * 1000))
                print("Calculatorul a \"gandit\" timp de " + str(t_dupa - t_inainte) + " milisecunde.")

                if (afis_daca_final(stare_curenta,stare_curenta.j_curent)):
                    break

                # S-a realizat o mutare. Schimb jucatorul cu cel opus
                stare_curenta.j_curent = Joc.jucator_opus(stare_curenta.j_curent)
    elif tip_joc=='2':
        while True:
            if (stare_curenta.j_curent == Joc.JMIN):
                # muta jucatorul minmax
                indexjs = stare_curenta.tabla_joc.matr.index(stare_curenta.j_curent)

                # indexos=stare_curenta.tabla_joc.matr.index()
                # preiau timpul in milisecunde de dinainte de mutare
                t_inainte = int(round(time.time() * 1000))
                stare_actualizata = min_max(stare_curenta)
                stare_curenta.tabla_joc = stare_actualizata.stare_aleasa.tabla_joc
                stare_curenta.tabla_joc.matr[indexjs] = '#'

                print("Tabla dupa mutarea calculatorului")
                print(str(stare_curenta))
                Joc.coordP1 = stare_curenta.tabla_joc.matr.index(stare_curenta.j_curent)
                stare_curenta.tabla_joc.deseneaza_grid()
                # preiau timpul in milisecunde de dupa mutare

                t_dupa = int(round(time.time() * 1000))
                print("Calculatorul a \"gandit\" timp de " + str(t_dupa - t_inainte) + " milisecunde.")

                if (afis_daca_final(stare_curenta, stare_curenta.j_curent)):
                    break

                # S-a realizat o mutare. Schimb jucatorul cu cel opus
                stare_curenta.j_curent = Joc.jucator_opus(stare_curenta.j_curent)
                # --------------------------------
            else:  # jucatorul e JMAX (calculatorul)
                # Mutare calculator
                indexjs = stare_curenta.tabla_joc.matr.index(stare_curenta.j_curent)

                # indexos=stare_curenta.tabla_joc.matr.index()
                # preiau timpul in milisecunde de dinainte de mutare
                t_inainte = int(round(time.time() * 1000))

                stare_actualizata = alpha_beta(-500, 500, stare_curenta)
                stare_curenta.tabla_joc = stare_actualizata.stare_aleasa.tabla_joc
                stare_curenta.tabla_joc.matr[indexjs] = '#'

                print("Tabla dupa mutarea calculatorului")
                print(str(stare_curenta))
                Joc.coordP2 = stare_curenta.tabla_joc.matr.index(stare_curenta.j_curent)
                stare_curenta.tabla_joc.deseneaza_grid()
                # preiau timpul in milisecunde de dupa mutare

                t_dupa = int(round(time.time() * 1000))
                print("Calculatorul a \"gandit\" timp de " + str(t_dupa - t_inainte) + " milisecunde.")

                if (afis_daca_final(stare_curenta, stare_curenta.j_curent)):
                    break

                # S-a realizat o mutare. Schimb jucatorul cu cel opus
                stare_curenta.j_curent = Joc.jucator_opus(stare_curenta.j_curent)
    else:
        while True:

            if (stare_curenta.j_curent == Joc.JMIN):
                # muta jucatorul
                # [MOUSEBUTTONDOWN, MOUSEMOTION,....]
                # l=pygame.event.get()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()  # inchide fereastra
                        sys.exit()
                    elif event.type == pygame.MOUSEBUTTONDOWN:

                        pos = pygame.mouse.get_pos()  # coordonatele clickului

                        for np in range(len(Joc.celuleGrid)):

                            if Joc.celuleGrid[np].collidepoint(
                                    pos):  # verifica daca punctul cu coord pos se afla in dreptunghi(celula)
                                linie = np // 9
                                coloana = np % 9
                                ###############################
                                if stare_curenta.tabla_joc.matr[np] == Joc.JMIN:
                                    if (de_mutat and linie == de_mutat[0] and coloana == de_mutat[1]):
                                        # daca am facut click chiar pe patratica selectata, o deselectez
                                        de_mutat = False
                                        stare_curenta.tabla_joc.deseneaza_grid()
                                    else:
                                        de_mutat = (linie, coloana)
                                        # desenez gridul cu patratelul marcat
                                        stare_curenta.tabla_joc.deseneaza_grid(np)
                                if stare_curenta.tabla_joc.matr[np] == Joc.GOL:
                                    if de_mutat:
                                        #### eventuale teste legate de mutarea simbolului
                                        stare_curenta.tabla_joc.matr[de_mutat[0] * 9 + de_mutat[1]] = Joc.GOL
                                        de_mutat = False
                                    # plasez simbolul pe "tabla de joc"
                                    indPlayer=stare_curenta.tabla_joc.matr.index(Joc.JMIN)
                                    if linie * 9 + coloana==indPlayer-1 or linie * 9 + coloana==indPlayer+1 or linie * 9 + coloana==indPlayer+9 or linie * 9 + coloana==indPlayer-9:
                                        stare_curenta.tabla_joc.matr[indPlayer]='#'
                                        stare_curenta.tabla_joc.matr[linie * 9 + coloana] = Joc.JMIN
                                        Joc.coordP1=linie * 9 + coloana
                                        # afisarea starii jocului in urma mutarii utilizatorului
                                        print("\nTabla dupa mutarea jucatorului")
                                        print(str(stare_curenta))

                                        stare_curenta.tabla_joc.deseneaza_grid()
                                        # testez daca jocul a ajuns intr-o stare finala
                                        # si afisez un mesaj corespunzator in caz ca da

                                        if (afis_daca_final(stare_curenta,stare_curenta.j_curent)):
                                            break

                                        # S-a realizat o mutare. Schimb jucatorul cu cel opus
                                        stare_curenta.j_curent = Joc.jucator_opus(stare_curenta.j_curent)


            # --------------------------------
            else:  # jucatorul e JMAX
                # Mutare calculator
                # muta jucatorul
                # [MOUSEBUTTONDOWN, MOUSEMOTION,....]
                # l=pygame.event.get()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()  # inchide fereastra
                        sys.exit()
                    elif event.type == pygame.MOUSEBUTTONDOWN:

                        pos = pygame.mouse.get_pos()  # coordonatele clickului

                        for np in range(len(Joc.celuleGrid)):

                            if Joc.celuleGrid[np].collidepoint(
                                    pos):  # verifica daca punctul cu coord pos se afla in dreptunghi(celula)
                                linie = np // 9
                                coloana = np % 9
                                ###############################
                                if stare_curenta.tabla_joc.matr[np] == Joc.JMAX:
                                    if (de_mutat and linie == de_mutat[0] and coloana == de_mutat[1]):
                                        # daca am facut click chiar pe patratica selectata, o deselectez
                                        de_mutat = False
                                        stare_curenta.tabla_joc.deseneaza_grid()
                                    else:
                                        de_mutat = (linie, coloana)
                                        # desenez gridul cu patratelul marcat
                                        stare_curenta.tabla_joc.deseneaza_grid(np)
                                if stare_curenta.tabla_joc.matr[np] == Joc.GOL:
                                    if de_mutat:
                                        #### eventuale teste legate de mutarea simbolului
                                        stare_curenta.tabla_joc.matr[de_mutat[0] * 9 + de_mutat[1]] = Joc.GOL
                                        de_mutat = False
                                    # plasez simbolul pe "tabla de joc"
                                    indPlayer = stare_curenta.tabla_joc.matr.index(Joc.JMAX)
                                    if linie * 9 + coloana == indPlayer - 1 or linie * 9 + coloana == indPlayer + 1 or linie * 9 + coloana == indPlayer + 9 or linie * 9 + coloana == indPlayer - 9:
                                        stare_curenta.tabla_joc.matr[indPlayer] = '#'
                                        stare_curenta.tabla_joc.matr[linie * 9 + coloana] = Joc.JMAX
                                        Joc.coordP2 = linie * 9 + coloana
                                        # afisarea starii jocului in urma mutarii utilizatorului
                                        print("\nTabla dupa mutarea jucatorului")
                                        print(str(stare_curenta))

                                        stare_curenta.tabla_joc.deseneaza_grid()
                                        # testez daca jocul a ajuns intr-o stare finala
                                        # si afisez un mesaj corespunzator in caz ca da

                                        if (afis_daca_final(stare_curenta, stare_curenta.j_curent)):
                                            break

                                        # S-a realizat o mutare. Schimb jucatorul cu cel opus
                                        stare_curenta.j_curent = Joc.jucator_opus(stare_curenta.j_curent)


if __name__ == "__main__":
    main()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
