import sys
import hashlib
import string



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

    def getHash(self):
        return self.hash

    def getName(self):
        return self.name

    def setPass(self, password):
        self.password = password

    def writeToFile(self):
        outputFile = open('output.mdp', 'w+')
        outputFile.write(self.name + ' : ' + self.password)
        outputFile.close()



class Shadow:

    SHADOW_FILE_NAME = "shadow"
    OUTPUT_FILE_NAME = "accounts"
    AUTHORIZED_CHAR = string.ascii_letters + string.digits + "@_;#"

    def __init__(self):
        self.accounts = []


    def crack(self):
        self.extractShadowPasswords()
        self.dictionnary()
        print("We are going to try the brute force method, it could be quite intensive for your hardware and take a lot of time...\nDo you want to try this method ? [Y/n] :")
        if input() == "Y": self.bruteForce()


    def getPasswords(self):
        passwords = []
        for account in self.accounts :
            passwords.append(account.getHash())
        return passwords


    def extractShadowPasswords(self):
        print("Opening " + self.SHADOW_FILE_NAME + " file...")
        shadowFile = open(self.SHADOW_FILE_NAME, 'r')
        print("Reading " + self.SHADOW_FILE_NAME + " file...")
        print("\n")
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
        print("\n")
        shadowFile.close()


    def bruteForce(self):
        passToTest = ""
        for char in self.AUTHORIZED_CHAR :
            passToTest += char
            for char in self.AUTHORIZED_CHAR :
                passToTest += char
                for char in self.AUTHORIZED_CHAR :
                    passToTest += char
                    for char in self.AUTHORIZED_CHAR :
                        passToTest += char
                        for char in self.AUTHORIZED_CHAR :
                            passToTest += char
                            #===== 6 =====#
                            self.iteratePass(passToTest)
                            for char in self.AUTHORIZED_CHAR :
                                passToTest += char
                                #===== 7 =====#
                                self.iteratePass(passToTest)
                                for char in self.AUTHORIZED_CHAR :
                                    passToTest += char
                                    #===== 8 =====#
                                    self.iteratePass(passToTest)
                                    for char in self.AUTHORIZED_CHAR :
                                        passToTest += char
                                        #===== 9 =====#
                                        self.iteratePass(passToTest)
                                        for char in self.AUTHORIZED_CHAR :
                                            passToTest += char
                                            #===== 10 =====#
                                            self.iteratePass(passToTest)
                                            for char in self.AUTHORIZED_CHAR :
                                                passToTest += char
                                                #===== 11 =====#
                                                self.iteratePass(passToTest)
                                                for char in self.AUTHORIZED_CHAR :
                                                    passToTest += char
                                                    #===== 12 =====#
                                                    self.iteratePass(passToTest)
                                                    passToTest = passToTest[:-1]
                                                passToTest = passToTest[:-1]
                                            passToTest = passToTest[:-1]
                                        passToTest = passToTest[:-1]
                                    passToTest = passToTest[:-1]
                                passToTest = passToTest[:-1]
                            passToTest = passToTest[:-1]
                        passToTest = passToTest[:-1]
                    passToTest = passToTest[:-1]
                passToTest = passToTest[:-1]
            passToTest = passToTest[:-1]


    def iteratePass(self, passToTest):
        for char in self.AUTHORIZED_CHAR :
            passToTest += char
            print(passToTest)
            for account in self.accounts :
                if self.testPass(passToTest, account.getHash()) :
                    account.setPass(passToTest)
                    account.writeToFile()
                    print ('!!!!! YEAH !!!!!')
                    input()
            passToTest = passToTest[:-1]


    def testPass(self, passToTest, hashToBreak):
        hashToTest = hashlib.md5(passToTest.encode('utf-8')).hexdigest()
        if hashToTest == hashToBreak : return True


    def dictionnary(self):
        print("No dictionary found")




main()
