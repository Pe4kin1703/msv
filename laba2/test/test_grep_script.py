import pytest
import src.main as s


@pytest.fixture(scope="module")
def module_fixture():
    print("FIXTURE with MODULE level was called")

@pytest.fixture()
def func_fixture():
    print("FIXTURE with FUNCTION level was called")

@pytest.mark.parametrize(
    "file_name, pattern, expected_name",
    [
        pytest.param("aboba", "rfi", "rfi-", id="TestCase1"),
        pytest.param("journal-after-boot-2.log", "rfi", "rfi-after-boot-2.log", id="TestCase2")
    ]
)
def test_create_output_file_name(module_fixture, func_fixture, file_name, pattern, expected_name):
    print(f"Test case {id=} with parameters: {file_name=}, {pattern=}, {expected_name=} started")
    output_file_name = s.creat_output_file_name(file_name, pattern)
    print(f"{output_file_name=}")
    assert (output_file_name == expected_name) , f"{output_file_name=} but {expected_name=} was expected"

@pytest.mark.parametrize(
    "file_name, pattern, exception_text",
    [
        pytest.param("journal-after-boot-2.log", "rfi", "", id="TestCase1"),
        pytest.param("journal-after-boot-3.log", "rfi", "file name is empty", id="TestCase2")
    ]
)
def test_verify_cmd_args(module_fixture, func_fixture, file_name, pattern, exception_text):
    print(f"Test case {id=} with parameters: {file_name=}, {pattern=}, {exception_text=} started")
    try:
        s.verify_cmd_args(file_name, pattern)
    except Exception as e:
        assert e == Exception(exception_text), f"{exception_text=} but {e=} was expected"




