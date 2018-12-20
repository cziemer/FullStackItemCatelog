from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import CarMake, Base, CarModel

engine = create_engine('sqlite:///carlist.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()


# Models for Ford
make1 = CarMake(name="Ford", creator="christopher.ziemer@gmail.")

session.add(make1)
session.commit()

model1 = CarModel(name="Fiesta", url="https://www.ford.com/cars/fiesta/", msrp="14260", 
					carType="Coupe", carmake=make1, creator="christopher.ziemer@gmail.")
session.add(model1)
session.commit()

model2 = CarModel(name="Focus", url="https://www.ford.com/cars/focus/", msrp="17950", 
					carType="Coupe", carmake=make1, creator="christopher.ziemer@gmail.")
session.add(model2)
session.commit()

model3 = CarModel(name="Mustang", url="https://www.ford.com/cars/mustang/", msrp="26120", 
					carType="Performance", carmake=make1, creator="christopher.ziemer@gmail.com")
session.add(model3)
session.commit()

model4 = CarModel(name="Edge", url="https://www.ford.com/suvs-crossovers/edge/", msrp="29995", 
					carType="SUV", carmake=make1, creator="christopher.ziemer@gmail.com")
session.add(model4)
session.commit()

model5 = CarModel(name="Explorer", url="https://www.ford.com/suvs/explorer/", 
					msrp="32365", carType="SUV", carmake=make1, creator="christopher.ziemer@gmail.com")
session.add(model5)
session.commit()

model6 = CarModel(name="Expedition", url="https://www.ford.com/suvs/expedition/", msrp="51790", 
					carType="SUV", carmake=make1, creator="christopher.ziemer@gmail.com")
session.add(model6)
session.commit()

model7 = CarModel(name="Ranger", url="https://www.ford.com/trucks/ranger/", msrp="24000", 
					carType="Truck", carmake=make1, creator="christopher.ziemer@gmail.com")
session.add(model7)
session.commit()

model8 = CarModel(name="F-150", url="https://www.ford.com/trucks/f150/", msrp="28155", 
					carType="Truck", carmake=make1, creator="christopher.ziemer@gmail.com")
session.add(model8)
session.commit()

# Models for Chevrolet
make2 = CarMake(name="Chevrolet", creator="christopher.ziemer@gmail.com")

session.add(make2)
session.commit()

model1 = CarModel(name="Spark", url="https://www.chevrolet.com/cars/spark-subcompact-car", 
					msrp="13220", carType="Coupe", carmake=make2, creator="christopher.ziemer@gmail.com")
session.add(model1)
session.commit()

model2 = CarModel(name="Malibu", url="https://www.chevrolet.com/cars/malibu-mid-size-car", 
					msrp="22090", carType="Coupe", carmake=make2, creator="christopher.ziemer@gmail.com")
session.add(model2)
session.commit()

model3 = CarModel(name="Camaro", url="https://www.chevrolet.com/performance/camaro-sports-car", 
					msrp="25000", carType="Performance", carmake=make2, creator="christopher.ziemer@gmail.com")
session.add(model3)
session.commit()

model4 = CarModel(name="Corvette", url="https://www.chevrolet.com/performance/corvette-stingray-sports-car", 
					msrp="55495", carType="Performance", carmake=make2, creator="christopher.ziemer@gmail.com")
session.add(model4)
session.commit()

model5 = CarModel(name="Equinox", url="https://www.chevrolet.com/suvs/equinox-small-suv", msrp="23800", 
					carType="SUV", carmake=make2, creator="christopher.ziemer@gmail.com")
session.add(model5)
session.commit()

model6 = CarModel(name="Traverse", url="https://www.chevrolet.com/suvs/traverse-mid-size-suv", 
					msrp="29930", carType="SUV", carmake=make2, creator="christopher.ziemer@gmail.com")
session.add(model6)
session.commit()

model7 = CarModel(name="Tahoe", url="https://www.chevrolet.com/suvs/tahoe", msrp="47900", 
					carType="SUV", carmake=make2, creator="christopher.ziemer@gmail.com")
session.add(model7)
session.commit()

model8 = CarModel(name="Silverado", url="https://www.chevrolet.com/silverado-pickup-trucks", msrp="34600", 
					carType="Truck", carmake=make2, creator="christopher.ziemer@gmail.com")
session.add(model8)
session.commit()

# Models for Lincoln
make3 = CarMake(name="Lincoln", creator="christopher.ziemer@gmail.com")

session.add(make3)
session.commit()

model1 = CarModel(name="MKZ", url="https://www.lincoln.com/luxury-cars/mkz/", msrp="35995", 
					carType="Coupe", carmake=make3, creator="christopher.ziemer@gmail.com")
session.add(model1)
session.commit()

model2 = CarModel(name="Continental", url="https://www.lincoln.com/luxury-cars/continental/", 
					msrp="46145", carType="Coupe", carmake=make3, creator="christopher.ziemer@gmail.com")
session.add(model2)
session.commit()

model3 = CarModel(name="MKT", url="https://www.lincoln.com/Lincoln/MKT", msrp="49500", 
					carType="SUV", carmake=make3, creator="christopher.ziemer@gmail.com")
session.add(model3)
session.commit()

model4 = CarModel(name="MKX", url="https://www.lincoln.com/Lincoln/MKX", msrp="39035", 
					carType="SUV", carmake=make3, creator="christopher.ziemer@gmail.com")
session.add(model4)
session.commit()

model5 = CarModel(name="Navigator", url="https://www.lincoln.com/Lincoln/Navigator", 
					msrp="73205", carType="SUV", carmake=make3, creator="christopher.ziemer@gmail.com")
session.add(model5)
session.commit()

# Models for Toyota
make4 = CarMake(name="Toyota", creator="christopher.ziemer@gmail.com")

session.add(make4)
session.commit()

model1 = CarModel(name="Camry", url="https://www.toyota.com/Toyota/Camry", 
					msrp="23845", carType="Coupe", carmake=make4, creator="christopher.ziemer@gmail.com")
session.add(model1)
session.commit()

model2 = CarModel(name="86", url="https://www.toyota.com/86", msrp="26455", 
					carType="Performance", carmake=make4, creator="christopher.ziemer@gmail.com")
session.add(model2)
session.commit()

model3 = CarModel(name="4Runner", url="https://www.toyota.com/4runner/", msrp="34910", 
					carType="SUV", carmake=make4, creator="christopher.ziemer@gmail.com")
session.add(model3)
session.commit()

model4 = CarModel(name="Land Cruiser", url="https://www.toyota.com/landcruiser/", 
					msrp="84765", carType="SUV", carmake=make4, creator="christopher.ziemer@gmail.com")
session.add(model4)
session.commit()

# Models for Nissan
make5 = CarMake(name="Nissan", creator="christopher.ziemer@gmail.com")

session.add(make5)
session.commit()

model1 = CarModel(name="Maxima", url="https://www.nissanusa.com/vehicles/cars/maxima.html", 
					msrp="33420", carType="Coupe", carmake=make5, creator="christopher.ziemer@gmail.com")
session.add(model1)
session.commit()

model2 = CarModel(name="Sentra", url="https://www.nissanusa.com/Sentra", msrp="17790", 
					carType="Coupe", carmake=make5, creator="christopher.ziemer@gmail.com")
session.add(model2)
session.commit()

model3 = CarModel(name="Altima", url="https://www.nissanusa.com/Altima", msrp="23260", 
					carType="Coupe", carmake=make5, creator="christopher.ziemer@gmail.com")
session.add(model3)
session.commit()

model4 = CarModel(name="Rogue", url="https://www.nissanusa.com/Rogue", msrp="24800", 
					carType="SUV", carmake=make5, creator="christopher.ziemer@gmail.com")
session.add(model4)
session.commit()

model5 = CarModel(name="Juke", url="https://www.nissanusa.com/vehicles/discontinued/juke.html", 
					msrp="20250", carType="SUV", carmake=make5, creator="christopher.ziemer@gmail.com")
session.add(model5)
session.commit()

# Models for Honda
make6 = CarMake(name="Honda", creator="christopher.ziemer@gmail.com")

session.add(make6)
session.commit()

model1 = CarModel(name="Accord", url="https://www.honda.com/Accord", msrp="23570", 
					carType="Coupe", carmake=make6, creator="christopher.ziemer@gmail.com")
session.add(model1)
session.commit()

model2 = CarModel(name="CR-V", url="https://www.honda.com/CR-V", msrp="24250", 
					carType="SUV", carmake=make6, creator="christopher.ziemer@gmail.com")
session.add(model2)
session.commit()

model3 = CarModel(name="Pilot", url="https://www.honda.com/Pilot", msrp="31450", 
					carType="SUV", carmake=make6, creator="christopher.ziemer@gmail.com")
session.add(model3)
session.commit()

# Models for Dodge
make7 = CarMake(name="Dodge", creator="christopher.ziemer@gmail.com")

session.add(make7)
session.commit()

model1 = CarModel(name="Challenger", url="https://www.dodge.com/challenger.html", msrp="27595", 
					carType="Performance", carmake=make7, creator="christopher.ziemer@gmail.com")
session.add(model1)
session.commit()

model2 = CarModel(name="Charger", url="https://www.dodge.com/charger.html", msrp="28995", 
					carType="Performance", carmake=make7, creator="christopher.ziemer@gmail.com")
session.add(model2)
session.commit()

model3 = CarModel(name="Durango", url="https://www.dodge.com/durango.html", msrp="29995", 
					carType="SUV", carmake=make7, creator="christopher.ziemer@gmail.com")
session.add(model3)
session.commit()

print "added all car models!"