import sys
import numpy as np
np.set_printoptions(threshold=sys.maxsize)

from PIL import Image
import matplotlib.pyplot as plt
import seaborn as sns
import time

from crypt_utils import generate_keypair
from image_utils import Im_encrypt, Im_decrypt, Brighten, Negation, LPF, Sharpen, Edge, Dilation, Hist_equal


def time_vs_size():
    ##############################################################################################
    # Image size vs time required for each operation
    ##############################################################################################

    IMG_SIZES = [50, 100, 200, 300, 400, 500]

    encryption_times = [0] * len(IMG_SIZES)     # e
    decryption_times = [0] * len(IMG_SIZES)     # d
    brighten_times = [0] * len(IMG_SIZES)       # b
    negation_times = [0] * len(IMG_SIZES)       # n
    lpf_times = [0] * len(IMG_SIZES)            # l
    sharpen_times = [0] * len(IMG_SIZES)        # s
    edge_times = [0] * len(IMG_SIZES)           # ed
    dilation_times = [0] * len(IMG_SIZES)       # di
    histeq_times = [0] * len(IMG_SIZES)         # h

    private_key, public_key = generate_keypair(num_digit=4)

    real_img = Image.open('lena.jpg').convert('L')

    for idx, MAX_IMG_DIM in enumerate(IMG_SIZES):
        img = np.asarray(real_img.resize((MAX_IMG_DIM, real_img.height * MAX_IMG_DIM // real_img.width)))
        s = time.time()

        """ Encryption """
        cipher_image = Im_encrypt(public_key, img)
        e = time.time()
        encryption_times[idx] = e - s

        """ Decryption """
        decrpted_img = Im_decrypt(private_key, public_key, cipher_image)
        d = time.time()
        decryption_times[idx] = d - e

        """ Brightening """
        b_img = Im_decrypt(private_key, public_key, Brighten(public_key, cipher_image, 100))
        b = time.time()
        brighten_times[idx] = b - d

        """ Negation """
        n_img = Im_decrypt(private_key, public_key, Negation(public_key, cipher_image))
        n = time.time()
        negation_times[idx] = n - b

        """ LPF """
        l_img = Im_decrypt(private_key, public_key, LPF(public_key, cipher_image, filter_type='linear', kernal_size=3))
        ll = time.time()
        lpf_times[idx] = ll - n

        """ Sharpen """
        s_img = Im_decrypt(private_key, public_key, Sharpen(public_key, cipher_image, 1))
        s = time.time()
        sharpen_times[idx] = s - ll

        """ Edge """
        Gx = Im_decrypt(private_key, public_key, Edge(public_key, cipher_image)[0])
        Gy = Im_decrypt(private_key, public_key, Edge(public_key, cipher_image)[1])
        G = np.sqrt(Gx**2 + Gy**2)
        ed = time.time()
        edge_times[idx] = ed - s

        """ HistEq """
        im_new = np.copy(img)
        histogram_array = np.bincount(img.flatten(), minlength=256)
        hist_cipher = Im_encrypt(public_key, histogram_array)
        pixel_transform = Im_decrypt(private_key, public_key, Hist_equal(public_key, hist_cipher, im_new.shape, private_key))

        row, column = im_new.shape
        for rr in range(row):
            for cc in range(column):
                im_new[rr][cc] = pixel_transform[im_new[rr][cc]]

        h = time.time()
        histeq_times[idx] = h - ed

        """ Dilation """
        bin_img = Image.open('dil.jpg').convert('L')
        bin_img_arr = np.asarray(bin_img.resize((MAX_IMG_DIM, bin_img.height * MAX_IMG_DIM // bin_img.width)))
        bin_cipher_image = Im_encrypt(public_key, bin_img_arr)

        s1 = time.time()
        d_img = Im_decrypt(private_key, public_key, Dilation(public_key, bin_cipher_image, kernal_size=3))
        d_img = np.clip(d_img, 0, 1)
        di = time.time()
        dilation_times[idx] = di - s1

    np.savez('experiments/times_mat.npz', e=encryption_times, d=decryption_times, b=brighten_times, n=negation_times, l=lpf_times, s=sharpen_times,
             ed=edge_times, di=dilation_times, h=histeq_times)

    """ For loading and plotting from saved matrix """
    # container = np.load('experiments/times_mat.npz')
    # encryption_times = container['e']
    # decryption_times = container['d']
    # brighten_times = container['b']
    # negation_times = container['n']
    # lpf_times = container['l']
    # sharpen_times = container['s']
    # edge_times = container['ed']
    # dilation_times = container['di']
    # histeq_times = container['h']

    sns.set_style("darkgrid")
    plt.plot(IMG_SIZES, encryption_times, color='blue', label='Encryption')
    plt.plot(IMG_SIZES, decryption_times, color='green', label='Decryption')
    plt.plot(IMG_SIZES, brighten_times, color='red', label='Brighten')
    plt.plot(IMG_SIZES, negation_times, color='turquoise', label='Negation')
    plt.plot(IMG_SIZES, lpf_times, color='magenta', label='Low Pass Filtering')
    plt.plot(IMG_SIZES, sharpen_times, color='magenta', linestyle='dashed', label='Sharpen')
    plt.plot(IMG_SIZES, edge_times, color='black', label='Edges')
    plt.plot(IMG_SIZES, dilation_times, color='green', linestyle='dashed', label='Dilation')
    plt.plot(IMG_SIZES, histeq_times, color='red', linestyle='dashed', label='Hist_equal')
    plt.xlabel('Size of image (side of square image in px)')
    plt.ylabel('Time taken (in s)')
    plt.title('Time taken in applying operations')
    plt.legend(loc='upper left', frameon=False, ncol=2)
    plt.savefig('experiments/time_vs_size.png')
    plt.show()


def shades_of_lpf():
    MAX_IMG_DIM = 400

    private_key, public_key = generate_keypair(num_digit=4)

    f, ax = plt.subplots(2, 3)
    img = Image.open('lena.jpg').convert('L')
    img = np.asarray(img.resize((MAX_IMG_DIM, img.height * MAX_IMG_DIM // img.width)))
    cipher_image = Im_encrypt(public_key, img)

    for ii, ks in enumerate([3, 5, 7]):
        for jj, fil in enumerate(['linear', 'gaussian']):
            ax[jj][ii].imshow(Im_decrypt(private_key, public_key, LPF(public_key, cipher_image, filter_type=fil, kernal_size=ks)), cmap='gray', vmin=0, vmax=255)
            ax[jj][ii].set_title(fil + " filter with \n" + str(ks) + " kernal size")

    plt.savefig('experiments/lpf_images.png')
    plt.show()


def shades_of_dilation():
    MAX_IMG_DIM = 400

    private_key, public_key = generate_keypair(num_digit=4)

    f, ax = plt.subplots(1, 4)
    img = Image.open('dil.jpg').convert('L')
    img = np.asarray(img.resize((MAX_IMG_DIM, img.height * MAX_IMG_DIM // img.width)))
    cipher_image = Im_encrypt(public_key, img)

    ax[0].imshow(img, cmap='gray')
    ax[0].set_title("Original image")
    for ii, ks in enumerate([5, 10, 20]):
        ax[ii + 1].imshow(np.clip(Im_decrypt(private_key, public_key, Dilation(public_key, cipher_image, kernal_size=ks)), 0, 1), cmap='gray', vmin=0, vmax=1)
        ax[ii + 1].set_title("Kernal size = " + str(ks))

    plt.savefig('experiments/dil_images.png')
    plt.show()


def shades_of_brighten():
    MAX_IMG_DIM = 400

    private_key, public_key = generate_keypair(num_digit=4)

    f, ax = plt.subplots(1, 4)
    img = Image.open('lena.jpg').convert('L')
    img = np.asarray(img.resize((MAX_IMG_DIM, img.height * MAX_IMG_DIM // img.width)))
    cipher_image = Im_encrypt(public_key, img)

    ax[0].imshow(img, cmap='gray')
    ax[0].set_title("Original image")
    for ii, ks in enumerate([20, 50, 100]):
        ax[ii + 1].imshow(Im_decrypt(private_key, public_key, Brighten(public_key, cipher_image, ks)), cmap='gray', vmin=0, vmax=255)
        ax[ii + 1].set_title("Brightness added: " + str(ks))

    plt.savefig('experiments/bri_images.png')
    plt.show()


def shades_of_sharpen():
    MAX_IMG_DIM = 400

    private_key, public_key = generate_keypair(num_digit=4)

    f, ax = plt.subplots(1, 4)
    img = Image.open('lena.jpg').convert('L')
    img = np.asarray(img.resize((MAX_IMG_DIM, img.height * MAX_IMG_DIM // img.width)))
    cipher_image = Im_encrypt(public_key, img)

    ax[0].imshow(img, cmap='gray')
    ax[0].set_title("Original image")
    for ii, ks in enumerate([3, 10, 20]):
        ax[ii + 1].imshow(Im_decrypt(private_key, public_key, Sharpen(public_key, cipher_image, ks)), cmap='gray', vmin=0, vmax=255)
        ax[ii + 1].set_title("Sharpness added: " + str(ks))

    plt.savefig('experiments/shrp_images.png')
    plt.show()


if __name__ == '__main__':
    shades_of_sharpen()
