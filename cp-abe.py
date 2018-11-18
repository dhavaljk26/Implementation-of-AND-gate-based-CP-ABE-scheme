
# coding: utf-8

# In[1]:


import math
import random
import hashlib
import time


# In[216]:


numAttributes = 128

RHO = 32
KEY_LEN = 32

MAX_BITS = 32


# In[217]:


#Function to check if a number is prime
def isPrime(n):
    if n == 2:
        return True
    
    if n%2 == 0 or n == 1:
        return False
    
    for i in range(3, math.ceil(math.sqrt(n))+1, 2):
        if n%i == 0:
            return False
        
    return True    


# In[218]:


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


# In[219]:


#Function to find gcd of 'a' and 'b' by Euclid's algorithm
def euclidGcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = euclidGcd(b % a, a)
        return (g, x - (b // a) * y, y)


# In[220]:


#Function to find multiplicative inverse of 'a' modulo 'm'
def moduloInverse(a, m):
    g, x, y = euclidGcd(a, m)
    if g != 1:
        raise Exception('modulo inverse does not exist')
    else:
        return x % m


# In[221]:


#Function to check if 'k' is coprime with all elements of array 'arr' 
def checkCoprimality(k, arr):
    for i in range(len(arr)):
        if math.gcd(k, arr[i]) != 1:
            return False
    return True  


# In[222]:


#Function to calaculate 'a' power 'b' modulo 'n'
def powerModN(a, b, n):
    if b == 0:
        return 1
    
    temp = 1
    a = a%n
    
    while b>0:
        if b&1:
            temp = (temp%n * a%n)%n
        b>>=1
        a = (a*a)%n
    return temp    
#     temp = powerModN(a, b//2, n)
#     temp = (temp*temp) % n
#     if b%2:
#         temp = (temp*a) %n
        
#     return temp    


# In[223]:


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


# In[224]:


### Setup phase ###

p = generatePrime(RHO)
q = generatePrime(RHO)

while p == q:
    q = generatePrime(RHO)
    
N = p*q

phiN = (p-1)*(q-1)


# In[225]:


pi = list()
qi = list()

for i in range(0, numAttributes):
    temp = generatePrime()
    
    while math.gcd(temp, phiN) != 1:
        temp = generatePrime()

    pi.append(temp)    
    qi.append(moduloInverse(pi[i], phiN))


# In[226]:


k = random.getrandbits(MAX_BITS)

while math.gcd(k, phiN) != 1 or checkCoprimality(k, qi) == False:
    k = random.getrandbits(MAX_BITS)
    
x = random.getrandbits(MAX_BITS)

while checkCoprimality(x, qi) == False:
    x = random.getrandbits(MAX_BITS)    


# In[227]:


g = random.randint(3, N-2)
    
while math.gcd(g, N) != 1:
    g = random.randint(3, N-2)


# In[228]:


dU = 1
for i in range(len(qi)):
    dU *= qi[i]

DU = powerModN(g, dU, N)
Y  = powerModN(g,  x, N)
R  = powerModN(g,  k, N)


# In[235]:


### Encryption phase ###

start_time_encryption = time.time()

sigmaM = str(random.getrandbits(KEY_LEN))
P = str('10101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010')
M = str('1234567890123456789012345678901234567890123456789012345678901234')

len_H1 = RHO
len_H2 = len(sigmaM)
len_H3 = len(M)

dP = 1
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

print('Encryption Time = {0}'.format(time.time() - start_time_encryption))


# In[236]:


### Key Generation Phase ###

#User 1 - attribute '10'

A = str('10101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010')
dA = 1
for i, c in enumerate(A):
    if c == '1':
        dA *= qi[i]
        
ru = random.getrandbits(MAX_BITS)%phiN
tu = random.getrandbits(MAX_BITS)%phiN

su = (((dA-(ru*x)%phiN+phiN)%phiN) * moduloInverse(k, phiN))%phiN 

k1 = (su + (x*tu)%phiN)%phiN 
k2 = (ru - (k*tu)%phiN + phiN)%phiN


#User 2 - attribute '01'

A2 = str('01')
dA2 = 1
for i, c in enumerate(A2):
    if c == '1':
        dA2 *= qi[i]
        
ru2 = random.getrandbits(MAX_BITS)%phiN
tu2 = random.getrandbits(MAX_BITS)%phiN

su2 = (((dA2-(ru2*x)%phiN+phiN)%phiN) * moduloInverse(k, phiN))%phiN 

k12 = (su2 + (x*tu2)%phiN)%phiN 
k22 = (ru2 - (k*tu2)%phiN + phiN)%phiN


# In[248]:


### Decryption phase ###

start_time_decryption = time.time()

eA = 1 
for i, c in enumerate(A):
    if c == '1':
        eA *= pi[i]

eP = 1 
for i, c in enumerate(P):
    if c == '1':
        eP *= pi[i]  
        
if eA%eP:
    print ('Unable to decrypt')
else:
    Km = powerModN(Ym, k2, N)
    Km = (Km * powerModN(Rm, k1, N))%N
    Km = powerModN(Km, eA//eP, N)
    
    sigmaM = onewayhash(Km, len_H2) ^ CsigmaM
    M = Cm ^ onewayhash(sigmaM, len_H3)

    if not onewayhash(str(sigmaM)+str(M), len_H1) == Sm:
        print ('Invalid signature')
    else:    
        print ('Message :', M)      
        

print('Decryption Time = {0}'.format(time.time() - start_time_decryption))


# In[191]:


### Decryption phase ###
eA2 = 1 
for i, c in enumerate(A2):
    if c == '1':
        eA2 *= pi[i]

eP = 1 
for i, c in enumerate(P):
    if c == '1':
        eP *= pi[i]  
        
if eA2%eP:
    print ('Unable to decrypt')
else:
    Km2 = powerModN(Ym, k22, N)
    Km2 = (Km2 * powerModN(Rm, k12, N))%N
    Km2 = powerModN(Km2, eA//eP, N)
    
    sigmaM2 = onewayhash(Km2, len_H2) ^ CsigmaM
    M2 = Cm ^ onewayhash(sigmaM2, len_H3)
    
    if not onewayhash(str(sigmaM2)+str(M2), len_H1) == Sm:
        print ('Invalid signature')
    else:    
        print ('Message :', M2)  


# In[85]:


print (k1, k2, k12, k22)
print ()


# In[98]:


T1 = powerModN(Ym, k2, N)
T1 = (T1 * powerModN(Rm, k1, N))%N
T2 = powerModN(Ym, k22, N)
T2 = (T2 * powerModN(Rm, k12, N))%N

(GCD, a1, a2) = euclidGcd(pi[0], pi[1])

a1 %= phiN
while a1<0:
    a1 += phiN
    
a2 %= phiN
while a2<0:
    a2 += phiN
    
K = powerModN(T2, a1, N)
K = (K * powerModN(T1, a2, N))%N

print (K, Km)


# In[95]:


print (T1, T2, powerModN(T1, pi[0], N), powerModN(T2, pi[1], N), powerModN(g, rm, N), powerModN(g, rm*qi[0], N))


# In[97]:


print (a1*pi[0] + a2*pi[1], a1, a2)

