from decimal import Decimal


def extended_euclidean_algorithm(a, b):
    x0, x1, y0, y1 = 0, 1, 1, 0
    while a != 0:
        q, b, a = b // a, a, b % a
        y0, y1 = y1, y0 - q * y1
        x0, x1 = x1, x0 - q * x1
    return b, x0, y0


def main():
    c1 = 13740701343175031613859506260680271  # primo ciphertext intercettato
    c2 = 442020648620790478265510268903148188611479520134128911  # secondo ciphertext intercettato
    e1 = 7
    e2 = 11

    n = 1200867589138402836833011627922648843865398758356119243237528992192661195883356632897345588719304934438534205354787918897834861577085344762327143956220911721261528444200091612203799709834594997775067917847690315178675148605331912292785817786238119642200812571328900475396454557843711810878201457471117182510681991129539167165552073440243913144926216242708247975357913354302233984628116835035339887667027876020733894592318754941490852771134623356130705203596572659

    # calcolo i coefficienti di Bezout x, y tali che d = mcd(d1,d2) = d1*x +d2*y
    _, x, y = extended_euclidean_algorithm(e1, e2)

    # calcolo del plaintext basato sull'identità di Bezout

    m = Decimal((c1 ** x) * (c2 ** y)) % n
    m = int(m)
    print(m)

    # encryption del messaggio con la prima chiave per verifica
    t1 = (m ** e1) % n
    t1 = int(t1)
    print(t1 == c1)

    # encryption del messaggio con la seconda chiave per verifica
    t2 = (m ** e2) % n
    t2 = int(t2)
    print(t2 == c2)


if __name__ == '__main__':
    main()
