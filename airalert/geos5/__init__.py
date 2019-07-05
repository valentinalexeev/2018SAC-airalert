"""
Data collector for GEOS-5 Earth observation data
"""

from netCDF4 import Dataset
import requests
import logging
import os
from datetime import date, timedelta
from clint.textui import progress
import numpy as np
import pprint

GEOS_BASE_URL_MASK = "https://portal.nccs.nasa.gov/datashare/gmao_ops/pub/fp/das/Y{:04d}/M{:02d}/D{:02d}/{}"
GEOS_FILE_MASK = "GEOS.fp.asm.tavg3_2d_aer_Nx.{:04d}{:02d}{:02d}_{}.V01.nc4"

GEOS_TIME_IN_DAY = ["0130"] #, "0430", "0730"]

GEOS_CACHE_MASK = "./data/geos5/{}"

SKIP_LOAD = bool(os.environ.get("AA_GEOS5_SKIP_LOAD"))

GEOS_VARIABLE_CONVERSION = {
    'DUSMASS25': 1000000000 # kg m-3 -> ppm
}

logging.basicConfig()
log = logging.getLogger("airalert.geos5");
log.setLevel(logging.DEBUG)

class FileLoader():
    def __init__(self, year, month, day, time_in_day):
#        log.info('Expecting file data for {}-{:02d}-{:02d} at {}'.format(year, month, day, time_in_day))
        self._year = year
        self._month = month
        self._day = day
        self._time_in_day = time_in_day

    def is_in_cache(self):
        fName = GEOS_CACHE_MASK.format(GEOS_FILE_MASK.format(self._year, self._month, self._day, self._time_in_day))
#        log.info('Checking if the following file exists in cache {}'.format(fName))
        return os.path.exists(fName)

    def _file_name(self):
        return GEOS_FILE_MASK.format(self._year, self._month, self._day, self._time_in_day)

    def _cached_file_name(self):
        return GEOS_CACHE_MASK.format(self._file_name())

    def load_data(self):
        if not self.is_in_cache():
            fName = self._file_name()
            log.info('File {} is missing in cache, downloading from NASA'.format(fName))
            r = requests.get(GEOS_BASE_URL_MASK.format(self._year, self._month, self._day, fName))
            fName_cache = self._cached_file_name()

            with open(fName_cache, 'wb') as f:
                total_length = int(r.headers.get('content-length'))
                for chunk in progress.bar(r.iter_content(chunk_size=1024), expected_size=(total_length/1024) + 1):
                    if chunk:
                        f.write(chunk)
                        f.flush()

    def get_training_data(self, variable, result_latlng, impact_latlngs):
        #log.info("get_training_data {}".format(self._cached_file_name()));
        result = []
        try:
            rootgrp = Dataset(self._cached_file_name())

            lats = rootgrp.variables['lat'][:]
            lons = rootgrp.variables['lon'][:]

            result_idx = [
                np.argmin(np.abs(lats - result_latlng[0])),
                np.argmin(np.abs(lons - result_latlng[1]))
            ]

            impact_idxs = []
            for impact in impact_latlngs:
                impact_idxs += [[
                    np.argmin(np.abs(lats - impact[0])),
                    np.argmin(np.abs(lats - impact[1]))
                ]]


            var = rootgrp.variables[variable]
            result = [
                int(var[:, result_idx[0], result_idx[1]][0] * GEOS_VARIABLE_CONVERSION[variable])
            ]
            for impact_idx in impact_idxs:
                result += [
                    int(var[:, impact_idx[0], impact_idx[1]][0] * GEOS_VARIABLE_CONVERSION[variable])
                ]

            rootgrp.close()
        except:
            log.warn('Unable to read GEOS-5 file {}.'.format(self._cached_file_name()))
        return result

class DataLoader():
    def __init__(self, year, month, day):
#        log.info("Will collect data from GEOS-5 on date {:4d}-{:02d}-{:02d}".format(year, month, day))
        self._year = year
        self._month = month
        self._day = day
        self._loaders = {}

    def load_data(self):
        for time_in_day in GEOS_TIME_IN_DAY:
            if not time_in_day in self._loaders:
                fl = FileLoader(self._year, self._month, self._day, time_in_day)
                if SKIP_LOAD and fl.is_in_cache():
                    self._loaders[time_in_day] = fl
                elif not SKIP_LOAD:
                    fl.load_data()
                    self._loaders[time_in_day] = fl

    def get_training_data(self, variable, result_latlng, impact_latlngs):
        result = []

        for loader in self._loaders:
            result += self._loaders[loader].get_training_data(variable, result_latlng, impact_latlngs)

        return result

class YearDataLoader():
    def __init__(self, year):
        log.info('Preparing to load data for year {}'.format(year))
        self._year = year
        self._data_loaders = {}

    def load_single(self, day_delta):
        d_next = date.today().replace(day = 1, month = 1) + timedelta(days=day_delta)
        if d_next <= date.today():
            dl = DataLoader(d_next.year, d_next.month, d_next.day)
            dl.load_data()
            return {d_next: dl}

    def load_data(self):
        log.info("Loading data");
        d = date.today().replace(day = 1, month = 1)
        for day_delta in range(367, 0, -1):
            d_next = d + timedelta(days=day_delta)
            if d_next <= date.today():
                dl = DataLoader(d_next.year, d_next.month, d_next.day)
                dl.load_data()
                self._data_loaders[d_next] = dl

    def get_training_data(self, variable, result_latlng, impact_latlngs):
        result = []

        for loader in self._data_loaders:
            data = self._data_loaders[loader].get_training_data(variable, result_latlng, impact_latlngs)
            if len(data) > 0:
                data = [loader] + data
                result += [data]

        return result

class TrainingDataExtractor():
    def __init__(self, result_latlng, impact_latlngs, year = 2018, variable = 'DUSMASS25'):
        self._variable = variable
        self._result_latlng = result_latlng
        self._impact_latlngs = impact_latlngs

        self._year_data = YearDataLoader(year)

    def get_training_data(self):
        log.info("Collecting training data for variable {}".format(self._variable))
        self._year_data.load_data()
        res = self._year_data.get_training_data(self._variable, self._result_latlng, self._impact_latlngs)

        pprint.pprint(res)

        return res
