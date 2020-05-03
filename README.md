# Easy Java

I wrote this program because I was tired of writing POJOs from SQL then having to write the RowMapper afterwards. This simple program generates the Entity POJO and RowMapper given the following:

1. entity "Application" - Name of entity
2. data "C:/data.txt" - A pipe separated export of the data. You only need header and 1 row of data. 

Will generate Entity.java and EntityRowMapper.java in directory invoked from.

example: python easyjava.py --entity ApplicationGroup --data "C:/Users/majora2007/Desktop/testdata.txt"

Word list came from:
https://raw.githubusercontent.com/first20hours/google-10000-english/master/google-10000-english-no-swears.txt

N.B. This code is pretty messy, I wrote this in 2 hours. Don't judge. 

Build:
pyinstaller easyjava.spec