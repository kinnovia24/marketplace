import streamlit as st
import pandas as pd
from datetime import datetime
import folium
from streamlit_folium import st_folium
from PIL import Image

# Main Streamlit app with icon-based tabs
st.set_page_config(page_title="Motorcycle Marketplace", page_icon="🏍️", layout="centered")

st.sidebar.image("motorcycle_logo.png", use_column_width=True)
menu_selection = st.sidebar.radio(
    "Navigate", 
    ["Purchase 🏍️", "Test Drive 🛵", "Services 🛠️", "Merchandise 🎁", "Dealers 🗺️"]
)

# Set background color for the app
st.markdown(
    """
    <style>
    .main {
        background-color: #f5f5f5;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Load or create an empty dataframe to store user data
excel_file = 'motorcycle_marketplace_data.xlsx'

try:
    data = pd.read_excel(excel_file)
except FileNotFoundError:
    data = pd.DataFrame(columns=['Name', 'Email', 'Address', 'Purchase', 'Delivery Location', 'Delivery Date'])

# Save user data to Excel
def save_to_excel(new_data):
    global data
    data = data.append(new_data, ignore_index=True)
    data.to_excel(excel_file, index=False)

# Motorcycle categories and prices
motorcycle_categories = {
    'Sports': 15000,
    'Cruiser': 18000,
    'Touring': 25000,
    'Off-Road': 10000,
    'Adventure': 30000
}

# Merchandise items and prices
merchandise_items = {
    'T-Shirt': 30,
    'Toy Motorcycle': 50,
    'Helmet': 120,
    'Small Electric Motorcycle': 200
}

# Dealer locations in Europe
dealers = {
    'Berlin, Germany': [52.5200, 13.4050],
    'Paris, France': [48.8566, 2.3522],
    'Rome, Italy': [41.9028, 12.4964],
    'Madrid, Spain': [40.4168, -3.7038],
    'London, UK': [51.5074, -0.1278]
}

# Placeholder for images (replace with your own image paths)
images = {
    'motorcycle': 'motorcycle.jpg',
    'test_drive': 'test_drive.jpg',
    'service': 'service.jpg',
    'merchandise': 'merchandise.jpg'
}

# Function to buy a motorcycle
def buy_motorcycle():
    st.header('Buy a Motorcycle')
    st.image(images['motorcycle'], use_column_width=True)
    
    name = st.text_input('Enter your name:')
    address = st.text_input('Enter your address:')
    delivery_location = st.text_input('Enter the delivery location:')
    category = st.selectbox('Select Motorcycle Category', list(motorcycle_categories.keys()))
    price = motorcycle_categories[category]
    st.write(f'Price for {category}: ${price}')
    
    if st.button('Buy Motorcycle'):
        if name and address and delivery_location:
            new_data = {
                'Name': name,
                'Email': '',
                'Address': address,
                'Purchase': category + ' Motorcycle',
                'Delivery Location': delivery_location,
                'Delivery Date': datetime.now().strftime('%Y-%m-%d')
            }
            save_to_excel(new_data)
            st.success(f'You have successfully purchased a {category} motorcycle for ${price}!')

# Function to book a test drive
def book_test_drive():
    st.header('Book a Test Drive')
    st.image(images['test_drive'], use_column_width=True)
    
    name = st.text_input('Enter your name:')
    email = st.text_input('Enter your email:')
    date = st.date_input('Select a date for your test drive')
    time = st.time_input('Select a time for your test drive')

    if st.button('Book Test Drive'):
        if name and email:
            st.success(f'Test drive booked for {name} on {date} at {time}. Confirmation sent to {email}.')

# Function to book a service appointment
def book_service_appointment():
    st.header('Book a Service Appointment')
    st.image(images['service'], use_column_width=True)
    
    name = st.text_input('Enter your name:')
    email = st.text_input('Enter your email:')
    service_date = st.date_input('Select a date for the service appointment')
    service_time = st.time_input('Select a time for the service appointment')

    if st.button('Book Service Appointment'):
        if name and email:
            st.success(f'Service appointment booked for {name} on {service_date} at {service_time}. Confirmation sent to {email}.')

# Function to buy merchandise
def buy_merchandise():
    st.header('Buy Merchandise')
    st.image(images['merchandise'], use_column_width=True)
    
    name = st.text_input('Enter your name:')
    address = st.text_input('Enter your address:')
    delivery_date = st.date_input('Select delivery date:')
    selected_item = st.selectbox('Choose an item:', list(merchandise_items.keys()))
    price = merchandise_items[selected_item]

    st.write(f'Price for {selected_item}: ${price}')
    
    if st.button('Buy Merchandise'):
        if name and address:
            new_data = {
                'Name': name,
                'Email': '',
                'Address': address,
                'Purchase': selected_item + ' Merchandise',
                'Delivery Location': address,
                'Delivery Date': delivery_date.strftime('%Y-%m-%d')
            }
            save_to_excel(new_data)
            st.success(f'You have successfully purchased {selected_item} for ${price}!')

# Function to show motorcycle dealers on an interactive map
def show_dealers_map():
    st.header("Motorcycle Dealers in Europe")
    
    m = folium.Map(location=[54.5260, 15.2551], zoom_start=4)
    
    # Add dealer locations as markers
    for city, coords in dealers.items():
        folium.Marker(location=coords, popup=f"Dealer in {city}", tooltip="Dealer").add_to(m)
    
    st_folium(m, width=700, height=500)


if menu_selection == "Purchase 🏍️":
    buy_motorcycle()

elif menu_selection == "Test Drive 🛵":
    book_test_drive()

elif menu_selection == "Services 🛠️":
    book_service_appointment()

elif menu_selection == "Merchandise 🎁":
    buy_merchandise()

elif menu_selection == "Dealers 🗺️":
    show_dealers_map()