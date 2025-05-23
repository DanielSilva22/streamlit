
import streamlit as st
import json
import os

st.set_page_config(page_title="Cristal Sémantique", layout="centered")

# Chargement des données
def load_json(filename):
    with open(os.path.join("data", filename), "r") as f:
        return json.load(f)

mots = load_json("mots.json")
phrases = load_json("phrases.json")
embeddings = load_json("embeddings.json")

def cosine(a, b):
    dot = sum(x*y for x,y in zip(a,b))
    norm = lambda v: sum(x*x for x in v) ** 0.5
    return round(100 * dot / (norm(a)*norm(b)), 1)

# Interface principale
st.markdown("<a href='#' style='display:inline-block;padding:8px 12px;border:1px solid #ccc;border-radius:8px;text-decoration:none;font-size:14px;'>← Retour au menu</a>", unsafe_allow_html=True)
st.markdown("<h1 style='text-align:center; margin-bottom:0;'>🧠 Cristal Sémantique</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; margin-top:0; color: #555;'>Choisissez un mode de jeu</p>", unsafe_allow_html=True)

mode = st.selectbox("🎮 Mode de jeu", ["Cemantix", "Faux Vrai", "Trou de Mémoire", "Pendu Sémantique", "Fusion Thématique"])

if mode == "Cemantix":
    st.header("🔥 Mode Cemantix")
    st.markdown("""
    <div style='background-color:#eef4ff; padding:15px; border-radius:8px; margin-bottom:20px;'>
        <b>🔥 Mode Cemantix</b><br>
        Devinez le mot mystère caché. À chaque mot que vous proposez, vous verrez à quel point vous êtes proche du bon mot.
        <span style='color:red;'>Plus c'est chaud, plus vous êtes près de la réponse.</span>
    </div>
    """, unsafe_allow_html=True)
    target = "amour"
    with st.form("cemantix_form"):
        guess = st.text_input("Tapez votre mot ici...", label_visibility="collapsed", placeholder="Tapez votre mot ici...")
        submit = st.form_submit_button("🔍 Valider")
    if submit and guess:
        if guess not in embeddings:
            st.error(f"Le mot "{guess}" est inconnu ou mal orthographié.")
        else:
            score = cosine(embeddings[guess], embeddings[target])
            st.success(f"{guess} → 🔥 Proximité : {score}%")
            if guess == target:
                st.balloons()
                st.success("🎉 Bravo ! Vous avez trouvé le mot mystère.")

elif mode == "Faux Vrai":
    st.header("🧠 Mode Faux Vrai")
    phrase = phrases["fauxvrai"]["phrase"]
    intrus = phrases["fauxvrai"]["intrus"]
    st.markdown(f"Phrase : **{phrase}**")
    guess = st.text_input("Quel mot aurait dû être à la place ?")
    if guess:
        if guess in phrase.split():
            st.warning("Ce mot est déjà visible dans la phrase.")
        elif guess == intrus:
            st.success("✅ Bravo, c'était le mot attendu !")
        else:
            st.error("❌ Ce n'était pas le bon mot.")

elif mode == "Trou de Mémoire":
    st.header("🧩 Mode Trou de Mémoire")
    phrase = phrases["troudememoire"]["phrase"]
    trous = set(phrases["troudememoire"]["trous"])
    affichage = phrase
    guess = st.text_input("Complétez un mot manquant")
    if "found" not in st.session_state:
        st.session_state["found"] = []
    if guess:
        if guess in trous and guess not in st.session_state["found"]:
            st.session_state["found"].append(guess)
            st.success("Mot correct !")
        else:
            st.error("❌ Ce mot n’est pas attendu ou déjà trouvé.")
    for mot in st.session_state["found"]:
        affichage = affichage.replace("___", mot, 1)
    st.markdown(f"Phrase actuelle : **{affichage}**")
    st.info(f"Mots trouvés : {len(st.session_state['found'])}/{len(trous)}")

elif mode == "Pendu Sémantique":
    st.header("💀 Mode Pendu Sémantique")
    phrase = phrases["pendu"]["phrase"]
    mot = phrases["pendu"]["mot"]
    if "pendu" not in st.session_state:
        st.session_state["pendu"] = {"display": "_"*len(mot), "erreurs": 0}
    g = st.text_input("Lettre ou mot entier")
    state = st.session_state["pendu"]
    if g:
        if g == mot:
            state["display"] = mot
            st.balloons()
            st.success("🎉 Mot trouvé !")
        elif len(g) == 1 and g in mot:
            state["display"] = "".join([g if mot[i]==g else state["display"][i] for i in range(len(mot))])
            st.success("Lettre correcte.")
        else:
            state["erreurs"] += 1
            st.error("Erreur !")
    st.markdown(f"Mot : **{state['display']}**")
    st.info(f"Erreurs : {state['erreurs']}/{round(len(mot)*0.4)}")
    if state["erreurs"] >= round(len(mot)*0.4):
        st.error("💀 Pendu !")

elif mode == "Fusion Thématique":
    st.header("🌌 Mode Fusion Thématique")
    theme = phrases["fusion"]["theme"]
    if "fusion" not in st.session_state:
        st.session_state["fusion"] = []
    g = st.text_input("Proposez un mot du thème")
    if g:
        if g in theme and g not in st.session_state["fusion"]:
            st.session_state["fusion"].append(g)
            st.success("✅ Mot du thème trouvé.")
        elif g in st.session_state["fusion"]:
            st.warning("Mot déjà trouvé.")
        else:
            st.error("❌ Mot incorrect ou hors-thème.")
    st.write("Mots trouvés :", ", ".join(st.session_state["fusion"]))
