# --------------------------------------------------------------------------------------------------------------------
from random import randint


class Employee:
    def __init__(self, type, salary):
        self.salary = salary
        self.type = type

    isBusy = False


class Restaurant:
    def __init__(self, type, openHour, closeHour):
        self.type = type
        self.openHour = openHour
        self.closeHour = closeHour

    unservTablesList = []  # wolne stoły
    filledTablesList = []  # zajęte stoły
    employeeList = []

    allguestList = []  # goście którzy jeszcze nie dotarli
    waitlineguestList = []  # goście którzy są w kolejce

    orderlist = []
    revenue = 0

    def workHours(self):
        if self.closeHour < self.openHour:
            return abs((24 - self.openHour + self.closeHour)) % 24
        if (self.closeHour == self.openHour):
            return 24
        return self.closeHour - self.openHour

    def addEmployees(self, chefNum, waiterNum, managerNum, chefSalary, waiterSalary, managerSalary):
        for i in range(chefNum):
            employe = Employee("chef", chefSalary)
            self.employeeList.append(employe)

        for i in range(waiterNum):
            employe = Employee("waiter", waiterSalary)
            self.employeeList.append(employe)

        for i in range(managerNum):
            employe = Employee("manager", managerSalary)
            self.employeeList.append(employe)

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
        time = self.workHours()
        zakres = (time * 60) - 30  # do 30 min przed zamknięciem wpuszczamy klientów
        numberofguests = time * average  # dzienne liczba klientów
        guestID = 0
        groupID = 0
        # w ostatniej linijce jest warunek kończący pętlę
        while numberofguests > 0:

            x = randint(1, 8)
            grupa = []
            minpat = 99999

            for i in range(x):

                patience = 10 + randint(1, 10)
                # minpat najmniejsza cierpliwość w danej grupie ludzi
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
        guestinside = 0
        print(len(self.waitlineguestList))
        for table in self.filledTablesList:
            if table.status == True:
                guestinside = 1

        if len(self.waitlineguestList) > 0:
            guestinside = 1
        return guestinside

    def countWorkers(self, type):
        sum = 0
        for employee in self.employeeList:
            if employee.type == type:
                sum += 1

        return sum


class Table:
    def __init__(self, chairs, id):
        self.chairs = chairs
        self.tableID = id

    status = False
    orderTaken = False
    guestList = []

    # dodatkowe funkcje
    # def isOpen(self):
    #     isopen = True
    #     if self.status != 0:
    #         isopen = False
    #     return isopen

    def emptyTable(self):
        self.guestList.clear()
        self.status = False
        self.orderTaken = False

    def fillTable(self, guests):
        self.guestList = guests
        self.status = True

    def finishedEating(self):
        finished = True
        for client in self.guestList:
            if client.clientStatus != 2:
                finished = False
        return finished


class Client:


    def __init__(self, patience, clientID, groupID):
        self.patience = patience
        self.clientID = clientID
        self.groupID = groupID

    hapiness = True
    waitTime = 0
    clientStatus = 0  # 0-jeszcze nie je, 1-je, 2-zjadł
    clientEatTime = 0


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

    # def incTimewaited(self):
    #     self.timewaited = self.timewaited + 1


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

    # def decTime(self):
    #     self.czas = self.czas - 1


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
    chefSalary = 15
    waiterNum = 6
    waiterSalary = 15
    managerNum = 1
    managerSalary = 15
    table2 = 4
    table4 = 4
    table6 = 2
    table8 = 2
    avgGuestperHour = 12
    restaurant = Restaurant(typeRestaurant, 2, 22)
    restaurant.addEmployees(chefNum, waiterNum, managerNum, chefSalary, waiterSalary, managerSalary)
    restaurant.addTables(table2, table4, table6, table8)
    restaurant.addGuests(avgGuestperHour)

    # to tylko do kontroli czy klientów poprawnie dodaje (do tego momętu działa
    for groupofpeople in restaurant.allguestList:
        print("Liczba gosci" + str(groupofpeople.numberofGuests))
        print("czas przybycia: " + str(groupofpeople.arrival))
        for client in groupofpeople.listofPeople:
            print("id klienta:" + str(client.clientID) + " id grupy" + str(client.groupID))

    czasdzialania = 0
    czaszamkniecia = restaurant.workHours() * 60  # pentla będzie co minutę

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
    czyotwarte = True
    czygosciewsrodku = True

    print(str(restaurant.workHours()))

    while czyotwarte or czygosciewsrodku:  # działa w czasie pracy i jak są klienci
        # print("@@@@@@@@@@@@@@@@@@@@@@@@")
        # print((czasdzialania <= czaszamkniecia))
        # print((restaurant.guestInside()))
        # print((czasdzialania <= czaszamkniecia or restaurant.guestInside()!=0))
        # print("$$$$$$$$$$$$$$$$$$$$$$$$")
        chef = chefNum
        kelnerzy = waiterNum
        menagers = managerNum
        # print("liczba kucharzy: "+str(chef))

        for groupofpeople in restaurant.allguestList:
            # sprawdzamy czy czas przyjścia grupy nadszedł
            # jśli tak to przerzucamy ich do kolejki
            if groupofpeople.arrival == czasdzialania:
                restaurant.waitlineguestList.append(groupofpeople)
                restaurant.allguestList.remove(groupofpeople)
                print("czas działania" + str(czasdzialania))
                for client in groupofpeople.listofPeople:
                    print("klient: " + str(client.clientID) + "przyszedł")

        # dostępni menagerzy
        # (na razie zakładam że menagerzy zawsze dostępni czyli czas obsługi =1 minuta)

        if czasdzialania == czaszamkniecia:
            restaurant.waitlineguestList.clear()

        dlugkolejki = len(restaurant.waitlineguestList)
        print("czas działania" + str(czasdzialania))
        print("Długość kolejki: " + str(dlugkolejki))
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
                            # print("Stol: " + str(table.tableID) + "zajety")
                            # print("Stol: " + str(table.chairs))

                            break

        # rezygnowanie z kolejki

        for groupofpeople in restaurant.waitlineguestList:  # jeśli dalej stoją w kolejce
            groupofpeople.timewaited += 1  # zwiększamy czas jaki stoją
            if groupofpeople.resignorNot():  # sprawdzamy czy są dalej cierpliwi
                restaurant.waitlineguestList.remove(groupofpeople)  # jeśli nie są to wywalamy ich z kolejki

        # dostarczanie zamówień
        zamówienia = len(restaurant.orderlist)

        if zamówienia > 0:
            for order in restaurant.orderlist:
                if kelnerzy > 0 and order.isReady():
                    kelnerzy -= 1
                    for table in restaurant.filledTablesList:
                        if table.tableID == order.tableID:
                            for client in table.guestList:
                                # dostarczenie zamówienia klientowi:
                                if client.clientID == order.klientID:
                                    client.clientStatus = 1
                                    timeofeating = randint(3, 10)
                                    client.clientEatTime = timeofeating
                                    restaurant.revenue += order.cena  # tymczasowo
                                    restaurant.orderlist.remove(order)  # usunięcie zamówienia z listy zamówień
                                    break
        print("kelnerzy po obsłudze zamówień:"+str(kelnerzy))

        # jedzenie
        for table in restaurant.filledTablesList:
            for client in table.guestList:
                if client.clientStatus == 1:
                    client.clientEatTime -= 1
                    if client.clientEatTime <= 0:
                        client.clientStatus = 2

        # koniec jedzenia i wyjście klientów
        for table in restaurant.filledTablesList:

            if table.finishedEating():
                print("----------------")
                for table in restaurant.filledTablesList:
                    print("id stołu zajętego: " + str(table.tableID))
                    print("status stołu: " + str(table.status))
                print("----------------")
                table.emptyTable()
                table.status = False
                print(table.guestList)
                print(table.status)
                print("Stol: " + str(table.tableID) + "zwolniony")
                print("----------------")
                restaurant.unservTablesList.append(table)
                restaurant.filledTablesList.remove(table)
                for table in restaurant.filledTablesList:
                    print("id stołu zajętego: " + str(table.tableID))
                    print("status stołu: " + str(table.status))
                print("----------------")
                for table in restaurant.unservTablesList:
                    print("id stołu wolnego: " + str(table.tableID))
                    print("status stołu: " + str(table.status))
                print("----------------")
                print("a")

        # zamówienia

        if kelnerzy > 0:
            for table in restaurant.filledTablesList:
                if kelnerzy > 0:
                    if table.orderTaken == False:  # jeśli stolik nie złożył zamówienia
                        table.orderTaken=True
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

        if zamówienia > 0:
            for order in restaurant.orderlist:
                if chef > 0:
                    if not order.isReady():  # jeśli zamówienie nie jest skończone i jest dostępny szef to zmniejszamy jego czas o minutę
                        chef = chef - 1
                        order.czas -= 1

        czasdzialania += 1
        if czasdzialania == czaszamkniecia:
            czyotwarte = False

        # print("^^^"+str(restaurant.guestInside())+"^^^")
        if restaurant.guestInside() == 0:
            czygosciewsrodku = False
        elif restaurant.guestInside() != 0:
            czygosciewsrodku = True

        print("ilosć zamówień: " + str(len(restaurant.orderlist)))
        print("12121")
        for table in restaurant.filledTablesList:

            print("id stołu: " + str(table.tableID))
            print("status stołu: " + str(table.status))
        print("222222")
        if czasdzialania> czaszamkniecia+60:
            break
    # później można nadgodziny wziąć
    chefcost = chefNum * chefSalary * restaurant.workHours() + menagers * managerSalary * restaurant.workHours()
    menagercost = managerNum * managerSalary * restaurant.workHours()
    waitercost = waiterNum * waiterSalary * restaurant.workHours()
    print("koszt kelnerów: " + str(waitercost))
    print("koszt kucharzy: " + str(chefcost))
    print("koszt menagerów: " + str(menagercost))
    allcost = chefcost + menagercost + waitercost
    print("wszstkie koszty: " + str(allcost))
    print("dochód: " + str(restaurant.revenue))
    adjusted_revenue = restaurant.revenue - allcost
    print("dochód po kosztach: " + str(adjusted_revenue))


if __name__ == "__main__":
    main()

# ---------------------------------------------------------------------------------------------------------------------------------------------
