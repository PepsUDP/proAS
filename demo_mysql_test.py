import mysql.connector

mydb = mysql.connector.connect(
    host="btayogimwuf6ppd8dtgu-mysql.services.clever-cloud.com",
    user="uzkqujyps8yvnfwd",
    password="LMRyKb5ygYFGs32bg0W5",
    database="btayogimwuf6ppd8dtgu"
)

print(mydb)

mycursor = mydb.cursor()

mycursor.execute("SHOW TABLES")

for x in mycursor:
  print(x)