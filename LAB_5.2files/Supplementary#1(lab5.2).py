fout = open('SURNAME.txt', 'w')

analysis = "Hello, I'm Czer Justine D. Maringal.\n"
fout.write(analysis)

analysis = "From BS Computer Engineering 1-A.\n"
fout.write(analysis)

analysis = "UCC College of Engineering.\n"
fout.write(analysis)

fout.close()

fhand = open('SURNAME.txt', 'r')

for line in fhand:
    print(line, end='')

fhand.close()