import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit.components.v1 as components
from reportlab.pdfgen import canvas
import streamlit.components.v1 as components
from reportlab.pdfgen import canvas
import base64



# Функция для генерации тестовых данных
def generate_test_data():
    months = ["Январь", "Февраль", "Март", "Апрель", "Май", "Июнь", "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"]
    categories = ["Кабели", "Провода"]
    subcategories = ["Витая пара", "Коаксиальный", "Оптоволоконный", "Электропровод"]

    data = []

    for month in months:
        for category in categories:
            for subcategory in subcategories:
                production = round((10 + 30 * (categories.index(category) + 1)) * (1 + subcategories.index(subcategory) * 0.1))
                data.append({"Месяц": month, "Категория": category, "Подкатегория": subcategory, "Производство": production})

    return pd.DataFrame(data)

# Заголовок приложения
st.title("Аналитическая система для предприятия по производству кабельно-проводниковой продукции")

# Загрузка данных
data = generate_test_data()

# Отображение данных
st.subheader("Данные о продукции")
st.dataframe(data)

# ... (предыдущий код)

# Новый раздел "Настройка параметров анализа"
st.sidebar.title("Настройка параметров анализа")

# Выбор периода
selected_period = st.sidebar.selectbox("Выберите период анализа", data['Месяц'].unique())

# Выбор типа продукции
selected_product_type = st.sidebar.selectbox("Выберите тип продукции", data['Категория'].unique())

# Фильтрация данных
filtered_data = data[(data['Месяц'] == selected_period) & (data['Категория'] == selected_product_type)]

# Новый раздел "Визуализация результатов"
st.sidebar.title("Визуализация результатов")

# Выбор графиков для построения
visualization_options = st.sidebar.multiselect(
    "Выберите графики для визуализации",
    ['Распределение продукции по категориям', 'Динамика производства по месяцам'],
    default=['Распределение продукции по категориям', 'Динамика производства по месяцам']
)

# Построение выбранных графиков
if 'Распределение продукции по категориям' in visualization_options:
    st.subheader("Распределение продукции по категориям")
    fig_category_distribution_filtered = px.pie(filtered_data, names='Подкатегория', title='Распределение продукции в выбранном периоде и типе продукции')
    st.plotly_chart(fig_category_distribution_filtered)

if 'Динамика производства по месяцам' in visualization_options:
    st.subheader("Динамика производства по месяцам")
    fig_production_trend_filtered = px.line(filtered_data, x='Месяц', y='Производство', title='Динамика производства в выбранном периоде и типе продукции')
    st.plotly_chart(fig_production_trend_filtered)

# Новый раздел "Формирование отчетов"
st.sidebar.title("Формирование отчетов")

# Выбор формата отчета
report_format = st.sidebar.selectbox("Выберите формат отчета", ['PDF', 'Excel'])

# Кнопка для формирования отчета
if st.sidebar.button("Сформировать отчет"):
    if report_format == 'PDF':
        pdf_filename = "отчет.pdf"
        c = canvas.Canvas(pdf_filename)
        c.drawString(100, 100, "Пример PDF отчета")
        c.save()

        # Кодируем PDF файл в base64
        with open(pdf_filename, "rb") as pdf_file:
            pdf_content = pdf_file.read()
            pdf_base64 = base64.b64encode(pdf_content).decode('utf-8')

        # Вставляем ссылку для скачивания
        href = f'<a href="data:application/octet-stream;base64,{pdf_base64}" download="{pdf_filename}">Скачать PDF отчет</a>'
        st.sidebar.markdown(href, unsafe_allow_html=True)
        st.sidebar.success(f"PDF отчет сформирован успешно!")
       
    elif report_format == 'Excel':
        excel_filename = "отчет.xlsx"
        filtered_data.to_excel(excel_filename, index=False)

        # Кодируем Excel файл в base64
        with open(excel_filename, "rb") as excel_file:
            excel_content = excel_file.read()
            excel_base64 = base64.b64encode(excel_content).decode('utf-8')

        # Вставляем ссылку для скачивания
        href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{excel_base64}" download="{excel_filename}">Скачать Excel отчет</a>'
        st.sidebar.markdown(href, unsafe_allow_html=True)
        st.sidebar.success(f"Excel отчет сформирован успешно!")


# Визуализация данных
fig_category_distribution = px.pie(data, names='Категория', title='Распределение продукции по категориям')
fig_production_trend = px.line(data, x='Месяц', y='Производство', color='Категория', title='Динамика производства по месяцам')

# Отображение веб-интерфейса
st.plotly_chart(fig_category_distribution)
st.plotly_chart(fig_production_trend)

# Вкладка "Сервис"
st.sidebar.title("Сервис")

# Информация о приложении
st.sidebar.subheader("О приложении")
st.sidebar.text("Это прототип аналитической системы для предприятия, производящего кабельно-проводниковую продукцию. "
                "Здесь представлены тестовые данные и графики для демонстрации функционала.")

# Инструкции по использованию
st.sidebar.subheader("Инструкции по использованию")
st.sidebar.text("1. Используйте вкладку 'Данные о продукции' для просмотра тестовых данных о производстве."
                "\n2. В разделе 'Распределение продукции по категориям' вы увидите круговую диаграмму."
                "\n3. В разделе 'Динамика производства по месяцам' представлен график линии с динамикой производства."
                "\n4. В разделе 'Сервис' находится дополнительная информация об этом приложении.")

# Контактная информация
st.sidebar.subheader("Контактная информация")
st.sidebar.text("Команда:\nСобачева Анна - Тимлид,\nМакаров Максим - Программист,\nЛяпина Валерия - Аналитик")
