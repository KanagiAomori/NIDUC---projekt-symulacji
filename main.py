# --------------------------------------------------------------------------------------------------------------------
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


class Table:
    def __init__(self, chairs):
        self.chairs = chairs

    status = False
    guestList = []


class Client:
    def __init__(self, patience, orderType):
        self.orderType = orderType
        self.patience = patience

    hapiness = True
    waitTime = 0


# Symulacja:
typeRestaurant = "stacjonarna"
chefNum = 5
chefSalary = 2000
waiterNum = 6
waiterSalary = 2000
managerNum = 1
managerSalary = 2000
tableNum = 20
carNum = 0
symDays = 20
restaurant = Restaurant(typeRestaurant, 8, 18)
restaurant.addEmployees(chefNum, waiterNum, managerNum, chefSalary, waiterSalary, managerSalary)

# ---------------------------------------------------------------------------------------------------------------------------------------------

