import pytesseract as ocr
import numpy as np
import cv2

from PIL import Image


# tipando a leitura para os canais de ordem RGB
fotoResultado = Image.open('resultado.png').convert('RGB')
width, height = fotoResultado.size
print(width)
p1_left = width / 5
p1_top = 2 * height / 5 #ok
p1_right = width / 3 #ok
p1_bottom = 3 * height / 5 #ok


p2_left = 4 * width / 6 #ok
p2_top = 2 * height / 5 #ok
p2_right = 5 * width / 6 #ok
p2_bottom = 3 * height / 5 #ok

im1 = fotoResultado.crop((p1_left, p1_top, p1_right, p1_bottom))
im2 = fotoResultado.crop((p2_left, p2_top, p2_right, p2_bottom))
im1.show()
#im2.show()
imagens = [im1, im2]
# convertendo em um array editável de numpy[x, y, CANALS]
for imagem in imagens:
  npimagem = np.asarray(imagem).astype(np.uint8)  

  # diminuição dos ruidos antes da binarização
  npimagem[:, :, 0] = 0 # zerando o canal R (RED)
  npimagem[:, :, 2] = 0 # zerando o canal B (BLUE)

  # atribuição em escala de cinza
  im = cv2.cvtColor(npimagem, cv2.COLOR_RGB2GRAY) 

  # aplicação da truncagem binária para a intensidade
  # pixels de intensidade de cor abaixo de 127 serão convertidos para 0 (PRETO)
  # pixels de intensidade de cor acima de 127 serão convertidos para 255 (BRANCO)
  # A atrubição do THRESH_OTSU incrementa uma análise inteligente dos nivels de truncagem
  ret, thresh = cv2.threshold(im, 127, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU) 

  # reconvertendo o retorno do threshold em um objeto do tipo PIL.Image
  binimagem = Image.fromarray(thresh) 

  # chamada ao tesseract OCR por meio de seu wrapper
  phrase = ocr.image_to_string(binimagem)

  # impressão do resultado
  print('#################')
  print(phrase) 
