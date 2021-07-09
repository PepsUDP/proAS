from demo_mysql_test import mydb

mycursor = mydb.cursor()

sql = "INSERT INTO paciente (RUT, nombre, fechanac, edad, enfermedad) VALUES (%s, %s, %s, %s, %s)"
val = ("222222222", "Martín Caucaman", "1998-06-25", "100", "Dislexia")
mycursor.execute(sql, val)

mydb.commit()

print(mycursor.rowcount, "record inserted.")