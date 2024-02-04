# main.py
import pandas as pd
import streamlit as st


def parse_date(date_string):
    # Example: Convert the date string to a pandas datetime object
    return pd.to_datetime(date_string, format="%d/%m/%Y %H:%M:%S")


def main():
    st.title("Analise de WBS e PSE")

    # Read CSV file
    file_path = st.file_uploader("Selecione a planilha a ser analisada", type=["csv"])
    if file_path is not None:
        df = pd.read_csv(file_path)

        st.write("### Data Overview")
        st.write(df.head())
        isPSE = "PSE" in df.columns

        names = df["Nome"].unique()
        selected_name = st.selectbox("Selecionar usuario", names)

        filtered_df = df[df["Nome"] == selected_name]
        st.write(filtered_df)

        chart_data = filtered_df.copy()
        chart_data["Carimbo de data/hora"] = chart_data["Carimbo de data/hora"].apply(
            parse_date
        )
        chart_data.set_index("Carimbo de data/hora", inplace=True)

        chart_name = "PSE" if isPSE else "WBS"
        st.write(f"### Gráficos - {chart_name} - {selected_name}")

        if isPSE:
            st.line_chart(chart_data["PSE"])
            st.bar_chart(chart_data["PSE"])
        else:
            chart_metric_options = [
                "Fadiga",
                "Qualidade do sono",
                "Dor muscular geral",
                "Nível de estresse",
                "Humor",
                "PSR",
            ]
            selected_metric = st.selectbox(
                "Selecionar uma métrica", chart_metric_options
            )
            st.line_chart(chart_data[selected_metric])
            st.bar_chart(chart_data[selected_metric])


if __name__ == "__main__":
    main()
