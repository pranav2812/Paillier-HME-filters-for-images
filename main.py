import sys
import numpy as np
np.set_printoptions(threshold=sys.maxsize)

from PIL import Image
import matplotlib.pyplot as plt
import time

from crypt_utils import generate_keypair
from crypt_utils import encrypt, decrypt, new_paillier_mul
from image_utils import Im_encrypt, Im_decrypt, Brighten, Negation, LPF

MAX_IMG_DIM = 400

private_key, public_key = generate_keypair(num_digit=4)

# f, ax = plt.subplots(2, 3)

img = Image.open('lena.jpg').convert('L')

img = np.asarray(img.resize((MAX_IMG_DIM, img.height * MAX_IMG_DIM // img.width)))

# ax[0][0].imshow(img, cmap='gray', vmin=0, vmax=255)
# ax[0][0].set_title('Orignal image')

cipher_image = Im_encrypt(public_key, img)
# ax[0][1].imshow(cipher_image.astype(float))
# ax[0][1].set_title('Encrypted image')


# r_img = Im_decrypt(private_key, public_key, cipher_image)
# ax[0][2].imshow(r_img, cmap='gray', vmin=0, vmax=255)
# ax[0][2].set_title('Decrypted image')


# b_img = Im_decrypt(private_key, public_key, Brighten(public_key, cipher_image, 100))
# ax[1][0].imshow(b_img, cmap='gray', vmin=0, vmax=255)
# ax[1][0].set_title('Brightened image')


# n_img = Im_decrypt(private_key, public_key, Negation(public_key, cipher_image))
# ax[1][1].imshow(n_img, cmap='gray', vmin=0, vmax=255)
# ax[1][1].set_title('Negative image')

s = time.time()
l_img = Im_decrypt(private_key, public_key, LPF(public_key, cipher_image, private_key))
# ax[1][2].imshow(l_img, cmap='gray', vmin=0, vmax=255)
# ax[1][2].set_title('LPF image')
print(type(l_img))
# print(l_img)
plt.imshow(l_img, cmap='gray', vmin=0, vmax=255)
# plt.set_title('LPF image')
print("Time taken = %d s" % (time.time() - s))
plt.show()

# a = 1307
# b = 1 / 9
# e = decrypt(private_key, public_key, new_paillier_mul(public_key, encrypt(public_key, a), b))
# print(e)
