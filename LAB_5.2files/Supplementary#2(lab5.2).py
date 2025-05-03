fout = open('SURNAME.txt', 'w')
fout.write("Line 1: first line.\n")
fout.write("Line 2: second line.\n")
fout.write("Line 3: third line.\n")
fout.close()

fhand = open('SURNAME.txt', 'r')
print("Reading file:")
for line in fhand:
    print(line, end='')
fhand.close()

fhand = open('SURNAME.txt', 'r')
lines = fhand.readlines()
fhand.close()

lines[1] = "Line 2: This line has been updated.\n"

fout = open('SURNAME.txt', 'w')
fout.writelines(lines)
fout.close()

fhand = open('SURNAME.txt', 'r')
print("\n\nAfter update:")
for line in fhand:
    print(line, end='')
fhand.close()

fhand = open('SURNAME.txt', 'r')
lines = fhand.readlines()
fhand.close()

del lines[1]

fout = open('SURNAME.txt', 'w')
fout.writelines(lines)
fout.close()

fhand = open('SURNAME.txt', 'r')
print("\n\nAfter delete:")
for line in fhand:
    print(line, end='')
fhand.close()