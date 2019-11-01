import zwift_generator as gx


class TestClass:
    input_dict_for_steady = dict(Power="0.5", Duration="3600", Cadence="100")
    input_dict_for_steady_no_cadence = dict(Power="0.5", Duration="3600")

    def test_generate_steady_with_cadence(self):
        result = gx.generate_workout_segment_dictionary_steady(self.input_dict_for_steady)
        assert "Cadence" in result

    def test_generate_steady_without_cadence(self):
        result = gx.generate_workout_segment_dictionary_steady(self.input_dict_for_steady_no_cadence)
        assert "Cadence" not in result

    # def test_two(self):
    #     x = "check"
    #     assert hasattr(x, "check")
