import requests
import os
import json

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
    response = requests.get(spreadsheet_url)
    
    # Wyciągnij fragment JSON z odpowiedzi
    start_index = response.text.find("google.visualization.Query.setResponse(")
    end_index = response.text.rfind(");")
    json_data = response.text[start_index + len("google.visualization.Query.setResponse("):end_index]

    # Parsuj JSON
    data = json.loads(json_data)

    # Utwórz katalog docelowy, jeśli nie istnieje
    os.makedirs(target_directory, exist_ok=True)

    # Lista do śledzenia wierszy, z których udało się pobrać obrazki
    successful_rows = []

    # Iteruj przez dane i pobierz obrazki
    for row_number, row in enumerate(data["table"]["rows"], start=1):
        # Sprawdź, czy kolumna "miniatura" istnieje i ma wartość
        if "c" in row and len(row["c"]) > 10 and row["c"][10] and "v" in row["c"][10] and row["c"][10]["v"]:
            image_url = row["c"][10]["v"]  # Kolumna "miniatura" (numer kolumny 10)
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
