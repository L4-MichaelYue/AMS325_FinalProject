from sklearn import linear_model
import numpy as np
import pandas as pd
import tkinter as Tk
import datetime

def estimate(name,age,km_driven,fuel,seller_type,transmission,owner):
    #clean data
    def first_word(s):
        s = s.strip()
        for i in range(len(s)):
            if s[i] == ' ':
                return s[:i]
        return s

    df_car = pd.read_csv("CAR DETAILS FROM CAR DEKHO.csv")

    name = first_word(name)

    df_car['first'] = df_car.name.apply(first_word)
    now = datetime.datetime.now().year
    age = now - int(age)
    df_car['year'] = 2022 - df_car.year

    df = df_car[df_car['first'] == name]
    #detect errors
    if len(df) < 20:
        return "Not enough data for this name"
    if int(age) <0:
        return "Can't have future car"
    if int(km_driven) <0:
        return "km driven can't be negative"
    if len(df[df['fuel'] == fuel]) == 0:
        return "No data for this fuel"
    if len(df[df['seller_type'] == seller_type]) == 0:
        return "No data for this seller_type"
    if len(df[df['transmission'] == transmission]) == 0:
        return "No data for this transmission"
    if len(df[df['owner'] == owner]) == 0:
        return "No data for this owner"
    #get dummy
    df_fuel = pd.get_dummies(df.fuel,drop_first=True)
    df_seller = pd.get_dummies(df.seller_type,drop_first=True)
    df_transmission = pd.get_dummies(df.transmission,drop_first=True)
    df_owner = pd.get_dummies(df.owner,drop_first=True)
    df_age = df.year 
    df_km_driven = df.km_driven

    df_data = pd.concat([df_fuel,df_seller,df_transmission,df_age,df_owner,df_km_driven], axis=1, join='inner')

    X = df_data

    y = np.log(df.selling_price)
    # it was test for whether model make sense
    # X_train, X_test, y_train, y_test = model_selection.train_test_split(X, y,train_size = 0.7)

    model = linear_model.LinearRegression()
    model.fit(X, y)

    df2 = X[0:0].copy()
    dict = {"km_driven": km_driven,
                        # fuel: 1,
                        # seller_type: 1,
                        # transmission:1,
                        # owner:1,
                        'year':age
                        }
    if fuel in df2.columns:
        dict[fuel] = 1
    if seller_type in df2.columns:
        dict[seller_type] = 1
    if transmission in df2.columns:
        dict[transmission] = 1
    if owner in df2.columns:
        dict[owner] = 1
    df2 = df2.append(dict,ignore_index=True)
    df2 = df2.fillna(0)
    s = np.exp(model.predict(df2))
    return('The estimate value is %d Rupees, which equal to %d dollars' %(s,0.012*s))

class Response:
    def __init__(self, parent, main_obj):
        self.parent = parent
        self.main_obj = main_obj
        
        self.frame = Tk.Frame(self.parent)
        self.frame.pack(fill=Tk.BOTH, expand=1)
        
        name = self.main_obj.field_name.get()
        age = self.main_obj.field_year.get()
        km_driven = self.main_obj.field_km_driven.get()
        fuel = self.main_obj.field_fuel.get()
        seller_type = self.main_obj.field_seller_type.get()
        transmission = self.main_obj.field_transmission.get()
        owner = self.main_obj.field_owner.get()
        
        result = estimate(name,age,km_driven,fuel,seller_type,transmission,owner)
        
        self.label = Tk.Label(self.frame, text=result)
        self.label.grid(row=0, column=0, sticky=Tk.W)

        self.frame_buttons = Tk.Frame(self.parent)
        self.frame_buttons.pack(fill=Tk.BOTH, expand=1)
        
        self.ok_button = Tk.Button(self.frame_buttons, text="Ok", command=self._ok)
        self.ok_button.pack(side=Tk.RIGHT, padx=5, pady=5)
        
    def _ok(self):
        self.parent.destroy()

class MyGUI2:
    def __init__(self, parent):
        self.parent = parent
        #name
        self.frame_name = Tk.Frame(self.parent)
        self.frame_name.pack(fill=Tk.BOTH, expand=1)                                                                        
        
        self.label_name = Tk.Label(self.frame_name, text="name")
        self.label_name.grid(row=0, column=0, sticky=Tk.W)
        
        self.label_str = Tk.StringVar()
        
        self.field_name = Tk.Entry(self.frame_name, textvariable=self.label_str)
        self.field_name.grid(row=0, column=1, sticky=Tk.W)
        #year
        self.frame_year = Tk.Frame(self.parent)
        self.frame_year.pack(fill=Tk.BOTH, expand=1)                                                                        
        
        self.label_year = Tk.Label(self.frame_year, text="year")
        self.label_year.grid(row=1, column=0, sticky=Tk.W)
        
        self.label_str = Tk.StringVar()
        
        self.field_year = Tk.Entry(self.frame_year, textvariable=self.label_str)
        self.field_year.grid(row=1, column=1, sticky=Tk.W)
        #km_driven
        self.frame_km_driven = Tk.Frame(self.parent)
        self.frame_km_driven.pack(fill=Tk.BOTH, expand=1)                                                                        
        
        self.label_km_driven = Tk.Label(self.frame_km_driven, text="km_driven")
        self.label_km_driven.grid(row=2, column=0, sticky=Tk.W)
        
        self.label_str = Tk.StringVar()
        
        self.field_km_driven = Tk.Entry(self.frame_km_driven, textvariable=self.label_str)
        self.field_km_driven.grid(row=2, column=1, sticky=Tk.W)
        #fuel
        self.frame_fuel = Tk.Frame(self.parent)
        self.frame_fuel.pack(fill=Tk.BOTH, expand=1)                                                                        
        
        self.label_fuel = Tk.Label(self.frame_fuel, text="fuel")
        self.label_fuel.grid(row=3, column=0, sticky=Tk.W)
        
        self.label_str = Tk.StringVar()
        
        self.field_fuel = Tk.Entry(self.frame_fuel, textvariable=self.label_str)
        self.field_fuel.grid(row=3, column=1, sticky=Tk.W)
        #seller_type
        self.frame_seller_type = Tk.Frame(self.parent)
        self.frame_seller_type.pack(fill=Tk.BOTH, expand=1)                                                                        
        
        self.label_seller_type = Tk.Label(self.frame_seller_type, text="seller_type")
        self.label_seller_type.grid(row=4, column=0, sticky=Tk.W)
        
        self.label_str = Tk.StringVar()
        
        self.field_seller_type = Tk.Entry(self.frame_seller_type, textvariable=self.label_str)
        self.field_seller_type.grid(row=4, column=1, sticky=Tk.W)
        #transmission
        self.frame_transmission = Tk.Frame(self.parent)
        self.frame_transmission.pack(fill=Tk.BOTH, expand=1)                                                                        
        
        self.label_transmission = Tk.Label(self.frame_transmission, text="transmission")
        self.label_transmission.grid(row=5, column=0, sticky=Tk.W)
        
        self.label_str = Tk.StringVar()
        
        self.field_transmission = Tk.Entry(self.frame_transmission, textvariable=self.label_str)
        self.field_transmission.grid(row=5, column=1, sticky=Tk.W)
        #owner
        self.frame_owner = Tk.Frame(self.parent)
        self.frame_owner.pack(fill=Tk.BOTH, expand=1)                                                                        
        
        self.label_owner = Tk.Label(self.frame_owner, text="owner")
        self.label_owner.grid(row=5, column=0, sticky=Tk.W)
        
        self.label_str = Tk.StringVar()
        
        self.field_owner = Tk.Entry(self.frame_owner, textvariable=self.label_str)
        self.field_owner.grid(row=5, column=1, sticky=Tk.W)
        
        #bottom
        self.frame_buttons = Tk.Frame(self.parent)
        self.frame_buttons.pack(fill=Tk.BOTH, expand=1)

        self.show_button = Tk.Button(self.frame_buttons, text="show", command=self._show)
        self.show_button.pack(side=Tk.RIGHT, padx=5, pady=5)
        
    def _show(self):
        self.new_window = Tk.Toplevel(self.parent)
        self.show = Response(self.new_window, self)

root = Tk.Tk()
root.wm_title("Car prediction")

gui_test = MyGUI2(root)

root.mainloop()