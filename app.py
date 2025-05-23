
import streamlit as st
import json
import os

# Load data
def load_json(filename):
    with open(os.path.join("data", filename), "r") as f:
        return json.load(f)

mots = load_json("mots.json")
phrases = load_json("phrases.json")
embeddings = load_json("embeddings.json")

def cosine(a, b):
    if not a or not b:
        return 0
    dot = sum(x*y for x,y in zip(a,b))
    norm = lambda v: sum(x*x for x in v) ** 0.5
    return round(100 * dot / (norm(a)*norm(b)), 1)

# App UI
st.set_page_config(page_title="Cristal Sémantique – Agent Complet", layout="centered")
st.title("🎮 Cristal Sémantique – Tous les modes")

mode = st.sidebar.selectbox("🎲 Choisissez un mode", [
    "Cemantix", "Faux Vrai", "Trou de Mémoire", "Pendu Sémantique", "Fusion Thématique"
])

if mode == "Cemantix":
    st.header("🔥 Mode Cemantix")
    target = "amour"
    guess = st.text_input("Proposez un mot")
    if guess:
        if guess not in embeddings:
            st.error("Mot inconnu ou mal orthographié.")
        else:
            score = cosine(embeddings[guess], embeddings[target])
            st.success(f"Proximité : {score} %")
            if guess == target:
                st.balloons()
                st.success("🎉 Mot mystère trouvé !")

elif mode == "Faux Vrai":
    st.header("🧠 Mode Faux Vrai")
    phrase = phrases["fauxvrai"]["phrase"]
    intrus = phrases["fauxvrai"]["intrus"]
    st.write(f"Phrase : {phrase}")
    guess = st.text_input("Quel mot aurait dû être là ?")
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
    st.write(f"Phrase : {affichage}")
    st.info(f"Mots trouvés : {len(st.session_state['found'])}/{len(trous)}")

elif mode == "Pendu Sémantique":
    st.header("💀 Mode Pendu Sémantique")
    phrase = phrases["pendu"]["phrase"]
    mot = phrases["pendu"]["mot"]
    if "pendu" not in st.session_state:
        st.session_state["pendu"] = {"display": "_"*len(mot), "erreurs": 0, "essais": []}
    g = st.text_input("Lettre ou mot entier")
    if g:
        state = st.session_state["pendu"]
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
        st.write(f"Mot : {state['display']}")
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
