import socket
import math

number_dict = {'0':1,'1':2,'2':3,'3':4,'4':5,'5':6,'6':7,'7':8,'8':9,'9':10}

word_dict= {'A':11,'B':12,'C':13,'D':14,'E':15,'F':16,'G':17,'H':18,'I':19,'J':20,'K':21,'L':22,'M':23,'N':24,'O':25,'P':26,'Q':27,'R':28,'S':29,'T':30,'U':31,'V':32,'W':33,'X':34,'Y':35,'Z':36,
            'a':37,'b':38,'c':39,'d':40,'e':41,'f':42,'g':43,'h':44,'i':45,'j':46,'k':47,'l':48,'m':49,'n':50,'o':51,'p':52,'q':53,'r':54,'s':55,'t':56,'u':57,'v':58,'w':59,'x':60,'y':61,'z':62,' ':63}

word_dict.update(number_dict)

def decrypt_subs(cipher_text,key):
    cipher_len = len(cipher_text)
    key_len = len(key)
    c = 0
    string = ""
    i=0
    try:
        while(i<cipher_len):
            if(c%key_len == 0):
                c=0
            if(cipher_text[i] == '$'):
                val1 = word_dict[cipher_text[i+1]]
                val2 = word_dict[cipher_text[i+2]]
                final_val = val1 + val2 - word_dict[key[c]]
                string += str(list(word_dict.keys())[list(word_dict.values()).index(final_val)])
                i=i+4
            else:
                val1 = 2*word_dict[cipher_text[i]]
                final_val = val1 - word_dict[key[c]]
                string += str(list(word_dict.keys())[list(word_dict.values()).index(final_val)])
                i=i+1
            c = c+1
    except:
        print('Access denied, Please enter the right key')
        string = ""
    return string

def decryptTransposition(cipher_text, key):
    string = ""
    letter = []
    i = 0
    while(i<len(cipher_text)):
        if(cipher_text[i] == '$'):
            letter.append(cipher_text[i:i+4])
            i += 4
        else:
            letter.append(cipher_text[i])
            i += 1

    new = list(key)
    new.sort()
    row_count = int(len(letter)/len(key))
    matrix = []
    for i in range(row_count):
        abc = []
        for i in range(len(new)):
            abc.append("")
        matrix.append(abc)
    count = 0

    for i in range(len(new)):
        if(i%2 == 0):
            for j in range(len(matrix)-1,-1,-1):
                matrix[j][i] = letter[count]
                count += 1
        else:
            for j in range(len(matrix)):
                matrix[j][i] = letter[count]
                count += 1

    matrix.append(new)
    new_m = transpose(matrix)

    key = list(key)
    ans = []

    for i in key:
        for j in new_m:
            if(j[-1] == i):
                ans.append(j)
                break
    new_m = transpose(ans)
    new_m.remove(key)

    for i in new_m:
        for j in i:
            string = string + j
    string = string.replace('_','')
    key1 = input("Enter the 1st key: ")
    ans = decrypt_subs(string, key1)
    return ans


def transpose(l1):
    l2 = []
    for i in range(len(l1[0])):
        row =[]
        for item in l1:
            row.append(item[i])
        l2.append(row)
    return l2


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((socket.gethostname(), 1024))
print("Connected")
msg = s.recv(1024)
print("Data Received")
cipher_text = msg.decode("utf-8")
print("Received Message: ", cipher_text)
key = input("Enter the 2nd key: ")
print("Decrypting...")
ans = decryptTransposition(cipher_text, key)
print(ans)
