import os
import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="FormCheck", layout="wide")

st.title("FormCheck – Прогноз риска ухудшения формы игрока")

if 'history' not in st.session_state:
    st.session_state.history = []

tab1, tab2, tab3 = st.tabs(["Прогноз", "История прогнозов", "О проекте"])

with tab1:
    with st.form("prediction_form"):
        col1, col2 = st.columns(2)

        with col1:
            age = st.slider("Возраст игрока", 16, 45, 25)
            recovery_days = st.slider("Длительность восстановления (дней)", 1, 180, 30)
            pre_rating = st.slider("Рейтинг до травмы (0-100)", 0, 100, 70)

        with col2:
            injury_severity = st.selectbox("Тяжесть травмы (0 — лёгкая, 1 — средняя, 2 — тяжёлая)", [0, 1, 2])
            position = st.selectbox("Позиция игрока", ["Forward", "Midfielder", "Defender", "Goalkeeper"])

        desired_threshold = st.slider("Желаемый порог риска (%)", 0, 100, 50)
        submitted = st.form_submit_button("Предсказать риск")

    if submitted:
        position_mapping = {"Forward": 0, "Midfielder": 1, "Defender": 2, "Goalkeeper": 3}
        position_encoded = position_mapping[position]

        api_url = "http://localhost:8000/predict"
        payload = {
            "injury": injury_severity,
            "recovery_days": recovery_days,
            "rating_before_clean": pre_rating,
            "age": age,
            "position": position_encoded
        }

        try:
            response = requests.post(api_url, json=payload)
            if response.status_code == 200:
                result = response.json()
                probability = result["risk_probability"] / 100
                prediction = result["risk_prediction"]

                st.subheader("Результаты прогноза:")
                risk_label = "Высокий" if probability >= (desired_threshold / 100) else "Низкий"
                st.write(f"Риск ухудшения формы: {risk_label}")
                st.write(f"Вероятность ухудшения формы: {probability:.2%}")

                st.progress(int(probability * 100))

                risk_color = "green" if probability < 0.3 else "orange" if probability < 0.7 else "red"
                st.markdown(
                    f'<div style="background-color:{risk_color}; padding:15px; border-radius:8px; margin-top:15px; margin-bottom:25px;">'
                    f'<h4 style="color:white; text-align:center;">Текущий риск: {probability:.2%}</h4>'
                    '</div>',
                    unsafe_allow_html=True
                )

                if probability >= (desired_threshold / 100):
                    st.warning("Рекомендуется снизить тренировочную нагрузку и увеличить восстановление")
                else:
                    st.success("Можно продолжать текущую тренировочную программу")

                st.session_state.history.append({
                    "Возраст": age,
                    "Травма": injury_severity,
                    "Дней восстановления": recovery_days,
                    "Рейтинг до травмы": pre_rating,
                    "Позиция": position,
                    "Вероятность ухудшения формы (%)": round(probability * 100, 2),
                    "Риск": risk_label
                })
            else:
                st.error("Ошибка при обращении к API.")
        except Exception as e:
            st.error(f"Ошибка запроса к API: {e}")

with tab2:
    if st.session_state.history:
        st.subheader("История прогнозов за сессию:")
        history_df = pd.DataFrame(st.session_state.history)
        st.dataframe(history_df)

        csv = history_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Скачать историю в CSV",
            data=csv,
            file_name='formcheck_history.csv',
            mime='text/csv'
        )
    else:
        st.info("История прогнозов пуста. Сделайте хотя бы один прогноз")

with tab3:
    st.header("О проекте FormCheck")
    st.write("FormCheck — это AI-система для анализа спортивной формы и прогнозирования риска травм")
    st.subheader("GitHub проекта:")
    st.markdown("[Открыть репозиторий проекта](https://github.com/danlikendy/formcheck_project)")
    st.subheader("Контакты:")
    st.write("Автор: Цыганцов Артём Сергеевич")
    st.write("[Открыть персональный сайт](https://tsygantsov.ru)")