import matplotlib.pyplot as plt
import numpy as np
import stars as stars
import GUI as gui

mintaka = stars.Star("Mintaka", 30000, 0.96, "img", "img")
rigel = stars.Star("Rigel", 11000, 0.12, "img", "img")
wega = stars.Star("Wega", 9602, 0.03, "img", "img")
polarstern = stars.Star("Polarstern", 6900, 0.02, "img", "img")
sun = stars.Star("Sonne", 5772, -26.74, "img", "img")
aldebaran = stars.Star("Aldebaran", 3910, 0.87, "images/aldebaran-spectrum-raw.png", "images/aldebaran-spectrum.png")
beteigeuze = stars.Star("Beteigeuze", 3500, 0.58, "img", "img")

stars_list = np.array([mintaka, rigel, wega, polarstern, sun, aldebaran, beteigeuze])

temperatur = np.array([star.temperature for star in stars_list])
temperatur_x_values = []
leuchtkraft = np.array([star.magnitude for star in stars_list])

fig, ax = plt.subplots()
ax.set_ylabel("Absolute Helligkeit in mag")
ax.set_xlabel("Spektralklassen (ermittelt durch Temperatur)")
ax.set_title("Hertzsprung-Russel-Diagramm")
ax.grid(True, linestyle="--")

spectral_class_info = {
    'O': {'temp_min': 30000, 'temp_max': 40000},
    'B': {'temp_min': 10000, 'temp_max': 30000},
    'A': {'temp_min': 7500, 'temp_max': 10000},
    'F': {'temp_min': 6000, 'temp_max': 7500},
    'G': {'temp_min': 5200, 'temp_max': 6000},
    'K': {'temp_min': 3700, 'temp_max': 5200},
    'M': {'temp_min': 2400, 'temp_max': 3700},
}

# --- Funktion zur Transformation der X-Achse ---
def get_x_value_via_temp(temperature):
    """
    Wandelt BP-RP Farbe in eine gleichmäßig skalierte X-Achsenposition (0 bis N Klassen) um.
    """
    temp_coords = []
    transformed_coords = []

    #temp_coords.append(spectral_class_info['O']['temp_min'] - 0.1)
    #transformed_coords.append(0)

    class_index = 0
    for s_class in ['O', 'B', 'A', 'F', 'G', 'K', 'M']:
        data = spectral_class_info[s_class]

        temp_coords.append(data['temp_max'])
        transformed_coords.append(class_index)

        temp_coords.append(data['temp_min'])
        transformed_coords.append(class_index + 1)

        class_index += 1

    sorted_indices = np.argsort(temp_coords)
    transformed_x = np.interp(temperature, np.array(temp_coords)[sorted_indices],
                              np.array(transformed_coords)[sorted_indices], left=transformed_coords[-1],
                              right=transformed_coords[0])
    return transformed_x

#transformed_x_value, temp_coords, transformed_coords = get_x_value_via_temp(9)

#print(transformed_x_value)
#print(temp_coords)
#print(transformed_coords)

x_ticks = [1,2,3,4,5,6,7]
ax.set_xticks(x_ticks, ['O', 'B', 'A', 'F', 'G', 'K', 'M'])

if __name__ == "__main__":

    for temp in temperatur:
        temp_x_value = get_x_value_via_temp(temp)
        temperatur_x_values.append(temp_x_value)
        values = np.array(temperatur_x_values)

    ax.scatter(values, leuchtkraft, picker=True)

def on_pick(event):
    index = event.ind[0]
    print(temperatur[index])
    gui.star_data(stars_list[index].name, stars_list[index].temperature, stars_list[index].magnitude, stars_list[index].spec_raw, stars_list[index].spec_diagram)

fig.canvas.mpl_connect("pick_event", on_pick)

plt.show()
