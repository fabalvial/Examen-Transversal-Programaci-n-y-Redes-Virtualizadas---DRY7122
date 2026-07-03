import requests

key = "9cde12d4-faa9-4b8a-9718-42f145f219ee"

# Diccionario para traducir la entrada en español a los perfiles que acepta la API
perfiles_api = {
    "auto": "car",
    "bus": "car", 
    "avion": "car", # GraphHopper no traza rutas aéreas; se asimila a ruta terrestre para evitar error
    "bicicleta": "bike"
}

while True:
    origen = input("Ciudad de Origen (o 's' para salir): ")
    if origen.lower() == 's': 
        break
    destino = input("Ciudad de Destino: ")
    transporte = input("Medio de transporte (auto, bus, avion, bicicleta): ").lower()

    if transporte not in perfiles_api:
        print("Medio de transporte no reconocido. Intente nuevamente.")
        continue

    vehiculo = perfiles_api[transporte]

    try:
        # Obtener coordenadas
        url_o = f"https://graphhopper.com/api/1/geocode?q={origen}&key={key}"
        url_d = f"https://graphhopper.com/api/1/geocode?q={destino}&key={key}"
        
        datos_o = requests.get(url_o).json()
        datos_d = requests.get(url_d).json()
        
        lat_o, lng_o = datos_o['hits'][0]['point'].values()
        lat_d, lng_d = datos_d['hits'][0]['point'].values()

        # Calcular ruta agregando locale=es para la narrativa en español
        url_route = f"https://graphhopper.com/api/1/route?point={lat_o},{lng_o}&point={lat_d},{lng_d}&vehicle={vehiculo}&locale=es&key={key}"
        respuesta_ruta = requests.get(url_route).json()

        # Evitar el error de 'paths' si la API no encuentra una ruta posible
        if 'paths' not in respuesta_ruta:
            print("\nError: La API no encontró una ruta terrestre posible entre estas ubicaciones.")
            continue

        res = respuesta_ruta['paths'][0]

        km = res['distance'] / 1000
        millas = km * 0.621371
        tiempo = res['time'] / 60000

        print(f"\nDistancia: {km:.2f} kilómetros / {millas:.2f} millas.")
        print(f"Duración del viaje: {tiempo:.2f} minutos.")
        print("Narrativa del viaje:")
        for instr in res['instructions']:
            print("-", instr['text'])
        print("-" * 30)

    except Exception as e:
        print("\nOcurrió un error al conectar con la API. Verifique su API Key o las ciudades ingresadas.")
