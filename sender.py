import socket
import math

number_dict = {'0':1,'1':2,'2':3,'3':4,'4':5,'5':6,'6':7,'7':8,'8':9,'9':10}

word_dict= {'A':11,'B':12,'C':13,'D':14,'E':15,'F':16,'G':17,'H':18,'I':19,'J':20,'K':21,'L':22,'M':23,'N':24,'O':25,'P':26,'Q':27,'R':28,'S':29,'T':30,'U':31,'V':32,'W':33,'X':34,'Y':35,'Z':36,
            'a':37,'b':38,'c':39,'d':40,'e':41,'f':42,'g':43,'h':44,'i':45,'j':46,'k':47,'l':48,'m':49,'n':50,'o':51,'p':52,'q':53,'r':54,'s':55,'t':56,'u':57,'v':58,'w':59,'x':60,'y':61,'z':62,' ':63}

word_dict.update(number_dict)

def encrypt_subs(plain_text,key):
    pt_len = len(plain_text)
    key_len = len(key)
    string = ""
    c=0
    for i in range(0,pt_len):
        if(i%key_len == 0):
            c=0
        val1 = word_dict[plain_text[i]]
        val2 = word_dict[key[c]]
        avg_val = (val1+val2)/2
        check_val = math.ceil(avg_val) - math.floor(avg_val)
        if(check_val):
            string += '$'+ str(list(word_dict.keys())[list(word_dict.values()).index(math.floor(avg_val))])+ str(list(word_dict.keys())[list(word_dict.values()).index(math.ceil(avg_val))]) + '$'
        else:
            string +=  str(list(word_dict.keys())[list(word_dict.values()).index(math.floor(avg_val))])
        c= c+1
    print("After substitution : ", string)
    keytrans = input("Enter 2nd key key for transposition: ")
    while(True):
        for i in keytrans:
            if(keytrans.count(i)>1):
                keytrans = input("Enter the Key again with no similar letters: ")
        if(i == keytrans[-1] and keytrans.count(i) == 1):
            break
    ans = encryptTransposition(string, keytrans)
    return ans

def encryptTransposition(plain_text, key):
    string = ""
    letter = []
    i = 0
    while(i<len(plain_text)):
        if(plain_text[i] == '$'):
            letter.append(plain_text[i:i+4])
            i += 4
        else:
            letter.append(plain_text[i])
            i += 1
    key = list(key)

    matrix = []
    count = 0
    if(len(letter)%len(key) == 0):
        row_count = int(len(letter)/len(key))+1
    else:
        row_count = int(len(letter)/len(key))+2
    for i in range(row_count):
        abc = []
        for j in key:
            if(i == 0):
                abc.append(j)
            else:
                if(count < len(letter)):
                    abc.append(letter[count])
                    count += 1
                else:
                    abc.append('_')
        matrix.append(abc)
    z = transpose(matrix)
    key.sort()
    new_matrix = []
    for i in key:
        for j in z:
            if(j[0] == i):
                new_matrix.append(j)
                break

    z = transpose(new_matrix)
    z = z[1:]
    for i in range(len(z[0])):
        if(i % 2 == 0):
            for j in range(len(z)-1,-1,-1):
                string = string + z[j][i]
        else:
            for j in range(len(z)):
                string = string + z[j][i]
    return string

def transpose(l1):
    l2 = []
    for i in range(len(l1[0])):
        row =[]
        for item in l1:
            row.append(item[i])
        l2.append(row)
    return l2

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((socket.gethostname(), 1024))
s.listen(5)
while True:
    clt, addr = s.accept()
    print("Connection to {} established".format(addr))
    plain_text = str(input('Enter the plain text: '))
    key = str(input('Enter the key: '))
    ciphered_text = encrypt_subs(plain_text,key)
    print("Your ciphered_text: ", ciphered_text)
    print("Sending Encrypted Data....")
    clt.send(bytes(ciphered_text, "utf-8"))
    print("Data sent.")
