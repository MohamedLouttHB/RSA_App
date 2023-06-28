import streamlit as st
import math,sympy
from rsa_app import generer_nombre_premier, generer_cle_publique
from PIL import Image


st.set_page_config(
    page_title="RSA Algorithm App",
    page_icon="🔐",

)



st.title(":blue[RSA Algorithm]")

#Side bar
with st.sidebar:
    st.title(":blue[Fonctionnement RSA]")
    st.write("1 - Choix de 2 nombres premiers :red[_p_] et :red[_q_] ")
    st.write("2 - Calcul de : :red[_n = p * q_]")
    st.write("3 - Calcul de :red[_ϕ(n) = (p-1) * (q-1)_]")
    st.write("4 - Choix du cle public :red[_e_] tq : :red[_pgcd(e,ϕ(n)) = 1_]")
    st.write("5 - Calcul du clé privé :red[_d_] tq : :red[_e.d ≡ 1 mod n_]")
    st.write("6 - Crypter le message avec le clé public du destinataire")
    st.write("7 - Decrypter le message avec le clé privé du destinataire")
    image = Image.open('rsa.jpeg')
    st.image(image, caption=' Fonctionnement RSA')
    st.write("_:red[code source :]_ https://github.com/MohamedLouttHB/RSA_App")
    st.write('**_:blue[Made by] :red[Mohamed Loutt Horma Babana]_**')

gen_choix = st.radio("**:red[Comment voulez vous genérer les clefs ?]**",('Automatiquement','Manuellement'), horizontal=True)

if (gen_choix == 'Manuellement') :
    col1, col2, col3 = st.columns(3)
    with col1:
        p_input = st.number_input('Saisir un nombre premier p',step=1)

    with col2 :
        q_input = st.number_input('Saisir un nombre premier q',step=1)
    with col3 :
        e_input = st.number_input('Saisir un cle publique e',step=1)


    if(sympy.isprime(p_input) and sympy.isprime(q_input)) :
            mn = p_input * q_input
            mphi = (p_input - 1)*(q_input -1)
            if math.gcd(e_input, mphi) == 1:
                md = sympy.mod_inverse(e_input, mphi)
            else:
                st.error("e doit etre premier avec ϕ(n)")
    else :
        st.error("p et q doit etre premier")

    st.divider()

    txtm = st.text_area('Entrer un message')
    txt_msgm =  [ord(ch) for ch in txtm]

    s_cipher_textm = [pow(sm,e_input,mn) for sm in txt_msgm ]

    s_decrypt_textm = [pow(sm,md,mn) for sm in s_cipher_textm ]
    s_clear_textm = "".join(chr(ch) for ch in s_decrypt_textm)


    col1, col2 = st.columns(2)
    with col1:
        encrypt = st.button('🔒 Chiffré')

    with col2:
        decrypt = st.button('🔑 Déchiffré')

    if(encrypt):
        st.error(s_cipher_textm)

    if(decrypt):
        st.success(s_clear_textm)



if (gen_choix == 'Automatiquement') :

    # Génération des deux nombres premiers aléatoires p et q
    sp = generer_nombre_premier()
    sq = generer_nombre_premier()

    # n et Phi
    sn = sp * sq
    sphi = (sp-1) * (sq-1)

    se = generer_cle_publique()
    sd = sympy.mod_inverse(se, sphi)

    col1, col2, col3, col4, col5, col6 = st.columns(6)
    col1.write(f"p = {sp}")
    col2.write(f"q = {sq}")
    col3.write(f"n = {sn}")
    col4.write(f"ϕ(n) = {sphi}")
    col5.write(f"clé publique = {se}")
    col6.write(f"clé privé = {sd}")
    st.warning("Tous ces valeurs sont générés automatiquement, si vous actualisez la page, ils seront changés")

    st.divider()
    txt = st.text_area('Entrer un message')
    txt_msg =  [ord(ch) for ch in txt]

    s_cipher_text = [pow(sm,se,sn) for sm in txt_msg ]

    s_decrypt_text = [pow(sm,sd,sn) for sm in s_cipher_text ]
    s_clear_text = "".join(chr(ch) for ch in s_decrypt_text)

    col1, col2 = st.columns(2)
    with col1:
        chiffre = st.button('🔒 Chiffré')

    with col2:
        dechiffre = st.button('🔑 Déchiffré')

    if(chiffre):
        st.error(s_cipher_text)

    if(dechiffre):
        st.success(s_clear_text)






