def get_height():
    while True:
        try:
            height = int(input('Height: '))
        except:
            continue

        if height > 0 and height <= 8:
            return height


def make_half_pyramids(height):
    for i in range(1, height + 1):
        # Pirâmide esquerda (espaços)
        for j in range(height - i):
            print(" ", end='')

        # Pirâmide esquerda (hashes)
        for j in range(i):
            print('#', end='')

        # Espaços
        for j in range(2):
            print(' ', end='')

        # Pirâmide direita (hashes)
        for j in range(i):
            print('#', end='')

        print()


def main():
    height = get_height()
    make_half_pyramids(height)


main()