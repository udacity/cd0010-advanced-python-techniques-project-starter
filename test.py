import models

if __name__ == '__main__':
    import extract

    neos: list[models.NearEarthObject] = extract.load_neos('./data/neos.csv')
    approaches: list[models.CloseApproach] = extract.load_approaches(
        './data/cad.json')


    print('hello')
