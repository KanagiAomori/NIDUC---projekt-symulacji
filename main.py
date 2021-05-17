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

    allTablesList = []
    unservTablesList = []
    chefList = []
    waiterList = []
    managerList = []
    busyList = []

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
        tableID=0
        for i in range(twoPerson):
            table = Table(2, tableID)
            self.allTablesList.append(table)
            self.unservTablesList.append(table)
            tableID=tableID+1

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


class Table:
    def __init__(self, chairs, id):
        self.chairs = chairs
        self.tableID=id

    status = False
    guestList = []
    # dodatkowe funkcje
    def isOpen(self):
        isopen=True
        if self.status !=0:
            isopen=False
        return isopen

    def emptyTable(self):
        self.guestList.clear()
        self.status=0

    def fillTable(self, guests):
        self.guestList=guests
        self.status=1




class Client:
    def __init__(self, patience, orderType):
        self.orderType = orderType
        self.patience = patience

    hapiness = True
    waitTime = 0


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
    # print("a")
    # test file
    # fh = FileHandler()
    # fh.read_config()
    # fh.print_config()
    typeRestaurant = "stacjonarna"
    chefNum = 5
    chefSalary = 2000
    waiterNum = 6
    waiterSalary = 2000
    managerNum = 1
    managerSalary = 2000
    restaurant = Restaurant(typeRestaurant, 8, 18)
    restaurant.addEmployees(chefNum, waiterNum, managerNum, chefSalary, waiterSalary, managerSalary)

# for i in range(100):
#     x=randint(1, 10)
#     print(x)


if __name__ == "__main__":
    main()

# ---------------------------------------------------------------------------------------------------------------------------------------------

