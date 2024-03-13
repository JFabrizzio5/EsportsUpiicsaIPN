import requests
from bs4 import BeautifulSoup

# Obtener información de agentes
url_agents = "https://tracker.gg/valorant/db/agents/sova"
response_agents = requests.get(url_agents)

# Obtener información de mapas
url_maps = "https://tracker.gg/valorant/db/maps"
response_maps = requests.get(url_maps)

if response_agents.status_code == 200 and response_maps.status_code == 200:
    # Parsear el HTML de agentes
    soup_agents = BeautifulSoup(response_agents.text, 'html.parser')
    agent_divs = soup_agents.find_all('a', {'class': 'agent-nav-agent'})

    # Parsear el HTML de mapas
    soup_maps = BeautifulSoup(response_maps.text, 'html.parser')
    map_divs = soup_maps.find_all('a', {'class': 'valorant-card'})

    # Crear contenido HTML para la tabla de agentes
    html_agents = '<table border="1"><tr><th>Imagen</th><th>Nombre</th></tr>'

    for agent_div in agent_divs:
        img_url = agent_div.find('img')['src']
        agent_name = agent_div.find('img')['title']
        html_agents += f'<tr><td><img src="{img_url}" alt="{agent_name}" width="200" height="200"></td><td style="font-size: 20px; color: white;">{agent_name}</td></tr>'

    html_agents += '</table>'

    # Crear contenido HTML para la tabla de mapas
    html_maps = '<table border="1"><tr><th>Imagen</th><th>Nombre</th><th>URL</th></tr>'

    for map_div in map_divs:
        img_style = map_div['style']
        img_url = img_style[img_style.find("(") + 1:img_style.find(")")] if 'style' in map_div.attrs and 'background-image' in img_style else ''
        map_name = map_div.find('span', {'class': 'valorant-card__name'}).text.strip()
        map_url = map_div['href']
        html_maps += f'<tr><td><img src="{img_url}" alt="{map_name}" width="1920" height="1080"></td><td>{map_name}</td><td>{map_url}</td></tr>'

    html_maps += '</table>'

    # Guardar el contenido HTML en un archivo
    with open('agents_and_maps.html', 'w', encoding='utf-8') as html_file:
        html_file.write(f"<html><head></head><body>{html_agents}<br>{html_maps}</body></html>")

    print("Se ha creado el archivo 'agents_and_maps.html'. Abre este archivo en un navegador web para ver el resultado.")

else:
    print("Error al obtener la página. Verifica las URLs proporcionadas.")
