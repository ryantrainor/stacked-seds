from src.image import ImageGenerator


def test_generate_image():
    """
        Tests the generate_image function
    """
    # Arrange
    image = ImageGenerator()
    # Act
    image.generate_cutout("test/images/test_image.fits", (0, 0))
    # Assert
    assert image.cutout is not None
    assert image.cutout.shape == (51, 51)
    assert image.cutout.data.shape == (51, 51)
    assert image.cutout.data[0][0] == 0.0
    assert image.cutout.data[50][50] == 0.0
    assert image.cutout.data[25][25] == 0.0

if __name__ == "__main__":
    test_generate_image()
    print("test_image.py passed \033[92m\033[1m\u2713\033[0m")