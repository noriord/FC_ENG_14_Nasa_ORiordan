#set the info
recipient_name = "Mina"
birth_year = 2012
personal_message = "Happy Birthday!"
sender_name = "Nasa"

#Set current year
current_year = 2026

#Calculate age
age = current_year - birth_year

#print the birthday card with f-strings
print()
print(f"{recipient_name}, let's celebrate your {age} years of awesomeness!")
print(f"Wishing you a day filled with joy and laugther as you turn {age} !")
print()
print(f"{personal_message}")
print()
print("With love and best wishes,")
print(f"{sender_name}")

#print the birthday card with format() method
print()
print("{}, let's celebrate your {} years of awesomeness!".format(recipient_name, age))
print("Wishing you a day filled with joy and laugther as you turn {} !".format(age))
print()
print("{}".format(personal_message))
print()
print("With love and best wishes,")
print("{}".format(sender_name))