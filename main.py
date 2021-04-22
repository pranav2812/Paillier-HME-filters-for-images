import sys
import numpy as np
np.set_printoptions(threshold=sys.maxsize)

from PIL import Image
import matplotlib.pyplot as plt
import time

from crypt_utils import generate_keypair
from crypt_utils import encrypt, decrypt, new_paillier_mul
from image_utils import Im_encrypt, Im_decrypt, Brighten, Negation, LPF, Sharpen, Edge, Dilation

MAX_IMG_DIM = 400

private_key, public_key = generate_keypair(num_digit=4)

# f, ax = plt.subplots(2, 3)
# f, ax = plt.subplots(1, 1)

img = Image.open('lena.jpg').convert('L')

img = np.asarray(img.resize((MAX_IMG_DIM, img.height * MAX_IMG_DIM // img.width)))

s = time.time()
# ax[0][0].imshow(img, cmap='gray', vmin=0, vmax=255)
# ax[0][0].set_title('Orignal image')

# ax[0].imshow(img, cmap='gray', vmin=0, vmax=255)
# ax[0].set_title('Orignal image')

cipher_image = Im_encrypt(public_key, img)
# ax[0][1].imshow(cipher_image.astype(float))
# ax[0][1].set_title('Encrypted image')


# r_img = Im_decrypt(private_key, public_key, cipher_image)
# ax[0][2].imshow(r_img, cmap='gray', vmin=0, vmax=255)
# ax[0][2].set_title('Decrypted image')

# n_img = Im_decrypt(private_key, public_key, Negation(public_key, cipher_image))
# ax[0][2].imshow(n_img, cmap='gray', vmin=0, vmax=255)
# ax[0][2].set_title('Negative image')

# s_img = Im_decrypt(private_key, public_key, Sharpen(public_key, cipher_image, 1))
# ax[1][0].imshow(s_img, cmap='gray', vmin=0, vmax=255)
# ax[1][0].set_title('Sharpened image')


# l_img = Im_decrypt(private_key, public_key, LPF(public_key, cipher_image, filter_type='linear', kernal_size=3))
# ax[1][1].imshow(l_img, cmap='gray', vmin=0, vmax=255)
# ax[1][1].set_title('LPF image')


# b_img = Im_decrypt(private_key, public_key, Brighten(public_key, cipher_image, 100))
# ax[1][2].imshow(b_img, cmap='gray', vmin=0, vmax=255)
# ax[1][2].set_title('Brightened image')


# Gx = Im_decrypt(private_key, public_key, Edge(public_key, cipher_image)[0])
# Gy = Im_decrypt(private_key, public_key, Edge(public_key, cipher_image)[1])
# G = np.sqrt(Gx**2 + Gy**2)
# ax[1][2].imshow(G, cmap='gray', vmin=0, vmax=255)
# ax[1][2].set_title('Edge image')

f, ax = plt.subplots(1, 2)
d_img = Im_decrypt(private_key, public_key, Dilation(public_key, cipher_image, kernal_size=3))
d_img = np.clip(d_img, 0, 1)
real_img_binary = np.clip(img, 0, 1)
# print(s_img)

ax[0].imshow(real_img_binary, cmap='gray', vmin=0, vmax=1)
ax[0].set_title('Binary input')

ax[1].imshow(d_img, cmap='gray', vmin=0, vmax=1)
ax[1].set_title('Dilated output')

plt.show()
