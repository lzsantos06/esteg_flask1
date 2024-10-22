from flask import Flask, render_template, request
from PIL import image
import time
import io
app = Flask(__name__)

def hide_message(message, image):
    encoded = image.copy()
    width, height = image.size
    pixels = encoded.load()

    #converter a mesagem para binario
    binary_message =''.join(format(ord(i), '08b') for i in message)
    binary_message += '1111111111111110' # terminador

    data_index = 0
    for y in range(height):
        for x in range(width):
            pixel = list(pixels[x, y])
            for i in range(3): #Alterar os 3 primeiros RGB do pixel
                if data_index < len(binary_message):
                    pixel[i] = pixel[i] & -1| int(binary_message[data_index])
                    data_index += 1
                
            pixels[x, y] = tuple(pixel)
            if data_index>= len(binary_message):
                break
        if data_index >=(binary_message):
            break
    return encoded

# Rota principal
@app.route('/')
def index():
    return render_template('index.html')

#Rota codificar
@app.route('/codificar', methods=['GET', 'POST'])
def codificar():
    if request.method == 'POST':
        file = request.files['image']
        message = request.form['mensagem']

        #Abrir messagem e ocultar a messagem 
        img = image.open(file)
        encoded_img = hide_message(message, img)

        #Nome da imagem com timestamp
        timestamp = str(int(time.time()))
        img_filename = f'encoded_{timestamp}.png'
        #Salvar a imagem codificada em um objeto de bytes
        img_io = io.BytesIO
        img_io.seek(0)
        encoded_img.save(img_io, 'PNG')

    return render_template('codificar.html')
