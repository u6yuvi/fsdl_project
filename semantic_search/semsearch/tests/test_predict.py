from semsearch.predict import make_predictions


def test_prediction(sample_input_data):
    # Given
    sample_query = "Two dogs playing in the snow"

    # When
    subject = make_predictions(sample_query)

    # Then
    assert subject is not None
    prediction = subject[0]
    assert isinstance(prediction, dict)
