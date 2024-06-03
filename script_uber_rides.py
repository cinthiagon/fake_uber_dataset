import pandas as pd
import numpy as np
from faker import Faker
import random

# Initialize the Faker object
fake = Faker()

# Define weather conditions
weather_conditions = ['Ensolarado', 'Chuvoso', 'Nublado', 'Ventos Fortes']

# Define locations (for simplicity, using city names)
locations = ['Aeroporto', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']

# Define sex options
sex_options = ['Homem', 'Mulher']

# Mapping of days from English to Portuguese
days_of_week_translation = {
    'Monday': 'Segunda-feira',
    'Tuesday': 'Terça-feira',
    'Wednesday': 'Quarta-feira',
    'Thursday': 'Quinta-feira',
    'Friday': 'Sexta-feira',
    'Saturday': 'Sabado',
    'Sunday': 'Domingo'
}

# Function to generate a single ride entry
def generate_ride():
    start_time = fake.date_time_this_year()
    duration = random.randint(10, 70)  # Duration between 10 minutes and 1 hour and 10 minutes
    end_time = start_time + pd.Timedelta(minutes=duration)
    weather = random.choice(weather_conditions)
    location_from = random.choice(locations)
    location_to = random.choice([loc for loc in locations if loc != location_from])
    sex_passenger = random.choice(sex_options)
    sex_driver = random.choice(sex_options)
    age = random.randint(18, 75)
    
    # Base price between $15 and $55
    base_price = random.uniform(15.0, 55.0)
    
    # Get the day of the week from start_time and translate to Portuguese
    day_of_week = start_time.strftime('%A')
    day_of_week_pt = days_of_week_translation[day_of_week]
    
    # Adjust price based on day of the week, rush hours & duration
    if day_of_week_pt in ['Sexta-feira', 'Sabado', 'Domingo', 'Segunda-feira']:
        base_price *= 1.25  # 25% increase on weekends and Mondays
    
    # Adjust price based on time of the day
    if start_time.hour >= 22 or start_time.hour < 6:
        base_price *= 1.25  # 25% increase during night
    
    if (7 <= start_time.hour < 10) or (17 <= start_time.hour < 20):
        base_price *= 1.45  # 45% increase during rush hours

    # Adjust price based on duration
    if 30 <= duration <= 50:
        base_price *= 1.20  # 20% increase for rides between 30 and 50 minutes
    elif duration > 50:
        base_price *= 1.30  # 30% increase for rides longer than 50 minutes
    
    price = round(base_price, 2)
    
    return {
        'inicio_da_corrida': start_time,
        'fim_da_corrida': end_time,
        'clima': weather,
        'local_de_partida': location_from,
        'local_de_destino': location_to,
        'sexo_do_passageiro': sex_passenger,
        'sexo_do_motorista': sex_driver,
        'preço_da_corrida': price,
        'idade_do_passageiro': age,
        'duracao_da_corrida': duration,
        'dia_da_semana': day_of_week_pt  # Adding day of the week in Portuguese
    }

# Generate the dataset
n_entries = 250000
data = [generate_ride() for _ in range(n_entries)]

# Create a DataFrame
df = pd.DataFrame(data)

# Save to a CSV file
df.to_csv('uber_rides_curitiba.csv', index=False)

# Save to an Excel file
df.to_excel('uber_rides_curitiba.xlsx', index=False)

print('Dataset generated and saved to uber_rides.csv and uber_rides.xlsx')
