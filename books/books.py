from book import Book
import csv
import sys

library = []

def readFile():
    with open("books.csv", 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            library.append(Book(row[0], row[1], row[2]))

def searchAuthors(searchString):
    searchedBooks = []
    for book in library:
        author = book.getAuthorName().lower()
        if searchString in author:
            searchedBooks.append(book)
    return sorted(searchedBooks, key = lambda Book: Book.authorName.split(" ")[1].lower())

#TODO add sort to searchTitle,searchYears,searchAll
def searchTitle(searchString):
    searchedBooks = []
    for book in library:
        if searchString in book.getTitle().lower():
            searchedBooks.append(book)
    return sorted(searchedBooks, key = lambda Book: Book.title.lower())

def searchYears(searchString):
    listYears = searchString.split("-")
    searchedBooks = []
    
    startYear = int(listYears[0])
    endYear = int(listYears[1])
    
    for book in library:
        for i in range(startYear,endYear + 1):
            if int(book.getPubYear()) == i:
                searchedBooks.append(book)
    return sorted(searchedBooks, key = lambda Book: int(Book.pubYear))

def searchAll(searchString):
    searchedBooks = []
    for book in library:
        if searchString in book.getFullLine():
            searchedBooks.append(book)
    return sorted(searchedBooks, key = lambda Book: Book.authorName.split(" ")[1].lower())

def helpCmnd():
    with open('usage.txt') as usage:
        usage = usage.readlines()
        for line in usage:
            print(line, end="")
    print()
    
def printBooks(bookList):
    for book in bookList:
        book.printBook()
        
#TODO finish
def determineCommands():
    #program name is sys.argv[0]
    
    length = len(sys.argv)
    
    if length < 2:
        sys.stderr.write("Please type a command. For more help, run the help commmand.\nTry running python3 books.py help.\n")
        
    elif sys.argv[1] == "print":
        option = sys.argv[2]
        
        if length == 2:
            printBooks(library)
        
        elif length == 3:
            printBooks(searchAll(sys.argv[2]))
            #could run into problems with books.py cmnd option since this also triggers it
        elif length == 4:
            option = sys.argv[2]
            if option == "--title":
                printBooks(searchTitle(sys.argv[3]))
            elif option == "--years":
                printBooks(searchYears(sys.argv[3]))
            elif option == "--author":
                printBooks(searchAuthors(sys.argv[3]))
            else:
                sys.stderr.write("You need to type a valid option.\nTry running python3 books.py help.\n")
        else:
            sys.stderr.write("You have typed too many command and option entries.\nTry running python3 books.py help.\n")
    elif sys.argv[1] == "help":
        helpCmnd()
    else:
        sys.stderr.write("Please type a valid command. For more help, run the help commmand.\nTry running python3 books.py help.\n")

def main():
    readFile()
    determineCommands()

main()
