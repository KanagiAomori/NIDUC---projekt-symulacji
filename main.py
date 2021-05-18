# --------------------------------------------------------------------------------------------------------------------
from random import randint


class Employee:
    def __init__(self, type, salary):
        self.salary = salary
        self.type = type

    state = False

    def makeBusy(self, employeeName, restaurant):
        if employeeName == "chef":
            restaurant.busyList.append(restaurant.chefList[0])
            restaurant.chefList.remove(restaurant.chefList[0])
        if employeeName == "waiter":
            restaurant.busyList.append(restaurant.waiterList[0])
            restaurant.waiterList.remove(restaurant.waiterList[0])
        if employeeName == "manager":
            restaurant.busyList.append(restaurant.managerList[0])
            restaurant.managerList.remove(restaurant.managerList[0])

    def endBusy(self, employeeName, restaurant):
        for employee in restaurant.busyList:
            if (employee.type == employeeName):
                if employeeName == "chef":
                    restaurant.chefList.append(employee)
                elif employeeName == "waiter":
                    restaurant.waiterList.append(employee)
                elif employeeName == "manager":
                    restaurant.managerList.append(employee)
                restaurant.busyList.rempve(employee)
                break


class Restaurant:
    def __init__(self, type, openHour, closeHour):
        self.type = type
        self.openHour = openHour
        self.closeHour = closeHour

    allTablesList = []  # wszystkie stoły
    unservTablesList = []  # wolne stoły
    filledTablesList = []  # zajęte stoły
    chefList = []
    waiterList = []
    managerList = []
    busyList = []

    allguestList = []  # goście którzy jeszcze nie dotarli
    waitlineguestList = []  # goście którzy są w kolejce

    orderlist = []

    def workHours(self):
        return self.closeHour - self.openHour

    def addEmployees(self, chefNum, waiterNum, managerNum, chefSalary, waiterSalary, managerSalary):
        for i in range(chefNum):
            employe = Employee("chef", chefSalary)
            self.chefList.append(employe)

        for i in range(waiterNum):
            employe = Employee("waiter", waiterSalary)
            self.waiterList.append(employe)

        for i in range(managerNum):
            employe = Employee("manager", managerSalary)
            self.managerList.append(employe)

    # tworzenie stołow
    def addTables(self, twoPerson, fourPerson, sixPerson, eightperson):
        tableID = 0
        for i in range(twoPerson):
            table = Table(2, tableID)
            self.allTablesList.append(table)
            self.unservTablesList.append(table)
            tableID = tableID + 1

        for i in range(fourPerson):
            table = Table(4, tableID)
            self.allTablesList.append(table)
            self.unservTablesList.append(table)
            tableID = tableID + 1

        for i in range(sixPerson):
            table = Table(6, tableID)
            self.allTablesList.append(table)
            self.unservTablesList.append(table)
            tableID = tableID + 1

        for i in range(eightperson):
            table = Table(8, tableID)
            self.allTablesList.append(table)
            self.unservTablesList.append(table)
            tableID = tableID + 1

    # dodawanie klientów na początku tworzymy listę osób co pajawią się w ciągu dnia a potem się będziemy bawić
    # w umieszczenie w kolejce
    def addGuests(self, average):
        time = self.workHours()
        zakres = (time * 60) - 30  # do 30 min przed zamknięciem wpuszczamy klientów
        numberofguests = time * average  # dzienne liczba klientów
        guestID = 0
        groupID = 0
        while numberofguests > 0:

            x = randint(1, 8)
            grupa = []
            minpat = 99999

            for i in range(x):

                patience = 10 + randint(1, 10)
                if patience < minpat:
                    minpat = patience
                client = Client(patience, guestID, groupID)
                grupa.append(client)
                guestID = guestID + 1

            arrival = randint(0, zakres)  # czas przybycia
            groupofpeople = Groupofpeople(x, arrival, minpat)
            groupofpeople.listofPeople = grupa
            self.allguestList.append(groupofpeople)
            groupID = groupID + 1
            numberofguests = numberofguests - x

    def guestInside(self):
        guestinside = False
        for table in self.allTablesList:
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
    przyjętezamowienie = False
    guestList = []

    # dodatkowe funkcje
    def isOpen(self):
        isopen = True
        if self.status != 0:
            isopen = False
        return isopen

    def emptyTable(self):
        self.guestList.clear()
        self.status = False

    def fillTable(self, guests):
        self.guestList = guests
        self.status = True


class Client:
    # def __init__(self, patience, orderType):
    #     self.orderType = orderType
    #     self.patience = patience

    def __init__(self, patience, clientID, groupID):
        self.patience = patience
        self.clientID = clientID
        self.groupID = groupID

    hapiness = True
    waitTime = 0


# szybciej będzie jak się ich zgrupuje
class Groupofpeople:
    def __init__(self, number, arrivaltime, minpatience):
        self.numberofGuests = number
        self.arrival = arrivaltime
        self.minimalPatience = minpatience

    listofPeople = []
    timewaited = 0

    # do obslugi kolejki
    def resignorNot(self):
        resign = False
        if self.timewaited >= self.minimalPatience:
            resign = True
        return resign

    def incTimewaited(self):
        self.timewaited = self.timewaited + 1


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

    def decTime(self):
        self.czas = self.czas - 1


# Symulacja:
# typeRestaurant = "stacjonarna"
# chefNum = 5
# chefSalary = 2000
# waiterNum = 6
# waiterSalary = 2000
# managerNum = 1
# managerSalary = 2000
# tableNum = 20
# carNum = 0
# symDays = 20
# restaurant = Restaurant(typeRestaurant, 8, 18)
# restaurant.addEmployees(chefNum, waiterNum, managerNum, chefSalary, waiterSalary, managerSalary)


# reading simulation configuration parameters from file
class FileHandler:
    buffer = [];
    start_config = [];

    def read_config(self):
        self.start_config = open('config.txt', 'r')
        self.buffer = self.start_config.read()

    def print_config(self):
        print(self.buffer)

    def write_result(self, result):
        result_file = open('result.txt', 'w')  # w or a
        for line in result:
            result_file.write(line)

    # def print_result(self):


# main func
def main():
    #
    # test file
    # fh = FileHandler()
    # fh.read_config()
    # fh.print_config()

    # zmienne na razie w funkcji
    typeRestaurant = "stacjonarna"
    chefNum = 5
    chefSalary = 2000
    waiterNum = 6
    waiterSalary = 2000
    managerNum = 1
    managerSalary = 2000
    table2 = 4
    table4 = 4
    table6 = 2
    table8 = 2
    avgGuestperHour = 12
    restaurant = Restaurant(typeRestaurant, 8, 18)
    restaurant.addEmployees(chefNum, waiterNum, managerNum, chefSalary, waiterSalary, managerSalary)
    restaurant.addTables(table2, table4, table6, table8)
    restaurant.addGuests(avgGuestperHour)

    # to tylko do kontroli czy klientów poprawnie dodaje (do tego momętu działa
    for groupofpeople in restaurant.allguestList:
        print("Liczba gosci" + str(groupofpeople.numberofGuests))

        for client in groupofpeople.listofPeople:
            print("id klienta:" + str(client.clientID) + " id grupy" + str(client.groupID))

    czasdzialania = 0
    czaszamkniecia = restaurant.workHours() * 60  # pentla będzie co minutę

    # główna pętla
    # założenie jest takie żeby co minutę wykonywać wszystkie operacje po kolei
    while czasdzialania <= czaszamkniecia or restaurant.guestInside():  # działa w czasie pracy i jak są klienci

        for groupofpeople in restaurant.allguestList:
            # sprawdzamy czy czas przyjścia grupy nadszedł
            # jśli tak to przerzucamy ich do kolejki
            if groupofpeople.arrival == czasdzialania:
                restaurant.waitlineguestList.append(groupofpeople)
                restaurant.allguestList.remove(groupofpeople)

        menagers = len(restaurant.managerList)  # dostępni menagerzy
        # (na razie zakładam że menagerzy zawsze dostępni czyli czas obsługi =1 minuta)
        dlugkolejki = len(restaurant.waitlineguestList)
        if dlugkolejki > 0 and menagers > 0:

            for table in restaurant.unservTablesList:

                for groupofpeople in restaurant.waitlineguestList:

                    if menagers > 0:

                        if table.chairs >= groupofpeople.numberofGuests:
                            # jeśli trafimy na wolny stół co ma tyle samo lub więcej krzeseł niż trzeba)
                            menagers = menagers - 1  # menager zajęty na turę
                            dlugkolejki = dlugkolejki - 1  # zmniejszamy długość kolejki
                            # porządki w listach
                            table.status = True
                            table.guestList = groupofpeople.listofPeople
                            restaurant.waitlineguestList.remove(groupofpeople)
                            restaurant.filledTablesList.append(table)
                            restaurant.unservTablesList.remove(table)
                            break

        for groupofpeople in restaurant.waitlineguestList:  # jeśli dalej stoją w kolejce
            groupofpeople.incTimewaited()  # zwiększamy czas jaki stoją
            if groupofpeople.resignorNot():  # sprawdzamy czy są dalej cierpliwi
                restaurant.waitlineguestList.remove(groupofpeople)  # jeśli nie są to wywalamy ich z kolejki
        # zamówienia
        kelnerzy = len(restaurant.waiterList)  # zakładam że wszyscy dostępni na razie
        if kelnerzy > 0:
            for table in restaurant.filledTablesList:
                if kelnerzy > 0:
                    if table.przyjętezamowienie == False:  # jeśli stolik złożył zamówienia
                        kelnerzy = kelnerzy - 1
                        for client in table.guestList:
                            danie = randint(1, 2)  # 1to zupa 2- drugie danie
                            czas = 0
                            cena = 0
                            if danie == 1:
                                czas = 2  # 2 min dla zupy
                                cena = 5
                            elif danie == 2:
                                czas = 3  # 3min
                                cena = 10
                            order = Order(client.clientID, table.tableID, danie, czas, cena)
                            restaurant.orderlist.append(order)
        # gotowanie
        zamówienia = len(restaurant.orderlist)
        chef = len(restaurant.chefList)
        if zamówienia > 0:
            for order in restaurant.orderlist:
                if chef>0:
                    if not order.isReady():#jeśli zamówienie nie jest skończone i jest dostępny szef to zmniejszamy jego czas o minutę
                        chef=chef-1
                        order.decTime()


        #dostarczanie


    czasdzialania = czasdzialania + 1


if __name__ == "__main__":
    main()

# ---------------------------------------------------------------------------------------------------------------------------------------------
