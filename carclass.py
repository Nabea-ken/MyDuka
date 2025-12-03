""" 1.Create a Car Class
Have the following attributes
- brand - model - year -fuel_capcity - fuel_level -is_running(boolen value)
Have the methods
- start()
- stop()
- refuel()
- drive()
- display_car_info() """

class Car:
    def __init__(self,brand,model,year,fuel_capacity,fuel_level,is_running=False):
        self.brand = brand
        self.model = model
        self.year = year
        self.fuel_capacity = fuel_capacity
        self.fuel_level = fuel_level
        self.battery_level = 100
        self.is_running=is_running

    def start(self):
        if self.battery_level<10:
            print("Car cannot start! Batter low!")
            return
    
        if self.fuel_level>0:
            self.is_running=True
            self.battery_level-=3
            print(f"{self.brand} {self.model} has started.")
        else:
            print("Fuel tank empty! cannot start!")
    
    def stop(self):
        self.is_running=False
        print(f"{self.brand} {self.model} has stopped.")

    def refuel(self,amount):
        if amount<=0:
            print("Refuel amount should be positive.")
            return
        if self.fuel_level+amount>self.fuel_capacity:
            print("Max Capacity! Tank overflow!")
            self.fuel_level=self.fuel_capacity
        else:
            self.fuel_level+=amount
            print(f"Fuel level: {self.fuel_level}/{self.fuel_capacity}Ltrs")
        
    def charge_battery(self,amount):
        if amount<=0:
            print("Charging amount should be positive.")
            return
        
        self.battery_level+=amount

        if self.battery_level>100:
            self.battery_level=100

        print(f"Battery charged to {self.battery_level}%")
        
    def drive(self,distance):
        if not self.is_running:
            print("Start the car.")
            return
        
        fuel_needed=distance*0.1
        battery_drain=distance*0.05
        battery_charge=distance*0.03

        if fuel_needed>self.fuel_level:
            print("Not enough fuel to cover distance!")
            return
        
        net_battery=battery_drain-battery_charge

        if net_battery>self.battery_level:
            print("Battery Low!")
            return
        
        self.fuel_level-=fuel_needed
        self.battery_level-=net_battery

        if self.battery_level<0:
            self.battery_level=0

        print(f"Car drove:{distance}km. Fuel:{self.fuel_level:.2f}Ltrs. Battery:{self.battery_level:.2f}%")

    def display_car_info(self):
        print("\n--- My Car Info --- ")
        print(f"Brand:{self.brand}")
        print(f"Model:{self.model}")
        print(f"Year:{self.year}")
        print(f"Fuel Level:{self.fuel_level}/{self.fuel_capacity}")
        print(f"Battery Level:{self.battery_level}%")
        print(f"Is car Running:{self.is_running}")
        print("--------------------------\n")
       

car1 = Car("Toyota", "Corolla", 2015, 50, 10)
car2 = Car("BMW", "X5", 2021, 70, 30)
car3 = Car("Honda", "Civic", 2020, 45, 5)

car1.display_car_info()
car1.start()
car1.drive(20)
car1.stop()
print(" ")
car2.refuel(20)
car2.start()
car2.drive(50)
car2.display_car_info()
print(" ")
car3.start()
car3.refuel(30)
car3.start()
car3.drive(15)
car3.display_car_info()
print(" ")
