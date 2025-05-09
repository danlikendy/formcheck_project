# AI-ассистент для прогнозирования спортивных травм

## Возможности

- Прогноз риска травм с учётом типа, тяжести и восстановления
- Визуализация зависимости травм от рейтингов и показателей
- Персональные рекомендации по тренировкам и восстановлению
- Использование ML-моделей (RandomForest / XGBoost)
- Веб-интерфейс на Streamlit и полноценный API (FastAPI)
- Готовая контейнеризация с использованием Docker и Docker Compose

## Стек технологий

- **Python 3.10+**
- `pandas`, `xgboost`, `scikit-learn`, `seaborn`, `matplotlib`, `Streamlit`, `FastAPI`, `Docker`

## Структура проекта

```
FormCheck/
│
├── apps/                   
│   ├── main.py               ← API (FastAPI)
│   ├── streamlit_app.py      ← Веб-интерфейс (Streamlit)
│   └── dockerfile            ← Docker для API и Streamlit
│
├── data/
│   └── formcheck_data.csv    ← Исходные данные
│
├── docks/
│   ├── Empathy map.png       ← API (FastAPI)
│   ├── UX Persona.png        ← Веб-интерфейс (Streamlit)
│   └── Статья ВАК            ← Docker для API и Streamlit
│
├── models/
│   └── rf_model.pkl          ← Обученная модель
│
├── requirements.txt
├── docker-compose.yml
└── README.md
```

## Установка и запуск

```bash
git clone https://github.com/danlikendy/formcheck_project.git
cd formcheck_project
pip install -r requirements.txt
```

### Запуск API (FastAPI)

```bash
uvicorn apps.main:app --reload
```

### Запуск Streamlit-интерфейса

```bash
streamlit run apps/streamlit_app.py
```

### Запуск через Docker Compose (API и Streamlit вместе)

```bash
docker-compose up --build
```

## Приватность

- Биометрия и оценки остаются локально
- Можно развернуть полностью оффлайн
- Возможность очистки логов, моделей и предсказаний

## Лицензия

MIT License — свободное использование, включая коммерческое

## Автор

Цыганцов Артём Сергеевич — [danlikendy](https://github.com/danlikendy)