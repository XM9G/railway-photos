import os
from datetime import date
from bs4 import BeautifulSoup

def extract_photo_urls(html_content, station_name):
    soup = BeautifulSoup(html_content, 'html.parser')
    photo_urls = []

    paragraphs = soup.find_all('p')
    for paragraph in paragraphs:
        location_tag = paragraph.find('a', href=True, text=True)
        if location_tag and station_name.lower() in location_tag.text.lower():
            img_tag = paragraph.find('img', src=True)
            if img_tag:
                photo_urls.append((img_tag['src'], location_tag['href']))
    
    return photo_urls

def check_html_files_in_folder(folder_path, station_name):
    photo_data = []

    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as html_file:
                    html_content = html_file.read()
                    urls = extract_photo_urls(html_content, station_name)
                    photo_data.extend([(url, file_path) for url, _ in urls])
    
    return photo_data

def generate_station_html(station_name, photo_data, output_folder, template_path):
    with open(template_path, 'r', encoding='utf-8') as template_file:
        html_template = template_file.read()

    photos_section = ""
    for img_url, file_path in photo_data:
        photos_section += f"<p><a href='{file_path}'><img src='{img_url}'></a><br><br>\n"
    
    html_content = html_template.format(
        station_name=station_name,
        current_date=date.today().strftime('%d-%m-%Y'),
        photos_section=photos_section
    )

    output_file_path = os.path.join(output_folder, f"{station_name.replace(' ', '_')}.html")
    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        output_file.write(html_content)

# Main function to check HTML files and generate HTML for each station
def main(folder_path, stations, output_folder, template_path):
    for station_name in stations:
        photo_data = check_html_files_in_folder(folder_path, station_name)
        if photo_data:
            generate_station_html(station_name, photo_data, output_folder, template_path)

folder_path = 'trains/melbourne'
output_folder = 'stations/melbourne'
stations = ['Armadale Station']
template_path = 'stations/template.html'

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

main(folder_path, stations, output_folder, template_path)
