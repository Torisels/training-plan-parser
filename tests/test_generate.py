# content of test_class.py
from generate_xml import generate_workout_segment_dictionary_steady as generate


class TestClass:
    input_dict = dict(Power="0.5", Duration="3600", Cadence="100")

    def test_generate(self):
        result = generate(self.input_dict)
        assert "Cadence" in result


    # def test_two(self):
    #     x = "check"
    #     assert hasattr(x, "check")
