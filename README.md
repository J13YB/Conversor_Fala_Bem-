# Conversor dFala Bem!

Esta aplicação converte mensagens com tom potencialmente passivo-agressivo em versões mais empáticas e construtivas.

## Funcionalidades
- Identificação do tom da mensagem
- Reformulação com IA (várias sugestões)
- Reformulação alternativa com regras simples
- Suporte a múltiplos idiomas (PT, EN, ES)
- Histórico com exportação CSV

## Executar localmente
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploy com Streamlit Cloud
1. Cria um repositório com `app.py`, `requirements.txt` e este `README.md`
2. Vai a [https://streamlit.io/cloud](https://streamlit.io/cloud)
3. Faz login com GitHub e seleciona o repositório
4. Clica em **Deploy**
