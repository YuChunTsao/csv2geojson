import os
import pytest
from csv2geojson.scripts import cli
from unittest import mock


@pytest.mark.parametrize("option", ("-h", "--help"))
def test_help(capsys, option):
    try:
        cli.main([option])
    except SystemExit:
        pass
    output = capsys.readouterr().out
    assert "Convert csv to geojson" in output


@pytest.mark.parametrize("option", ("-v", "--version"))
def test_version(capsys, option):
    try:
        cli.main([option])
    except SystemExit:
        pass
    output = capsys.readouterr().out
    assert cli.__version__ in output


@pytest.fixture
def tmp_out_geojson(tmpdir):
    out_geojson = tmpdir.join("outout.geojson")
    return out_geojson


in_csv = os.path.join(os.path.dirname(__file__), "fixtures", "input.csv")
out_geojson = "/tmp/output.geojson"


@pytest.mark.parametrize(
    "argv",
    [
        ([in_csv, out_geojson, "-lat", "latitude", "-long", "longitude"]),
    ],
)
def test_parse_required_columns(argv):
    with mock.patch("sys.argv", [""] + argv):
        try:
            parsed_args = cli.parse_args()
            assert parsed_args.input == in_csv
            assert parsed_args.output == out_geojson
            assert parsed_args.lat == "latitude"
            assert parsed_args.long == "longitude"
        except SystemExit:
            pass


@pytest.mark.parametrize(
    "argv",
    [
        (
            [
                in_csv,
                out_geojson,
                "-lat",
                "latitude",
                "-long",
                "longitude",
                "-include_columns",
                "name",
                "latitude",
                "longitude",
            ]
        ),
    ],
)
def test_parse_include_get_list(argv):
    with mock.patch("sys.argv", [""] + argv):
        try:
            parsed_args = cli.parse_args()
            assert parsed_args.include_columns == ["name", "latitude", "longitude"]
        except SystemExit:
            pass


@pytest.mark.parametrize(
    "argv",
    [
        (
            [
                in_csv,
                out_geojson,
                "-lat",
                "latitude",
                "-long",
                "longitude",
                "-exclude_columns",
                "name",
                "latitude",
                "longitude",
            ]
        ),
    ],
)
def test_parse_exclude_get_list(argv):
    with mock.patch("sys.argv", [""] + argv):
        try:
            parsed_args = cli.parse_args()
            assert parsed_args.exclude_columns == ["name", "latitude", "longitude"]
        except SystemExit:
            pass


@pytest.mark.parametrize(
    "argv",
    [
        (
            [
                in_csv,
                out_geojson,
                "-lat",
                "latitude",
                "-long",
                "longitude",
                "-include_columns",
                "a_column",
                "-exclude_columns",
                "a_column",
            ]
        ),
    ],
)
def test_mutually_exclusive_group(argv):
    with mock.patch("sys.argv", [""] + argv):
        try:
            cli.parse_args()
        except SystemExit:
            assert True
