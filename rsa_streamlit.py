import streamlit as st
import math
import sympy
from main import generer_nombre_premier, generer_cle_publique
from PIL import Image

# Set Streamlit page configuration
st.set_page_config(
    page_title="RSA Algorithm App",
    page_icon="🔐",
)

# Store initial variables in the Streamlit session state
if "sp" not in st.session_state:
    st.session_state.sp = None
if "sq" not in st.session_state:
    st.session_state.sq = None
if "sn" not in st.session_state:
    st.session_state.sn = None
if "sphi" not in st.session_state:
    st.session_state.sphi = None
if "se" not in st.session_state:
    st.session_state.se = None
if "sd" not in st.session_state:
    st.session_state.sd = None


# Display the RSA Algorithm App title
st.title(":blue[RSA Algorithm]",anchor=False)

# Sidebar
with st.sidebar:
    st.title(":blue[Fonctionnement RSA]")
    st.write("1 - Choix de 2 nombres premiers :red[_p_] et :red[_q_] ")
    st.write("2 - Calcul de : :red[_n = p * q_]")
    st.write("3 - Calcul de :red[_ϕ(n) = (p-1) * (q-1)_]")
    st.write("4 - Choix du clé publique :red[_e_] tq : :red[_pgcd(e,ϕ(n)) = 1_]")
    st.write("5 - Calcul du clé privé :red[_d_] tq : :red[_e.d ≡ 1 mod n_]")
    image = Image.open('rsa.jpeg')
    st.image(image, caption=' Fonctionnement RSA')
    st.write("_:red[code source :]_ https://github.com/MohamedLouttHB/RSA_App")
    st.write('**_:blue[Made by]_ :violet[Mohamed Loutt Horma Babana]**')

# Function to encrypt the message and cache the result
@st.cache_data
def encrypt_message(message, e, mn):
    message_ascii = [ord(ch) for ch in message]
    cipher_text = [pow(m, e, mn) for m in message_ascii]
    return cipher_text

# Function to decrypt the message and cache the result
@st.cache_data
def decrypt_message(cipher_text, d, mn):
    decrypted_text = [pow(c, d, mn) for c in cipher_text]
    clear_text = "".join(chr(ch) for ch in decrypted_text)
    return clear_text

gen_choix = st.radio("**:red[Comment voulez-vous générer les clés ?]**", ('Automatiquement', 'Manuellement'), horizontal=True)

if gen_choix == 'Manuellement':
    col1, col2, col3 = st.columns(3)
    with col1:
        p_input = st.number_input('Saisir un nombre premier p', step=1)

    with col2:
        q_input = st.number_input('Saisir un nombre premier q', step=1)
    with col3:
        e_input = st.number_input('Saisir un cle publique e', step=1)

    if (sympy.isprime(p_input) and sympy.isprime(q_input)):
        mn = p_input * q_input
        mphi = (p_input - 1) * (q_input - 1)
        if math.gcd(e_input, mphi) == 1:
            md = sympy.mod_inverse(e_input, mphi)
        else:
            st.warning("e doit etre premier avec ϕ(n)")
    else:
        st.warning("p et q doit etre premier")

    try:
        st.info(f"clé privé : {md}", icon="️ℹ️")
    except:
        pass

    st.divider()

    col1, col2 = st.columns(2)
    with col1:
        txtm = st.text_area('Entrer un message')
        txt_msgm = [ord(ch) for ch in txtm]
        s_cipher_textm = [pow(sm, e_input, mn) for sm in txt_msgm]
        s_decrypt_textm = [pow(sm, md, mn) for sm in s_cipher_textm]
        s_clear_textm = "".join(chr(ch) for ch in s_decrypt_textm)
        encrypt = st.button('🔒 Chiffré')
        if encrypt:
            try:
                st.write("Le message chiffré est : ")
                st.error(s_cipher_textm, icon="✉️")
            except:
                st.error("Vérifier la validité des valeurs !")

    with col2:
        key_priv = st.text_area("Entrer votre clé privé")
        decrypt = st.button('🔑 Déchiffré')

        if (decrypt):
            try:
                if(key_priv == str(md)):
                    st.write("Le message déchiffré est : ")
                    st.success(s_clear_textm)
                else:
                    st.error("Clé incorrect !")
            except:
                st.error("Vérifier la validité des valeurs !")

if gen_choix == 'Automatiquement':
    if st.session_state.sp is None or st.session_state.sq is None or st.session_state.sn is None \
            or st.session_state.sphi is None or st.session_state.se is None or st.session_state.sd is None:
        # Generate the two random prime numbers p and q
        sp = generer_nombre_premier()
        sq = generer_nombre_premier()

        # Calculate n and Phi
        sn = sp * sq
        sphi = (sp - 1) * (sq - 1)

        # Generate the public and private keys
        se = generer_cle_publique()
        sd = sympy.mod_inverse(se, sphi)

        st.session_state.sp = sp
        st.session_state.sq = sq
        st.session_state.sn = sn
        st.session_state.sphi = sphi
        st.session_state.se = se
        st.session_state.sd = sd

    col1, col2, col3, col4, col5, col6 = st.columns(6)
    col1.write(f"p = {st.session_state.sp}")
    col2.write(f"q = {st.session_state.sq}")
    col3.write(f"n = {st.session_state.sn}")
    col4.write(f"ϕ(n) = {st.session_state.sphi}")
    col5.write(f"clé publique = {st.session_state.se}")
    col6.write(f"clé privé = {st.session_state.sd}")
    st.info("Ces valeurs sont genérés automatiquement. Si vous actualisez la page, elles seront modifiés.", icon="️ℹ️")

    st.divider()

    col1, col2 = st.columns(2)
    with col1:

        txt = st.text_area('Entrer un message à chiffré')
        txt_msg = [ord(ch) for ch in txt]

        s_cipher_text = encrypt_message("".join(chr(ch) for ch in txt_msg), st.session_state.se, st.session_state.sn)

        chiffre = st.button('🔒 Chiffré')

        if chiffre:
            st.write("Le message chiffré est : ")
            st.error(s_cipher_text, icon="✉️")


    with col2:

        dech_input = st.text_area('Entrer votre clé privé pour déchiffrer le message ')
        dech = st.button('🔑 Déchiffré')
        if dech:
            if dech_input == str(st.session_state.sd):
                decrypted_text = decrypt_message(s_cipher_text, st.session_state.sd, st.session_state.sn)
                st.write("Le message en claire est : ")
                st.success(decrypted_text, icon="📨")

            else:
                st.error('Clé incorrecte !')
