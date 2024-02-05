# main.py
import pandas as pd
import streamlit as st


def parse_date(date_string):
    # Example: Convert the date string to a pandas datetime object
    return pd.to_datetime(date_string, format="%d/%m/%Y %H:%M:%S")


def main():
    st.title("Analise de WBS e PSE")

    # Read CSV file
    fileDict = {}
    uploaded_files = st.file_uploader(
        "Selecione a planilha a ser analisada", type=["csv"], accept_multiple_files=True
    )

    names = []
    pse, wbs = None, None

    if uploaded_files:
        for f in uploaded_files:
            df = pd.read_csv(f)
            names = df["Nome"].unique()
            df["Carimbo de data/hora"] = df["Carimbo de data/hora"].apply(parse_date)
            df.set_index("Carimbo de data/hora", inplace=True)
            if "PSE" in df.columns:
                pse = df
            else:
                wbs = df

        selected_name = st.sidebar.selectbox("Selecionar usuario", names)

        pse_check = st.sidebar.checkbox("PSE", disabled=(pse is None))
        wbs_check = st.sidebar.checkbox("WBS", disabled=(wbs is None))

        if pse_check:

            filtered_PSE = pse[pse["Nome"] == selected_name]
            chart_data_PSE = filtered_PSE.copy()
            st.write("### PSE: ")
            st.bar_chart(chart_data_PSE["PSE"])

        if wbs_check:
            chart_metric_options = [
                "Fadiga",
                "Qualidade do sono",
                "Dor muscular geral",
                "Nível de estresse",
                "Humor",
                "PSR",
                "Todas",
            ]
            selected_metric = st.sidebar.selectbox(
                "Selecionar uma métrica", chart_metric_options
            )
            filtered_WBS = wbs[wbs["Nome"] == selected_name]
            chart_data_WBS = filtered_WBS.copy()

            if selected_metric == "Todas":
                for c in (
                    "Fadiga",
                    "Qualidade do sono",
                    "Dor muscular geral",
                    "Nível de estresse",
                    "Humor",
                    "PSR",
                ):
                    st.write(f"### {c}: ")

                    st.bar_chart(chart_data_WBS[c])
            else:
                st.write(f"### {selected_metric}: ")

                st.bar_chart(chart_data_WBS[selected_metric])


if __name__ == "__main__":
    main()
