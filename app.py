import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from io import BytesIO

st.set_page_config(page_title="Ficha de EPI", page_icon="🧰", layout="wide")
st.title("🧰 Gerador de Ficha de EPI")

st.markdown("""
Este app gera uma ficha completa de entregas de EPI com base na **data de admissão**, **lista de EPIs** e suas respectivas **validade em dias**.

- A cada ciclo mensal (30 dias), o app só registra nova entrega de um EPI **após expirar a validade anterior**.
- Ao final, você pode **baixar o Excel** com toda a ficha.
""")

# Entrada de parâmetros
col1, col2 = st.columns(2)
with col1:
    start_date = st.date_input("Data de admissão", value=datetime(2015, 8, 21).date(), format="DD/MM/YYYY")
with col2:
    end_date = st.date_input("Data final", value=datetime.today().date(), format="DD/MM/YYYY")

st.markdown("### EPIs (edite se necessário)")
default_epis = [
    {"nome": "MÁSCARA PFF2", "frequencia": "DIÁRIO", "validade_dias": 1},
    {"nome": "LUVA MISTA", "frequencia": "01 MÊS", "validade_dias": 30},
    {"nome": "PROTETOR AURICULAR", "frequencia": "02 MESES", "validade_dias": 60},
    {"nome": "ÓCULOS INCOLOR", "frequencia": "03 MESES", "validade_dias": 90},
    {"nome": "PROTETOR SOLAR", "frequencia": "03 MESES", "validade_dias": 90},
    {"nome": "BOTINA C/ PROTEÇÃO METATARSO", "frequencia": "01 ANO", "validade_dias": 365},
    {"nome": "PERNEIRA DE LONA", "frequencia": "01 ANO", "validade_dias": 365},
    {"nome": "CAPACETE", "frequencia": "05 ANOS", "validade_dias": 1825},
]

epi_df = st.data_editor(
    pd.DataFrame(default_epis),
    num_rows="dynamic",
    use_container_width=True,
    key="epi_table",
)

if st.button("Gerar ficha"):
    # Validação básica
    if start_date > end_date:
        st.error("A data final deve ser maior ou igual à data de admissão.")
        st.stop()

    records = []
    current_date = datetime.combine(start_date, datetime.min.time())
    end_datetime = datetime.combine(end_date, datetime.min.time())

    epis_list = epi_df.to_dict(orient="records")

    while current_date <= end_datetime:
        for epi in epis_list:
            try:
                validade_dias = int(epi.get("validade_dias", 0))
            except Exception:
                validade_dias = 0

            last_delivery_dates = [
                datetime.strptime(r['Data de Entrega'], "%d/%m/%Y")
                for r in records if r['EPI'] == epi.get('nome', '')
            ]
            if last_delivery_dates:
                last_delivery = max(last_delivery_dates)
                if (current_date - last_delivery).days < validade_dias:
                    continue

            entrega = current_date
            devolucao = entrega + timedelta(days=validade_dias)

            records.append({
                "Data de Entrega": entrega.strftime("%d/%m/%Y"),
                "EPI": epi.get("nome", ""),
                "Validade (Uso)": epi.get("frequencia", ""),
                "Data de Devolução": devolucao.strftime("%d/%m/%Y"),
                "Assinatura do Colaborador": ""
            })

        current_date += timedelta(days=30)

    result_df = pd.DataFrame(records).sort_values(by=["Data de Entrega", "EPI"]).reset_index(drop=True)

    st.success(f"Gerado {len(result_df)} registros.")
    st.dataframe(result_df, use_container_width=True, height=400)

    # Download do Excel
    buffer = BytesIO()
    result_df.to_excel(buffer, index=False)
    buffer.seek(0)
    st.download_button(
        label="Baixar Excel (Ficha_EPI_Completa.xlsx)",
        data=buffer,
        file_name="Ficha_EPI_Completa.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
