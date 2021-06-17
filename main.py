import random
import math
from random import randint
from numpy import random

#klasa pracownika
class Employee:
    def __init__(self, type):
        self.type = type  # 0 -kucharz, 1-kelner, 2- manager

    workTime = 0    #czas pracy
    isBusy = False  #czy pracuje

#grupa pracownikow
class EmployeeGroup:
    def __init__(self, id):
        self.id = id            #id grupy
        self.employeeList = []  #lista okreslonych pracownikow

    def makeGroup(self, number, employeType):   #tworzenie grupy pracownikow
        for num in range(number):
            employee = Employee(employeType)
            self.employeeList.append(employee)

    def isGroupFree(self):                      #sprawdzenie czy w grupie sa wolni pracownicy
        for employee in self.employeeList:
            if not employee.isBusy:
                return True
        return False

    def groupWork(self, time):                  #przydzielenie zadania 1 osobie z grupy pracownikow
        for employee in self.employeeList:
            if not employee.isBusy:
                employee.workTime = time
                employee.isBusy = True
                break

    def workUpdate(self):                       #aktualizacja czasu pracy
        for employee in self.employeeList:
            if employee.workTime > 0:
                employee.workTime -= 1
            if employee.workTime == 0:
                employee.isBusy = False

#klasa restauracji
class Restaurant:
    def __init__(self, worktime, rushHourstart, rushHourEnd):
        self.worktime = worktime        #godziny otwarcia
        self.rHrstart = rushHourstart   #poczatek godzin szczytu
        self.rHrend = rushHourEnd       #koniec godzin szczytu

    unservTablesList = []  # wolne stoły
    filledTablesList = []  # zajęte stoły

    allguestList = []  # goście którzy jeszcze nie dotarli
    waitlineguestList = []  # goście którzy są w kolejce
    takeawayList = []  # goście którzy są w kolejce i zamawiaja na wynos
    markList = []      #lista osob oceniających

    orderlist = []      #lista zamowien
    dishMap = {}
    revenue = 0         #przychod

    def markRestaurant(self, group):            #funkcja oceny restauracji
        for client in group.listofPeople[:]:
            for markedClient in self.markList[:]:
                if markedClient.clientID == client.clientID:
                    self.markList.remove(markedClient)
            self.markList.append(client)

    # tworzenie stołow
    def addTables(self, twoPerson, fourPerson, sixPerson, eightperson):
        tableID = 0
        for i in range(twoPerson):
            table = Table(2, tableID)

            self.unservTablesList.append(table)
            tableID = tableID + 1

        for i in range(fourPerson):
            table = Table(4, tableID)

            self.unservTablesList.append(table)
            tableID = tableID + 1

        for i in range(sixPerson):
            table = Table(6, tableID)

            self.unservTablesList.append(table)
            tableID = tableID + 1

        for i in range(eightperson):
            table = Table(8, tableID)

            self.unservTablesList.append(table)
            tableID = tableID + 1

    # dodawanie klientów na początku tworzymy listę osób co pajawią się w ciągu dnia a potem się będziemy bawić
    # w umieszczenie w kolejce
    def addGuests(self, average):
        generated_guests = 0
        time = self.worktime
        guestID = 0
        groupID = 0
        godzinadzialania = 0
        # w ostatniej linijce jest warunek kończący pętlę

        while godzinadzialania < time:  # dla każdej godziny działania losujemy grupy
            # tutaj w sumie się nie bawiłem w rozkłady normalne bo powinni być w miare równomiernie rozłożeni w godzinie
            y = random.logistic(loc=average, scale=0.2 * average, size=1)  # rozkład losowy ale skalujący się opisujący wzrost
            if godzinadzialania >= self.rHrstart and godzinadzialania < self.rHrend:
                y = y + (average // 2)  # jeśli godz szczytu to dorzucamy 50proc średniej

            while y > 0:
                x = 10
                while (x > 8 or x < 1):
                    x = round(
                        random.uniform(1, 8))  # rozład losowy w którym każde zdarzenie ma równe prawdopodobieństwo
                generated_guests += x
                grupa = []
                minpat = 99999
                for i in range(x):
                    patience = 15 + random.normal(loc=0, scale=5, size=1)
                    if (patience < 1):
                        patience = 1

                    # minpat najmniejsza cierpliwość w danej grupie ludzi
                    if patience < minpat:  # cierpliwość grupy
                        minpat = patience
                    client = Client(patience, guestID, groupID)
                    grupa.append(client)
                    guestID = guestID + 1
                arrival = 0
                if godzinadzialania <= (time - 2):  # dla wszystkich godzin przed ostatnią mogą być w całej godzinie
                    arrival = randint((60 * godzinadzialania),
                                      (60 * ((godzinadzialania) + 1)))  # czas przybycia przed ostatnią godz
                elif godzinadzialania == (time - 1):  # dla ostatniej godziny mogą być tylko przez pierwsze 30min
                    arrival = randint((60 * godzinadzialania), ((60 * ((godzinadzialania) + 1)) - 30))
                # rodzaj zamówienia dla grupy
                losujzamowienie = randint(1, 50)
                rodzajzamowienia = False    #false to zamowienie normalne
                if losujzamowienie <= 10:
                    rodzajzamowienia = True #true to na wynos

                groupofpeople = Groupofpeople(x, arrival, minpat, rodzajzamowienia, groupID)
                groupofpeople.listofPeople = grupa

                self.allguestList.append(groupofpeople)
                groupID = groupID + 1
                y = y - x
            godzinadzialania += 1
        #print("Wygenerowani klienci: " + str(generated_guests))

    def guestInside(self):              #funkcja sprawdzająca czy goście są w środku
        guestinside = False
        for table in self.filledTablesList[:]:
            if table.status == True:
                guestinside = True
        if len(self.waitlineguestList) > 0:
            guestinside = True
        return guestinside


class Table:
    def __init__(self, chairs, id):
        self.chairs = chairs
        self.tableID = id

    status = False
    orderTaken = False
    guestList = []

    def emptyTable(self):
        self.guestList.clear()
        self.status = False
        self.orderTaken = False

    def fillTable(self, guests):
        self.guestList = guests
        self.status = True

    def finishedEating(self):
        finished = True
        for client in self.guestList[:]:
            if client.clientStatus != 2:
                finished = False
        return finished


class Client:

    def __init__(self, patience, clientID, groupID):
        self.patience = patience
        self.clientID = clientID
        self.groupID = groupID

    restaurantMark = 5.0
    clientStatus = 0  # 0-jeszcze nie je, 1-je, 2-zjadł
    clientEatTime = 0



# szybciej będzie jak się ich zgrupuje
class Groupofpeople:
    def __init__(self, number, arrivaltime, minpatience, ordertype, id):
        self.numberofGuests = number
        self.arrival = arrivaltime
        self.minimalPatience = minpatience
        self.ordertype = ordertype
        self.id = id

    listofPeople = []
    timewaited = 0

    def timeMarkCalc(self):
        for client in self.listofPeople[:]:
            procent = self.timewaited / client.patience
            if procent < 0.4:
                client.restaurantMark = client.restaurantMark * 1.2
                if client.restaurantMark > 10.0:
                    client.restaurantMark = 10.0
            else:
                client.restaurantMark = client.restaurantMark * 0.7

    # do obslugi kolejki
    def resignorNot(self):
        resign = False
        if self.timewaited >= self.minimalPatience:
            resign = True
        return resign


class Order:
    def __init__(self, klientId, tableId, rodzaj, czas, cena):
        self.klientID = klientId
        self.tableID = tableId
        self.rodzaj = rodzaj
        self.czas = czas
        self.cena = cena

    def isReady(self):
        isready = True
        if self.czas > 0:
            isready = False
        return isready



# main func
def main():


    # zmienne na razie w funkcji
    global menagers
    chefNum = int(input("Podaj liczbe kucharzy\n"))
    chefSalary = int(input("Podaj pensje\n"))
    waiterNum = int(input("Podaj liczbe kelnerow\n"))
    waiterSalary = int(input("Podaj pensje\n"))
    managerNum = int(input("Podaj liczbe managerow\n"))
    managerSalary = int(input("Podaj pensje\n"))
    table2 = int(input("Podaj liczbe stolow 2-osobowych\n"))
    table4 = int(input("Podaj liczbe stolow 4-osobowych\n"))
    table6 = int(input("Podaj liczbe stolow 6-osobowych\n"))
    table8 = int(input("Podaj liczbe stolow 8-osobowych\n"))
    avgGuestperHour = int(input("Srednia liczba gosci w restauracji\n"))
    workTime = int(input("Podaj czas pracy restauracji\n"))
    rushS = int(workTime * 0.5)
    restaurant = Restaurant(workTime, rushS, rushS + 1)  # rush hour start i end to nie godziny zegarowe
    # tylko godziny działania restauracji np jak zaczynamy o 8 i rushhourstart jest 4 to chodzi o to że się
    # zaczya o 12

    czaszamkniecia = restaurant.worktime * 60  # pentla będzie co minutę

    managers = EmployeeGroup(1)
    managers.makeGroup(managerNum, 2)
    waiters = EmployeeGroup(2)
    waiters.makeGroup(waiterNum, 1)
    cook = EmployeeGroup(3)
    cook.makeGroup(chefNum, 0)
    # główna pętla
    # założenie jest takie żeby co minutę wykonywać wszystkie operacje po kolei

    #
    #
    #
    #
    #
    #
    #
    #
    days = int(input("Podaj ilosc dni\n"))
    avgMark = 0
    oceny = 0
    profil = int(input("Wybierz profil: 0 - FastFood, 1 - Zwyczajna restauracja, 2 - Restauracja droga\n"))
    global expectedPrice
    if profil == 0:
        expectedPrice = 15
    elif profil == 1:
        expectedPrice = 25
    elif profil == 2:
        expectedPrice = 35

    dishmax = int(input("Podaj ilosc dan\n"))
    for d in range(dishmax):
        price = int(input("Podaj cene dania\n"))
        restaurant.dishMap[d+1] = price

    criticalPrice = 0
    for p in range(dishmax):
        criticalPrice += restaurant.dishMap[p + 1]

    for i in range(days):
        restaurant.markList.clear()
        restaurant.unservTablesList.clear()
        restaurant.filledTablesList.clear()
        restaurant.allguestList.clear()
        restaurant.waitlineguestList.clear()
        restaurant.takeawayList.clear()
        restaurant.orderlist.clear()

        restaurant.addGuests(avgGuestperHour)
        restaurant.addTables(table2, table4, table6, table8)

        czyotwarte = True
        czasdzialania = 0

        while czyotwarte or restaurant.guestInside():  # działa w czasie pracy i jak są klienci
            #chef = chefNum
            # kelnerzy = waiterNum
            # menagers = managerNum
            managers.workUpdate()
            waiters.workUpdate()
            cook.workUpdate()


            #ocenianie na podstawie czasu oczekiwania na zamowienia
            for table in restaurant.filledTablesList[:]:
                for klient in table.guestList[:]:
                    if klient.clientStatus == 0:
                        klient.restaurantMark = klient.restaurantMark * 0.7
                    else:
                        klient.restaurantMark = klient.restaurantMark * 1.3
                        if klient.restaurantMark > 10:
                            klient.restaurantMark = 10
                    if criticalPrice > 2 * expectedPrice * dishmax:
                        klient.restaurantMark = klient.restaurantMark * 0.8
                    elif criticalPrice > expectedPrice * dishmax:
                        klient.restaurantMark = klient.restaurantMark * 0.9
                    elif criticalPrice < 2 * expectedPrice * dishmax:
                        klient.restaurantMark = klient.restaurantMark * 1.2
                    elif criticalPrice < expectedPrice * dishmax:
                        klient.restaurantMark = klient.restaurantMark * 1.1




            for groupofpeople in restaurant.allguestList[:]:
                # sprawdzamy czy czas przyjścia grupy nadszedł
                # jśli tak to przerzucamy ich do kolejki
                if groupofpeople.arrival == czasdzialania:
                    if groupofpeople.ordertype:
                        restaurant.takeawayList.append(groupofpeople)
                    else:
                        restaurant.waitlineguestList.append(groupofpeople)
                        restaurant.allguestList.remove(groupofpeople)
            # dostępni menagerzy
            # (na razie zakładam że menagerzy zawsze dostępni czyli czas obsługi =1 minuta)

            # if czasdzialania == czaszamkniecia:
            #     restaurant.waitlineguestList.clear()

            for groupofpeopleW in restaurant.takeawayList[:]:  # jeśli dalej stoją w kolejce
                groupofpeopleW.timewaited += 1  # zwiększamy czas jaki stoją
                groupofpeopleW.timeMarkCalc()
                restaurant.markRestaurant(groupofpeopleW)
                for klientWyn in groupofpeopleW.listofPeople[:]:
                    if criticalPrice > 2 * expectedPrice * dishmax:
                        klientWyn.restaurantMark = klientWyn.restaurantMark * 0.8
                    elif criticalPrice > expectedPrice * dishmax:
                        klientWyn.restaurantMark = klientWyn.restaurantMark * 0.9
                    elif criticalPrice < 2 * expectedPrice * dishmax:
                        klientWyn.restaurantMark = klientWyn.restaurantMark * 1.2
                    elif criticalPrice < expectedPrice * dishmax:
                        klientWyn.restaurantMark = klientWyn.restaurantMark * 1.1
                if groupofpeopleW.resignorNot():  # sprawdzamy czy są dalej cierpliwi
                    restaurant.takeawayList.remove(groupofpeopleW)  # jeśli nie są to wywalamy ich z kolejki

            kolejkanaW = len(restaurant.takeawayList)
            if kolejkanaW > 0:
                for klientWynos in restaurant.takeawayList[:]:
                    if cook.isGroupFree():
                        restaurant.takeawayList.remove(klientWynos)
                        cook.groupWork(len(klientWynos.listofPeople)*randint(5, 10))
                        restaurant.revenue += len(klientWynos.listofPeople)*int(restaurant.dishMap[randint(1, dishmax)])
                        break
                    else:
                        break



            dlugkolejki = len(restaurant.waitlineguestList)
            if dlugkolejki > 0 and managers.isGroupFree():    #menagers > 0:
                for table in restaurant.unservTablesList[:]:
                    for groupofpeople in restaurant.waitlineguestList[:]:

                        if managers.isGroupFree():             #menagers > 0:

                            if table.chairs >= groupofpeople.numberofGuests:
                                # jeśli trafimy na wolny stół co ma tyle samo lub więcej krzeseł niż trzeba)
                                #menagers -= 1  # menager zajęty na turę
                                managers.groupWork(5)
                               # dlugkolejki = dlugkolejki - 1  # zmniejszamy długość kolejki
                                # porządki w listach
                                table.status = True
                                table.guestList = groupofpeople.listofPeople
                                restaurant.waitlineguestList.remove(groupofpeople)

                                groupofpeople.timeMarkCalc()
                                restaurant.markRestaurant(groupofpeople)

                                restaurant.filledTablesList.append(table)
                                restaurant.unservTablesList.remove(table)

                                break
                        else:
                            break

            for groupofpeople in restaurant.waitlineguestList[:]:  # jeśli dalej stoją w kolejce
                groupofpeople.timewaited += 1  # zwiększamy czas jaki stoją
                groupofpeople.timeMarkCalc()
                restaurant.markRestaurant(groupofpeople)
                if groupofpeople.resignorNot():  # sprawdzamy czy są dalej cierpliwi
                    restaurant.waitlineguestList.remove(groupofpeople)  # jeśli nie są to wywalamy ich z kolejki


            # dostarczanie zamówień
            zamowienia = len(restaurant.orderlist)

            if zamowienia > 0:

                for order in restaurant.orderlist[:]:
                    if waiters.isGroupFree() and order.isReady():  # kelnerzy > 0
                        # kelnerzy -= 1
                        waiters.groupWork(2)
                        for table in restaurant.filledTablesList[:]:
                            if table.tableID == order.tableID:
                                for client in table.guestList[:]:
                                    # dostarczenie zamówienia klientowi:
                                    if client.clientID == order.klientID:
                                        client.clientStatus = 1
                                        timeofeating = math.ceil(random.normal(loc=10, scale=4, size=1))
                                        if (timeofeating < 3):
                                            timeofeating = 3
                                        client.clientEatTime = timeofeating
                                        restaurant.revenue += order.cena  # tymczasowo
                                        restaurant.orderlist.remove(order)  # usunięcie zamówienia z listy zamówień
                                        break

            # jedzenie
            for table in restaurant.filledTablesList[:]:
                for client in table.guestList[:]:
                    if client.clientStatus == 1:
                        client.clientEatTime -= 1
                        if client.clientEatTime <= 0:
                            client.clientStatus = 2

            # koniec jedzenia i wyjście klientów
            for table in restaurant.filledTablesList[:]:
                if table.finishedEating():
                    table.emptyTable()
                    restaurant.unservTablesList.append(table)
                    restaurant.filledTablesList.remove(table)

            # zamówienia

            if waiters.isGroupFree():  # kelnerzy > 0:
                for table in restaurant.filledTablesList[:]:
                    if waiters.isGroupFree():  # kelnerzy > 0:
                        if table.orderTaken == False:  # jeśli stolik nie złożył zamówienia
                            table.orderTaken = True
                            # kelnerzy = kelnerzy - 1
                            waiters.groupWork(2)
                            for client in table.guestList[:]:
                                danie = randint(1, dishmax)
                                order = Order(client.clientID, table.tableID, danie, randint(5,10), restaurant.dishMap[danie])
                                restaurant.orderlist.append(order)
            # gotowanie
            zamowienia = len(restaurant.orderlist)
            if zamowienia > 0:
                for order in restaurant.orderlist[:]:
                    if cook.isGroupFree():  # chef > 0:
                        if not order.isReady():  # jeśli zamówienie nie jest skończone i jest dostępny szef to zmniejszamy jego czas o minutę
                            # chef = chef - 1
                            order.czas = int(order.czas * 0.3)
                            cook.groupWork(order.czas)

            czasdzialania += 1
            if czasdzialania == czaszamkniecia:
                czyotwarte = False

        for client in restaurant.markList:
             avgMark += client.restaurantMark
        avgMark = avgMark / len(restaurant.markList)
        oceny = oceny + len(restaurant.markList)

    # później można nadgodziny wziąć
    # chefcost = chefNum * chefSalary * restaurant.workHours() + menagers * managerSalary * restaurant.workHours()
    chefcost = chefNum * chefSalary * restaurant.worktime*days
    menagercost = managerNum * managerSalary * restaurant.worktime*days
    waitercost = waiterNum * waiterSalary * restaurant.worktime*days
    print(" ")
    print("Czas pracy: " + str(restaurant.worktime) + " Godzin")
    print("Wygenerowani klienci : " + str(oceny))
    # for i in restaurant.markList[:]:
    #     print(str(i.restaurantMark) + " id: " + str(i.clientID))
    print("Koszt kelnerów: " + str(waitercost))
    print("Koszt kucharzy: " + str(chefcost))
    print("Koszt menagerów: " + str(menagercost))
    allcost = chefcost + menagercost + waitercost
    print("Wszstkie koszty: " + str(allcost))
    print("Dochód: " + str(restaurant.revenue))
    adjusted_revenue = restaurant.revenue - allcost
    print("Dochód po kosztach: " + str(adjusted_revenue))
    print("Srednia ocena restauracji: " + str(int(avgMark)) + "/10")


if __name__ == "__main__":
    main()
