[README.md](https://github.com/user-attachments/files/22005914/README.md)
# Gerador de Ficha de EPI (Streamlit)

Este é um app web simples em **Streamlit** que gera uma ficha completa de entregas de EPI a partir da **data de admissão** e de uma **tabela editável de EPIs** (com validade em dias).

## Como rodar localmente

1. Instale Python 3.10+.
2. Crie e ative um ambiente virtual (opcional, mas recomendado).
3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
4. Rode o app:
   ```bash
   streamlit run app.py
   ```
5. Abra o endereço que aparecer no terminal (geralmente http://localhost:8501).

## Como publicar (gratuito) no Streamlit Community Cloud

1. Suba estes arquivos (`app.py`, `requirements.txt`) para um repositório no **GitHub**.
2. Acesse https://streamlit.io/cloud, faça login com o GitHub e clique em **New app**.
3. Selecione o repositório, branch e o caminho do arquivo `app.py`.
4. Clique em **Deploy**. Ao final, você terá uma **URL pública** do seu app.

> Dica: se atualizar o código no GitHub, o app será reconstruído automaticamente.

## Observações

- O ciclo entre entregas é de 30 dias ("mensal" simplificado). Se quiser usar meses de calendário reais, podemos adaptar o código.
- O app evita registrar nova entrega de um EPI enquanto a entrega anterior ainda estiver **dentro da validade**.
