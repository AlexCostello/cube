class Cube:

    def __init__(self):

        self.maturity = 0
        self.premium = 0
        self.benefit = 0
        self.mv_actual = 0

    def set_purchase_date(self, month, age):
        self.month_purchased = month
        self.age_purchased = age


class BasicCube(Cube):

    def __init__(self):
        Cube.__init__(self)
        self.deposit = 0
        self.type = 1
        self.maturity = 1

    def cube_clone(self, clone):
        self.maturity = clone.maturity
        self.premium = clone.premium
        self.benefit = clone.benefit
        self.mv_actual = clone.mv_actual
        self.deposit = clone.deposit

    def cube_copy(self):
        newCube = BasicCube()
        newCube.maturity = self.maturity
        newCube.premium = self.premium
        newCube.benefit = self.benefit
        newCube.mv_actual = self.mv_actual
        newCube.deposit = self.deposit
        return newCube

class BenefitCube(Cube):

    def __init__(self):
        Cube.__init__(self)
        self.mv_goal = 0
        self.type = 1

    def cube_clone(self, clone):
        self.maturity = clone.maturity
        self.premium = clone.premium
        self.benefit = clone.benefit
        self.mv_actual = clone.mv_actual
        self.mv_goal = clone.mv_goal

    def cube_copy(self):
        newCube = BenefitCube()
        newCube.maturity = self.maturity
        newCube.premium = self.premium
        newCube.benefit = self.benefit
        newCube.mv_actual = self.mv_actual
        newCube.mv_goal = self.mv_goal
        return newCube