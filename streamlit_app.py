import streamlit as st
import pandas as pd
import joblib
import json

st.title("Classipet")
st.write("Clasificador de mascotas. Introzca los datos de su mascota y le diremos a que clase pertenece.")

st.write("Por favor, introduzca los datos de su mascota:")

# Carga el modelo entrenado y las asignaciones para el color de ojos y el largo del pelo
model = joblib.load("model/pets_model.joblib")
with open("model/category_mapping.json", "r") as f:
    category_mapping = json.load(f)

# Extraer los valores categoricos
eye_color_values = category_mapping["eye_color"]
fur_length_values = category_mapping["fur_length"]

# Crear los widgets para la entrada de datos
weight = st.number_input("Peso (kg)", min_value=1.0, max_value=100.0)
height = st.number_input("Altura (cm)", min_value=1.0, max_value=100.0)
eye_color = st.selectbox("Color de ojos", ["Azul", "Marrón", "Gris", "Verde"])
fur_length = st.selectbox("Largo Del Pelo", ["Largo", "Medio", "Corto"])

# Mapea la seleccion de color de ojos y largo del pelo al español
eye_color_map = {"Azul": "blue", "Marrón": "brown", "Gris": "gray", "Verde": "green"}
fur_length_map = {"Largo": "long", "Medio": "medium", "Corto": "short"}

selected_eye_color = eye_color_map[eye_color]
selected_fur_length = fur_length_map[fur_length]

# Genera las columnas binarias para el color de ojos y el largo del pelo
# eye_color_binary = [int(color == selected_eye_color) for color in eye_color_values]
eye_color_binary = [(color == selected_eye_color) for color in eye_color_values]
fur_length_binary = [(length == selected_fur_length) for length in fur_length_values]

# Crea un DataFrame con los datos de entrada
Input_data = [weight, height] + eye_color_binary + fur_length_binary
columns = ["weight_kg", "height_cm"] + [f"eye_color_{color}" for color in eye_color_values] + [f"fur_length_{length}" for length in fur_length_values]
input_df = pd.DataFrame([Input_data], columns=columns)

# Realiza la predicción
if st.button("Predecir"):
    prediction = model.predict(input_df)[0]
    prediction_map = {"dog": "Perro", "cat": "Gato", "rabbit": "Conejo"}
    prediction = prediction_map[prediction]
    st.success(f"La mascota es un {prediction}", icon="✅")
    st.balloons()