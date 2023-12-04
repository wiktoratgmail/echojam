import requests
import json
import os

# URL do arkusza Google Spreadsheet
spreadsheet_url = "https://docs.google.com/spreadsheets/d/1hTaNoVxeK5HBXI7FHMMPKznvILbudUpxgRslYouw34Q/gviz/tq?tqx=out:json&tq&gid=0"

# Katalog docelowy dla obrazków w repozytorium GitHub
target_directory = "img"

def download_image(image_url, target_path):
    response = requests.get(image_url)
    if response.status_code == 200:
        with open(target_path, "wb") as f:
            f.write(response.content)
        return True
    else:
        return False

def main():
    # Pobierz dane z arkusza Google Spreadsheet (zakłada formatowanie danych w formie JSON)
    response = requests.get(spreadsheet_url + "/exec?format=json")
    
    # Wytnij niepotrzebne fragmenty JavaScript i pozostaw czysty JSON
    json_data = response.text.split("google.visualization.Query.setResponse(")[1].rstrip(");")
    
    # Parsuj czysty JSON
    data = json.loads(json_data)

    # Utwórz katalog docelowy, jeśli nie istnieje
    os.makedirs(target_directory, exist_ok=True)

    # Lista do śledzenia wierszy, z których udało się pobrać obrazki
    successful_rows = []

    # Iteruj przez dane i pobierz obrazki
    for row_number, row in enumerate(data["table"]["rows"], start=1):
        image_url = row["c"][9]["v"]  # Zastąp indeks, aby uzyskać URL obrazków
        if image_url:
            image_name = os.path.basename(image_url)
            target_path = os.path.join(target_directory, image_name)

            # Sprawdź, czy obrazek już istnieje w katalogu
            if not os.path.exists(target_path):
                success = download_image(image_url, target_path)
                if success:
                    successful_rows.append(row_number)

    # Ustaw wynik do przekazania informacji zwrotnej do GitHub Actions
    print(f"::set-output name=successful_rows::{','.join(map(str, successful_rows))}")

if __name__ == "__main__":
    main()
