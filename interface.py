"""
This module contains all the information needed to display the cube graphic user interface. 
"""
#import tkinter as tk
from person import Person
from tkinter import Tk, Frame, Label, Button, Entry, E, W, messagebox, OptionMenu, StringVar, ttk, END

#GLOBAL VARS
person = Person()

class Page(Frame):

    def __init__(self, *args, **kwargs):
        Frame.__init__(self, *args, **kwargs)

    def show(self):
        self.lift()


class PersonPage(Page):

    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)

        # WEIGHTING #
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(3, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(7, weight=1)

        # LABELS #
        Label(self, text="Enter Individual Attributes").grid(row=1, column=1, columnspan=2)
        Label(self, text="Sex").grid(row=2, column=1, sticky=E)
        Label(self, text="Age").grid(row=3, column=1, sticky=E)
        Label(self, text="Class").grid(row=4, column=1, sticky=E)
        Label(self, text="UW Score").grid(row=5, column=1, sticky=E)

        # ENTRY BOXES #
        self.sex = StringVar(self)
        self.sex.set("Male")
        sex_entry = OptionMenu(self, self.sex, "Male", "Female")
        sex_entry.grid(row=2, column=2)
        self.age_entry = Entry(self)
        self.age_entry.grid(row=3, column=2)
        self.class_opt = StringVar(self)
        self.class_opt.set("Non-Smoker")
        class_entry = OptionMenu(self, self.class_opt, "Non-Smoker", "Smoker")
        class_entry.grid(row=4, column=2)
        self.uw_entry = Entry(self)
        self.uw_entry.grid(row=5, column=2)

        # BUTTONS #
        Button(self, text="Set Default", command=self.set_defaults, width=15)\
                               .grid(row=6, column=1, sticky=E+W)
        Button(self, text="Submit", command=self.set_vals)\
                               .grid(row=6, column=2, sticky=E+W)

    def set_defaults(self):
        person.sex = "male"
        person.age = 35
        person.classification = "Non-smoker"
        person.uwScore = 100
        messagebox.showinfo("Information", "Person created.\nSex: %s \nAge: %d\nClass: %s\nUW Score: %d"
                            % (person.sex, person.age, person.classification, person.uwScore))

    def set_vals(self):
        sex_entry = self.sex.get()
        age_entry = self.age_entry.get()
        class_entry = self.class_opt.get()
        uw_entry = self.uw_entry.get()
        error = 0

        try:
            age_entry = int(age_entry)
            if 0 < age_entry < 121:
                person.age = age_entry
            else:
                messagebox.showerror("Error", "Invalid age input.\nEnter number between 0 and 120")
                error=1

        except ValueError as ex:
            messagebox.showerror("Error", "Invalid age input.\nEnter number between 0 and 120")
            error = 1

        try:
            uw_entry = int(uw_entry)

        except ValueError as ex:
            messagebox.showerror("Error", "Invalid UW score entered")
            error = 1

        if not error:
            person.sex = sex_entry
            person.classification = class_entry
            person.uwScore = uw_entry
            messagebox.showinfo("Information", "Person created.\nSex: %s \nAge: %d\nClass: %s\nUW Score: %d"
                                % (person.sex, person.age, person.classification, person.uwScore))


class CubeGenerator(Page):

    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)

        self.person = person

        # Weights #
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(3, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)

        # Frames #
        self.basic_frame = BasicFrame(self)
        self.benefit_frame = BenefitFrame(self)
        self.stash_frame = Frame(self)

        # Place Frames in Grid #
        self.basic_frame.grid(row=1, column=1)
        self.benefit_frame.grid(row=1, column=2)
        self.stash_frame.grid(row=2, column=1, columnspan=2)

        # Stash Frame Set Up #
        Label(self.stash_frame, text="Stashed Cubes").grid(row=0, column=0)
        self.generate_stash()

    def parse_entry(self, entry):
        parsed_entry = entry.translate({ord(c): None for c in '!@#$'})
        try:
            parsed_entry = int(parsed_entry)
        except ValueError as ex:
            parsed_entry = 0
        return parsed_entry

    def calculate_basic(self):
        self.person.basic_cube.deposit = int(self.basic_frame.deposit.get())
        self.person.basic_cube.cube_clone(self.person.calculate_basic_cube(self.person.basic_cube,
                                                                           self.person.benefit_cube))
        self.basic_frame.premium.config(text=self.person.basic_cube.premium)
        self.basic_frame.benefit.config(text=self.person.basic_cube.benefit)
        self.basic_frame.maturity_value.config(text=self.person.basic_cube.mv_actual)

    def calculate_benefit(self):
        self.person.benefit_cube.maturity = self.parse_entry(self.benefit_frame.maturity.get())
        self.person.benefit_cube.mv_goal = self.parse_entry(self.benefit_frame.mv_goal.get())
        self.person.benefit_cube.benefit = self.parse_entry(self.benefit_frame.benefit.get())

        self.benefit_frame.maturity.delete(0, END)
        self.benefit_frame.maturity.insert(0, self.person.benefit_cube.maturity)
        self.benefit_frame.mv_goal.delete(0, END)
        self.benefit_frame.mv_goal.insert(0, self.person.benefit_cube.mv_goal)
        self.benefit_frame.benefit.delete(0, END)
        self.benefit_frame.benefit.insert(0, self.person.benefit_cube.benefit)

    def calculate_cubes(self):

        self.calculate_basic()
        self.calculate_benefit()


    def stash_cubes(self):
        print("Stashing...")

    def generate_stash(self):
        stash_header = ['Maturity', 'Premium', 'MV Goal', 'Benefit', 'Maturity Value']
        self.stash_frame.cube_stash = ttk.Treeview(self.stash_frame, height=5, column=stash_header, show='headings')
        for col in stash_header:
            self.stash_frame.cube_stash.heading(col, text=col.title())
            self.stash_frame.cube_stash.column(col, width=90)

        self.stash_frame.cube_stash.grid(row=1, column=0)


class BasicFrame(Frame):
    def __init__(self, *args, **kwargs):
        Frame.__init__(self, *args, **kwargs)
        # Basic Frame Set Up #
        # Immutable Labels #
        Label(self, text="Basic Cube", font=14).grid(row=0, column=0, columnspan=2)
        Label(self, text="Maturity").grid(row=1, column=0, sticky=E, padx=5)
        Label(self, text="Deposit").grid(row=2, column=0, sticky=E, padx=5)
        Label(self, text="Premium").grid(row=3, column=0, sticky=E, padx=5)
        Label(self, text="Benefit").grid(row=4, column=0, sticky=E, padx=5)
        Label(self, text="Maturity Value").grid(row=5, column=0, sticky=E, padx=5)

        # Mutable Labels #
        self.maturity = Label(self, text="1").grid(row=1, column=1, sticky=W)
        self.premium = Label(self, text="$0.00")
        self.premium.grid(row=3, column=1, sticky=W)
        self.benefit = Label(self, text="$0.00")
        self.benefit.grid(row=4, column=1, sticky=W)
        self.maturity_value = Label(self, text="$0.00")
        self.maturity_value.grid(row=5, column=1, sticky=W)

        # Entry Fields #
        self.deposit = Entry(self, width=10)
        self.deposit.grid(row=2, column=1)

        # Buttons #
        self.calculate_button = Button(self, text="Calculate Cubes", command=self.master.calculate_cubes)
        self.calculate_button.grid(row=6, column=0, columnspan=2, sticky=E + W)


class BenefitFrame(Frame):
    def __init__(self, *args, **kwargs):
        Frame.__init__(self, *args, **kwargs)

        # Benefit Frame Set Up #
        # Immutable Labels #
        Label(self, text="Benefit Cube", font=14).grid(row=0, column=0, columnspan=2)
        Label(self, text="Maturity").grid(row=1, column=0, sticky=E)
        Label(self, text="Premium").grid(row=2, column=0, sticky=E)
        Label(self, text="Maturity Value Goal").grid(row=3, column=0, sticky=E)
        Label(self, text="Benefit").grid(row=4, column=0, sticky=E)
        Label(self, text="Maturity Value").grid(row=5, column=0, sticky=E)

        # Mutable Labels #
        self.premium = Label(self, text="$0.00").grid(row=2, column=1, sticky=W)
        self.maturity_value = Label(self, text="$0.00").grid(row=5, column=1, sticky=W)

        # Entry Fields #
        self.maturity = Entry(self, width=10)
        self.mv_goal = Entry(self, width=10)
        self.benefit = Entry(self, width=10)
        self.maturity.grid(row=1, column=1, sticky=W)
        self.mv_goal.grid(row=3, column=1, sticky=W)
        self.benefit.grid(row=4, column=1, sticky=W)

        # Buttons $
        self.stash_button = Button(self, text="Stash Cubes", command=self.master.stash_cubes)
        self.stash_button.grid(row=6, column=0, columnspan=2, sticky=W + E)



class Page3(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        label = Label(self, text="This is page 3")
        label.pack(side="top", fill="both", expand=True)

class MainView(Frame):
    def __init__(self, *args, **kwargs):
        Frame.__init__(self, *args, **kwargs)
        person_page = PersonPage(self)
        cube_generator_page = CubeGenerator(self)
        p3 = Page3(self)

        buttonframe = Frame(self)
        container = Frame(self)
        buttonframe.pack(side="top", fill="x", expand=False)
        container.pack(side="top", fill="both", expand=True)

        person_page.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        cube_generator_page.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p3.place(in_=container, x=0, y=0, relwidth=1, relheight=1)

        b1 = Button(buttonframe, text="Individual Attributes", command=person_page.lift)
        b2 = Button(buttonframe, text="Cube Generation", command=cube_generator_page.lift)
        b3 = Button(buttonframe, text="Page 3", command=p3.lift)

        b1.pack(side="left", expand=True, fill="x")
        b2.pack(side="left", expand=True, fill="x")
        b3.pack(side="left", expand=True, fill="x")

        person_page.show()

if __name__ == "__main__":
    root = Tk()
    main = MainView(root)
    main.pack(side="top", fill="both", expand=True)
    root.wm_geometry("700x700")
    root.mainloop()