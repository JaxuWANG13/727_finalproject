# Problem Set 3

# SETUP
from pickle import FALSE
from unicodedata import numeric


chinese_holidays = [
    ['Holiday Name', 'Date', 'Number of Days off', 'Official Public Holiday'],
    ["New Year's Day", '2022-01-01', '3 days off', False],
    ['Spring Festival', '2022-02-01', '7 days off', True],
    ['Lantern Festival', '2022-02-15', '0 days off', False],
    ['Qingming Festival', '2022-04-05', '3 days off', True],
    ['Labor Day', '2022-05-01', '5 days off', True],
    ['Dragon Boat Festival', '2022-06-03', '3 days off', True],
    ['Qixi Festival', '2022-08-04', '0 days off', True],
    ['Mid-Autumn Festival', '2022-09-10', '3 days off', True],
    ['National Day', '2022-10-01', '7 days off', False],
    ['Double Ninth Festival', '2022-10-04', '0 days off', True]
]

activities = [
    ["New Year's Day", 'Decorating Houses | Eating Dumplings'],
    ['Spring Festival', 'Exchanging Red Envelopes | Family Reunion Dinner'],
    ['Lantern Festival', 'Watching Lanterns | Eating Tangyuan'],
    ['Qingming Festival', 'Tomb Sweeping | Spring Outing'],
    ['Labor Day', 'Visiting Tourist Spots | Shopping'],
    ['Dragon Boat Festival', 'Dragon Boat Racing | Eating Zongzi'],
    ['Qixi Festival', 'Dating | Shopping'],
    ['Mid-Autumn Festival', 'Eating Mooncakes | Family Reunion Dinner'],
    ['National Day', 'Military Parade | Visiting Tourist Spots'],
    ['Double Ninth Festival', 'Climbing Mountain | Eating Chongyang Cakes']
]


# Problem 1
headers = chinese_holidays[0] 

for holiday in chinese_holidays[1:]:
    holiday[headers.index('Number of Days off')] = holiday[headers.index('Number of Days off')].replace("days off", "")
    holiday[headers.index('Number of Days off')]  = int(holiday[headers.index('Number of Days off')] )
    if int(holiday[headers.index('Number of Days off')]) == 0:
        holiday[headers.index('Official Public Holiday')] = False
    else:
        holiday[headers.index('Official Public Holiday')] = True
       

print(chinese_holidays)
# Problem 2
num_holidays = 0

for holiday in chinese_holidays[1:]:
    oph = holiday[headers.index('Official Public Holiday')]
    if oph == True:
        num_holidays += 1

print(num_holidays)




# Problem 3
public_holidays = []
other_holidays = []

for holiday in chinese_holidays[1:]:
    if holiday[3] == True:
        public_holidays.append(holiday[0])
    else:
         other_holidays.append(holiday[0])
print(public_holidays)
print(other_holidays)


# Problem 4
long_break = []
medium_break = []
short_break = []
no_break = []

headers = chinese_holidays[0] 

for holiday in chinese_holidays[1:]:
     dof = holiday[headers.index('Number of Days off')]
     name =  holiday[headers.index('Holiday Name')]
     if dof == 0:
       no_break.append(name)
     elif dof > 5:
        long_break.append(name)
     elif 3 < dof <= 5:
        medium_break.append(name)
     else:
        short_break.append(name)


print(long_break)
print(medium_break)
print(short_break)
print(no_break)

    


# Problem 5
headers = chinese_holidays[0]

i = 1
while i < len(chinese_holidays):
    chinese_holidays[i][1] = chinese_holidays[i][1].split('-')
    i += 1

print(chinese_holidays[1:])


# Problem 6
headers = chinese_holidays[0]

for holiday in chinese_holidays[1:]:
    dt = holiday[headers.index('Date')]
    if 3 <= int(dt[1]) <= 5:
        holiday.insert(0, "Spring") 
    elif 6 <= int(dt[1]) <= 8:
        holiday.insert(0, "Summer") 
    elif 9 <= int(dt[1]) <= 11:
        holiday.insert(0, "Fall")
    else:
         holiday.insert(0, "Winter")

print(chinese_holidays)

# Problem 7

dragon_boat_activities = []

j = 0
while j < len(activities):
    if "Eating Zongzi" in activities[j][1]:
        dragon_boat_activities.extend(activities[j][1].split("|"))
       
    j += 1

print(dragon_boat_activities)
