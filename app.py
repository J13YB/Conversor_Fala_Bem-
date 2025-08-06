# Conversor de Tom Passivo-Agressivo para Comunicação Empática (v5)

import streamlit as st
from transformers import pipeline
import pandas as pd

st.title("Conversor de Comunicação para Tom Empático")
st.write("Esta aplicação converte mensagens potencialmente passivo-agressivas em versões mais empáticas e construtivas, com apoio de IA.")

if 'historico' not in st.session_state:
    st.session_state.historico = []

idioma = st.selectbox("Seleciona o idioma da mensagem:", ["Português", "Inglês", "Espanhol"])
user_input = st.text_area("Escreve a mensagem que gostarias de reformular:", height=150)

@st.cache_resource
def load_pipelines():
    classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
    rewriter = pipeline("text2text-generation", model="google/flan-t5-large")
    return classifier, rewriter

classifier, rewriter = load_pipelines()
labels = ["empático", "neutro", "assertivo", "passivo-agressivo", "agressivo"]

def reescrever_com_regras(texto):
    substituicoes = {
        "pelo menos": "seria ideal se",
        "não concordo": "tenho uma perspetiva diferente",
        "como é óbvio": "poderá não ser claro para todos",
        "isto é o mínimo": "poderíamos considerar como boa prática",
        "!!!": ".",
        "???": ".",
        "pode ser?": "faria sentido para ti?"
    }
    for k, v in substituicoes.items():
        texto = texto.replace(k, v)
    return texto

def reescrever_com_ia_multiplas(texto, idioma):
    prompt_base = {
        "Português": "Reescreve esta mensagem de forma empática e construtiva:",
        "Inglês": "Rewrite this message in an empathetic and constructive tone:",
        "Espanhol": "Reescribe este mensaje con un tono empático y constructivo:"
    }[idioma]

    respostas = rewriter(f"{prompt_base} '{texto}'", max_length=256, num_return_sequences=3, num_beams=5)
    return [r['generated_text'] for r in respostas]

if st.button("Analisar e Reformular"):
    if user_input.strip():
        result = classifier(user_input, candidate_labels=labels)
        top_label = result['labels'][0]

        sugestoes_ia = reescrever_com_ia_multiplas(user_input, idioma)
        reformulado_regras = reescrever_com_regras(user_input)

        st.subheader("Tom Identificado:")
        st.write(f"{top_label.capitalize()} (confiança: {result['scores'][0]:.2f})")

        st.subheader("Sugestões Reformuladas com IA:")
        for i, sugestao in enumerate(sugestoes_ia):
            st.markdown(f"**Sugestão {i+1}:** {sugestao}")

        st.subheader("Versão Reformulada com Regras (alternativa):")
        st.write(reformulado_regras)

        st.session_state.historico.append({
            "Idioma": idioma,
            "Mensagem Original": user_input,
            "Tom Identificado": top_label,
            "Sugestões IA": " ||| ".join(sugestoes_ia),
            "Reformulado (Regras)": reformulado_regras
        })
    else:
        st.warning("Por favor, insere uma mensagem para reformular.")

if st.checkbox("Mostrar histórico de mensagens"):
    if st.session_state.historico:
        df = pd.DataFrame(st.session_state.historico)
        st.dataframe(df)
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Exportar histórico para CSV", data=csv, file_name="historico_mensagens.csv", mime="text/csv")
    else:
        st.info("Ainda não há histórico para mostrar.")
