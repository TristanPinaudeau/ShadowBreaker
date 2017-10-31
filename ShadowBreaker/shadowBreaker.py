import sys
import hashlib
import string
import itertools
import time

def main():
    args = sys.argv
    shadow = Shadow()
    for n in range(0, len(args)):
        if args[n] == "-s": shadow.SHADOW_FILE_NAME = args[n+1]
        if args[n] == "-o": shadow.OUTPUT_FILE_NAME = args[n+1]
        if args[n] == "-a": shadow.AUTHORIZED_CHAR = args[n+1]
    print("authorized characters : " + shadow.AUTHORIZED_CHAR)
    shadow.crack()



class Account:

    def __init__(self, name, password):
        self.name = name
        self.hash = password
        self.isBroken = False
        self.password = ""

    def getHash(self):
        return self.hash

    def getName(self):
        return self.name

    def getPass(self):
        return self.password

    def setPass(self, password):
        self.password = password

    def writeToFile(self):
        outputFile = open("output.txt", "a+")
        outputFile.write(self.name + ' : ' + self.password + "\n")
        outputFile.close()



class Shadow:

    SHADOW_FILE_NAME = "shadow"
    OUTPUT_FILE_NAME = "accounts"
    DICTIONARY_FILE_NAME = "dico_mini_fr"
    AUTHORIZED_CHAR = string.ascii_letters + string.digits + "@_;#"


    def __init__(self):
        self.accounts = []
        self.timePassed = 0


    def crack(self):
        self.extractShadowPasswords()
        timePassed = time.clock()
        self.dictionaryAttack()
        print("We are going to try the brute force method, it could be quite intensive for your hardware and take a lot of time...")
        if input("Do you want to try this method ? [Y/n] : ") == "Y": self.bruteForce()
        for account in self.accounts:
            if account.isBroken() == False:
                print("Failed to crack the password for user " + account.getName() + ", no match in dictionary")
                print("-- Time passed : " + str(timePassed) + " secs --")
                print("")


    def getPasswords(self):
        passwords = []
        for account in self.accounts :
            passwords.append(account.getHash())
        return passwords


    def extractShadowPasswords(self):
        print("Opening " + self.SHADOW_FILE_NAME + " file...")
        shadowFile = open(self.SHADOW_FILE_NAME, 'r')
        print("Reading " + self.SHADOW_FILE_NAME + " file...")
        print("")
        for line in shadowFile :
            if line.strip() :
                account = line.split(':')
                userName = account[0]
                password = account[1].split('$')
                if len(password) == 1:
                    print("The password for user " + userName + " can not be extract.")
                else :
                    passwordEncryption = password[1]
                    hashToBreak = password[2]
                    self.accounts.append(Account(userName, hashToBreak))
                    print(userName + " : " + hashToBreak)
        print("")
        shadowFile.close()


    def bruteForce(self):
        for n in range(6,12):
            for passToTest in itertools.product(self.AUTHORIZED_CHAR, repeat=n):
                passToTest = str.join("", passToTest)
                print(passToTest)
                if passToTest == "brazil" : input()
                self.testPass(passToTest)


    def dictionaryAttack(self):
        with open(self.DICTIONARY_FILE_NAME) as fileobj:
            for line in fileobj:
                line = line.strip()
                self.testPass(line)


    def testPass(self, passToTest):
         for account in self.accounts :
            if hashlib.md5(passToTest.encode('utf-8')).hexdigest() ==  account.getHash():
                account.setPass(passToTest)
                print("Successfully cracked the password for user " + account.getName() + " : " + account.getPass())
                print("-- Time passed : " + str(self.timePassed) + " secs --")
                print("")
                account.writeToFile()

main()
