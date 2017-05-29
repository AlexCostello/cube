from cube import BasicCube, BenefitCube
from options import Options

'''
Person class has the following attributes:
-age
-sex
-classification
-uwScore
'''
class Person:

    def __init__(self):
        self.basic_cube = BasicCube()
        self.benefit_cube = BenefitCube()
        self.maturing_benefit_array = []
        self.stored_cubes_array = []
        self.month = 1
        self.age = 0
        self.options = Options()

    def get_balance(self):
        maturing_value = 0
        for cube in self.maturing_benefit_array:
            maturing_value += cube.mv_actual

        maturing_value -= self.benefit_cube.premium
        return maturing_value

    def calculate_basic_cube(self, basic_cube, benefit_cube):
        basic_cube.premium = basic_cube.deposit
        basic_cube.benefit = 0

        for cube in self.maturing_benefit_array:
            basic_cube.premium += cube.mv_actual
            if cube.type == 0:
                basic_cube.benefit += cube.benefit

        if self.month == 1:
            basic_cube.benefit = self.options.initial_benefit
            basic_cube.premium += self.options.initial_deposit

        basic_cube.premium -= benefit_cube.premium

        balance = self.get_balance()

        basic_cube.mv_actual = self.calculate_mv(self.age, self.month, basic_cube.maturity,
                                                 basic_cube.deposit, balance, basic_cube.benefit)
        return basic_cube

    def calculate_mv(self, age, month, maturity, deposit, balance, benefit):
        if month == 1:
            deposit += self.options.initial_deposit
        maturity_value = deposit * (1 - self.options.premload_new) + balance * (1 - self.options.preload_renew)
        i = 0
        while i < maturity:
            MortIndex = int((age*12 + i + (month-1)) / 12)
            rate = self.options.getRate(MortIndex)/1000
            maturity_value = (maturity_value * (1 + self.options.month_int) + (maturity_value - benefit) * rate)
            i += 1
        maturity_value = round(maturity_value, 2)
        return maturity_value

    def calculate_benefit_cube(self, benefit_cube):
        benefit_cube.premium = benefit_cube.mv_goal
        for cube in self.maturing_benefit_array:
            if cube.type == 1:
                benefit_cube.benefit += cube.benefit
        benefit_cube.premium = 10

        benefit_cube.mv_actual = benefit_cube.mv_goal

        return benefit_cube

    def calculate_premium(self):