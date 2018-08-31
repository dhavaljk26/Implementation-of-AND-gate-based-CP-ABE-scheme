
# coding: utf-8

# In[83]:


import math
import random
import hashlib


# In[84]:


numAttributes = 3

RHO = 8
KEY_LEN = 8

MAX_BITS = 8


# In[85]:


#Function to check if a number is prime
def isPrime(n):
    if n == 2:
        return True
    
    if n%2 == 0:
        return False
    
    for i in range(3, math.ceil(math.sqrt(n))+1, 2):
        if n%i == 0:
            return False
        
    return True    


# In[86]:


#Function to generate a random prime number of rho bits
def generatePrime(len=MAX_BITS):
    
    temp = random.getrandbits(len)
    
    if len != MAX_BITS:
        temp = temp | (1<<(len-1)) 
    temp |= 1
    
    while not isPrime(temp):
        temp = random.getrandbits(len)
        if len != MAX_BITS: 
            temp = temp | (1<<(len-1)) 
        temp |= 1
    
    return temp


# In[87]:


#Function to find gcd of 'a' and 'b' by Euclid's algorithm
def euclidGcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = euclidGcd(b % a, a)
        return (g, x - (b // a) * y, y)


# In[88]:


#Function to find multiplicative inverse of 'a' modulo 'm'
def moduloInverse(a, m):
    g, x, y = euclidGcd(a, m)
    if g != 1:
        raise Exception('modulo inverse does not exist')
    else:
        return x % m


# In[89]:


#Function to check if 'k' is coprime with all elements of array 'arr' 
def checkCoprimality(k, arr):
    for i in range(len(arr)):
        if math.gcd(k, arr[i]) != 1:
            return False
    return True  


# In[90]:


#Function to calaculate 'a' power 'b' modulo 'n'
def powerModN(a, b, n):
    if b == 0:
        return 1
    
    temp = powerModN(a, b//2, n)
    temp = (temp*temp) % n
    if b%2:
        temp = (temp*a) %n
        
    return temp    


# In[91]:


#Function to compute one-way hash of given message 'M', with output of length 'len' bits
def onewayhash(message, len):
    
    message = str(message).encode('utf-8')
    hash_object = hashlib.sha1(message)
    hex_digest = hash_object.hexdigest()
    digest = 0   
    index = 1
    
    for c in reversed(hex_digest):
        temp = int (c, 16)        
        if len < 4:
            temp &= ( (1<<(len)) - 1)
            digest += temp * index
            break
            
        digest += temp * index
        index *= 16
        len -= 4    
    
    return digest


# In[92]:


### Setup phase ###

p = generatePrime(RHO)
q = generatePrime(RHO)

while p == q:
    q = generatePrime(RHO)
    
N = p*q

phiN = (p-1)*(q-1)


# In[93]:


pi = list()
qi = list()

for i in range(0, numAttributes):
    temp = generatePrime()
    
    while math.gcd(temp, phiN) != 1:
        temp = generatePrime()

    pi.append(temp)    
    qi.append(moduloInverse(pi[i], phiN))


# In[100]:


k = random.getrandbits(MAX_BITS)

while math.gcd(k, phiN) != 1 or checkCoprimality(k, qi) == False:
    k = random.getrandbits(MAX_BITS)
    
x = random.getrandbits(MAX_BITS)

while checkCoprimality(x, qi) == False:
    x = random.getrandbits(MAX_BITS)    


# In[101]:


g = random.randint(3, N-2)
    
while math.gcd(temp, N) != 1:
    temp = random.randint(3, N-2)


# In[102]:


dU = 1
for i in range(len(qi)):
    dU *= qi[i]

DU = powerModN(g, dU, N)
Y  = powerModN(g,  x, N)
R  = powerModN(g,  k, N)


# In[119]:


### Encryption phase ###

sigmaM = str(random.getrandbits(KEY_LEN))
P = str('010')
M = str('227')

len_H1 = RHO
len_H2 = len(sigmaM)
len_H3 = len(M)

dP = 1 #doubtful
for i, c in enumerate(P):
    if c == '1':
        dP *= qi[i]

rm = onewayhash(P+M+sigmaM, len_H1)
Km = powerModN(g, rm*dP, N)
Ym = powerModN(g, x*rm , N)
Rm = powerModN(g, k*rm , N)
CsigmaM = onewayhash(str(Km), len_H2) ^ int(sigmaM)
Cm = onewayhash(sigmaM, len_H3) ^ int(M)
Sm = onewayhash(sigmaM+M, len_H1)


# In[120]:


### Key Generation Phase ###

#User 1 - attribute '001'

A = str('011')
dA = 1 #doubtful
for i, c in enumerate(A):
    if c == '1':
        dA *= qi[i]
        
ru = random.getrandbits(MAX_BITS)%phiN
tu = random.getrandbits(MAX_BITS)%phiN

su = (((dA-(ru*x)%phiN+phiN)%phiN) * moduloInverse(k, phiN))%phiN 

k1 = (su + (x*tu)%phiN)%phiN 
k2 = (ru - (k*tu)%phiN + phiN)%phiN


# In[131]:


### Decryption phase ###
eA = 1 #doubtful
for i, c in enumerate(A):
    if c == '1':
        eA *= pi[i]

eP = 1 #doubtful
for i, c in enumerate(P):
    if c == '1':
        eP *= pi[i]  
        
if eA%eP:
    print ('Unable to decrypt')
else:
    Km2 = powerModN(Ym, k2, N)
    Km2 = (Km2 * powerModN(Rm, k1, N))%N
    Km2 = powerModN(Km2, eA/eP, N)
    
    sigmaM2 = onewayhash(Km2, len_H2) ^ CsigmaM
    M2 = Cm ^ onewayhash(sigmaM2, len_H3)
    
    if not onewayhash(str(sigmaM2)+str(M2), len_H1) == Sm:
        print ('Invalid signature')
    else:    
        print ('Message :', M2)      


# In[129]:


print (sigmaM,M)
print (sigmaM2,M2)

