import streamlit as st
import json
import os

FILE_NAME = "orders.json"

# ======================
# НАСТРОЙКИ СТРАНИЦЫ И СТИЛЬ
# ======================
st.set_page_config(page_title="Louro CRM PRO", page_icon="💜", layout="wide")

# Кастомный CSS для фиолетово-белой темы
st.markdown("""
    <style>
    .main {
        background-color: #f5f0ff;
    }
    .stButton>button {
        background-color: #6a0dad;
        color: white;
        border-radius: 10px;
        border: none;
        padding: 0.5rem 1rem;
    }
    .stButton>button:hover {
        background-color: #8a2be2;
        color: white;
    }
    .sidebar .sidebar-content {
        background-color: #ffffff;
    }
    h1, h2, h3 {
        color: #4b0082;
    }
    .stTextInput>div>div>input, .stNumberInput>div>div>input {
        border-color: #6a0dad;
    }
    </style>
    """, unsafe_allow_html=True)

# ======================
# ФУНКЦИИ ДАННЫХ
# ======================
def load_data():
    if os.path.exists(FILE_NAME):
        try:
            with open(FILE_NAME, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return []
    return []

def save_data(data):
    with open(FILE_NAME, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

data = load_data()

# ======================
# ВЕРХНЯЯ ПАНЕЛЬ (КНОПКА ПОМОЩИ)
# ======================
col1, col2 = st.columns([0.85, 0.15])
with col2:
    with st.expander("❓ Помощь"):
        st.write("Связаться с поддержкой:")
        st.info("📧 support@louro-crm.kz\n📞 +7 777 777 77 77")

# ======================
# БОКОВОЕ МЕНЮ (НАВИГАЦИЯ)
# ======================
st.sidebar.title("💜 Louro CRM")
menu = st.sidebar.radio(
    "Навигация по разделам:",
    ["📊 Обзор и Список", "➕ Новый заказ", "🔎 Поиск по ИИН", "🗑 Управление"]
)

# ======================
# 1. ОБЗОР И СПИСОК
# ======================
if menu == "📊 Обзор и Список":
    st.header("📋 Текущие заказы")
    
    if not data:
        st.info("В базе пока нет заказов.")
    else:
        total = sum(item['price'] for item in data)
        st.metric("Общий оборот", f"{total:,.0f} тг".replace(",", " "))
        
        # Отображение карточек заказов
        for i, order in enumerate(data):
            with st.container():
                st.markdown(f"""
                <div style="background-color: white; padding: 15px; border-radius: 10px; border-left: 5px solid #6a0dad; margin-bottom: 10px;">
                    <strong>Заказ №{i+1}: {order['fio']}</strong><br>
                    🆔 ИИН: {order['iin']} | 📦 {order['product']}<br>
                    💰 <span style="color: #6a0dad; font-weight: bold;">{order['price']:,} тг</span>
                </div>
                """, unsafe_allow_html=True)

# ======================
# 2. ДОБАВЛЕНИЕ ЗАКАЗА
# ======================
elif menu == "➕ Новый заказ":
    st.header("➕ Оформление нового заказа")
    
    with st.form("add_form"):
        fio = st.text_input("Полное ФИО клиента")
        iin = st.text_input("ИИН (12 цифр)", max_chars=12)
        product = st.text_input("Товар или услуга")
        # Лимит 10 млн тенге
        price = st.number_input("Цена (макс. 10 000 000 тг)", min_value=0, max_value=10000000, step=1000)
        
        submit = st.form_submit_button("Создать заказ")
        
        if submit:
            if not fio or len(iin) < 12 or not product or price <= 0:
                st.error("❌ Пожалуйста, корректно заполните все поля (ИИН должен быть 12 цифр)")
            else:
                new_order = {
                    "fio": fio,
                    "iin": iin,
                    "product": product,
                    "price": price
                }
                data.append(new_order)
                save_data(data)
                st.success("✅ Заказ успешно добавлен в базу!")

# ======================
# 3. ПОИСК ПО ИИН
# ======================
elif menu == "🔎 Поиск по ИИН":
    st.header("🔎 Поиск заказа")
    search_iin = st.text_input("Введите ИИН для поиска")
    
    if search_iin:
        results = [o for o in data if search_iin in o['iin']]
        if results:
            for res in results:
                st.success(f"Найдено: {res['fio']} — {res['product']} ({res['price']} тг)")
        else:
            st.warning("Заказов с таким ИИН не найдено.")

# ======================
# 4. УПРАВЛЕНИЕ (УДАЛЕНИЕ)
# ======================
elif menu == "🗑 Управление":
    st.header("🗑 Удаление записей")
    if data:
        options = [f"{i+1}. {d['fio']} ({d['product']})" for i, d in enumerate(data)]
        to_delete = st.selectbox("Выберите заказ для удаления:", options)
        idx = int(to_delete.split(".")[0]) - 1
        
        if st.button("Удалить безвозвратно"):
            removed = data.pop(idx)
            save_data(data)
            st.success(f"Заказ на имя {removed['fio']} удален.")
            st.rerun()
    else:
        st.write("Список пуст.")