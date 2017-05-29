import sqlite3

class Options:

    def __init__(self):
        self.preload_renew = 0
        self.premload_new = 0
        self.month_int = .003333
        self.max_month = 350
        self.mort_table = sqlite3.connect("mortality.db")
        self.initial_deposit = 25
        self.initial_benefit = 5000

    def getRate(self, age):
        c = self.mort_table.cursor()
        command = "SELECT RATE FROM mortality WHERE AGE='" + str(age) + "';"
        c.execute(command)
        result = c.fetchall()
        rate = result[0][0]
        return rate