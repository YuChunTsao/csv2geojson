import os
import json
import pytest
from csv2geojson.csv2geojson import csv2geojson


in_csv = os.path.join(os.path.dirname(__file__), "fixtures", "input", "input.csv")


def test_include_columns(tmpdir):
    out_geojson = tmpdir.join("output.geojson")
    include_columns = ["name", "latitude", "longitude"]
    csv2geojson(in_csv, out_geojson, include_columns=include_columns)

    with open(out_geojson, "r") as f:
        data = json.load(f)
        keysList = list(data["features"][0]["properties"].keys())
        assert len(keysList) == 3


def test_exclude_columns(tmpdir):
    out_geojson = tmpdir.join("output.geojson")
    exclude_columns = ["name", "latitude", "longitude"]
    csv2geojson(in_csv, out_geojson, exclude_columns=exclude_columns)

    with open(out_geojson, "r") as f:
        data = json.load(f)
        keysList = list(data["features"][0]["properties"].keys())
        assert len(keysList) == 28


def test_without_exclude_or_include(tmpdir):
    out_geojson = tmpdir.join("output.geojson")
    csv2geojson(in_csv, out_geojson)

    with open(out_geojson, "r") as f:
        data = json.load(f)
        keysList = list(data["features"][0]["properties"].keys())
        assert len(keysList) == 31


def test_invalid_lat_column(tmpdir):
    with pytest.raises(Exception) as e:
        out_geojson = tmpdir.join("output.geojson")
        invalid_lat_column = "invalid_lat_column"
        csv2geojson(in_csv, out_geojson, lat_column=invalid_lat_column)
    assert e.type == KeyError


def test_invalid_long_column(tmpdir):
    with pytest.raises(Exception) as e:
        out_geojson = tmpdir.join("output.geojson")
        invalid_long_column = "invalid_long_column"
        csv2geojson(in_csv, out_geojson, long_column=invalid_long_column)
    assert e.type == KeyError


def test_invalid_in_csv(tmpdir):
    with pytest.raises(Exception) as e:
        invalid_in_csv = "invalid_in_csv.csv"
        out_geojson = tmpdir.join("output.geojson")
        csv2geojson(invalid_in_csv, out_geojson)
    assert e.type == FileNotFoundError
