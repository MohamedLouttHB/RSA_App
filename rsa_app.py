import random
import sympy
import math

# Fonction pour générer un nombre premier aléatoire
def generer_nombre_premier():
    while True:
        nombre = random.randint(2, 1000)  # Choisissez une plage appropriée pour vos besoins
        if sympy.isprime(nombre):
            return nombre

# Génération des deux nombres premiers aléatoires p et q
p = generer_nombre_premier()
q = generer_nombre_premier()


# calcul n et Phi
n = p * q
phi = (p-1) * (q-1)

# cle prive e :
def generer_cle_publique():
    while True:
        e = random.randint(2, 1000)  # Choisissez une plage appropriée pour vos besoins
        if math.gcd(e, phi) == 1:
            return e

e = generer_cle_publique()
d = sympy.mod_inverse(e, phi)


cle_prive, cle_publique = (n,e), (n,d)

msg = "Hello word!"

message= [ord(ch) for ch in msg]
print(message)

cipher_text = [pow(m,e,n) for m in message ]

decryt_msg = [pow(c,d,n) for c in cipher_text ]
clear_text = "".join(chr(ch) for ch in decryt_msg)


#Affichage des infos

#print("n:", n)
#print("Phi  :", phi)
#Affichage des n et phi
#print("n:", n)
#print("Phi  :", phi)
#print("e:", e)
#print("d:", d)
#print(cipher_text)
#print(clear_text)
